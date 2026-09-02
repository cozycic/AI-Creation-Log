import os
from datetime import datetime

from openai import OpenAI


# ============================================================
# 基础配置
# ============================================================

APP_NAME = "七分少年 AI短视频生成器 V2.3.2"
MODEL_NAME = "deepseek-v4-flash"
BASE_URL = "https://api.deepseek.com"


# ============================================================
# AI客户端
# ============================================================

def create_client():
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        print("\n错误：没有找到 DEEPSEEK_API_KEY")
        print("请检查 DeepSeek API Key 是否已经配置。")
        raise SystemExit(1)

    return OpenAI(
        api_key=api_key,
        base_url=BASE_URL
    )


client = create_client()


# ============================================================
# 界面工具
# ============================================================

def print_line():
    print("=" * 70)


def print_title(title):
    print_line()
    print(title)
    print_line()


def ask(prompt):
    return input(prompt).strip()


# ============================================================
# AI调用
# ============================================================

def call_ai(prompt):
    try:
        response = client.responses.create(
            model=MODEL_NAME,
            input=prompt
        )

        return response.output_text.strip()

    except Exception as e:
        print("\nAI调用失败：")
        print(e)
        return None


# ============================================================
# 视频类型
# ============================================================

def choose_video_type():
    print_title("选择视频类型")

    options = {
        "1": "AI创业",
        "2": "AI工具",
        "3": "AI知识",
        "4": "个人成长",
        "5": "故事分享"
    }

    for key, value in options.items():
        print(f"{key}. {value}")

    while True:
        choice = ask("\n请选择视频类型：")

        if choice in options:
            video_type = options[choice]
            print(f"\n已选择：{video_type}")
            return video_type

        print("输入错误，请输入 1-5。")


# ============================================================
# 获取主题
# ============================================================

def get_topic():
    while True:
        topic = ask("\n请输入视频主题：")

        if topic:
            return topic

        print("主题不能为空，请重新输入。")


# ============================================================
# 标题生成
# ============================================================

def validate_titles(titles):
    """过滤明显的、未经用户提供的个人真实经历/收益型标题。"""
    blocked_patterns = [
        "我赚了", "我赚到", "我收入", "我的收入", "我接单", "我接到第一单",
        "我接到了", "我有客户", "我的客户", "我被裁", "我辞职", "我裸辞",
        "我靠AI赚", "我靠ai赚", "我盈利", "我赚了钱", "第一单",
        "到账", "真实收入", "月入", "月赚", "一个月多了", "副业收入"
    ]
    return [title for title in titles if not any(p in title for p in blocked_patterns)]


def parse_titles(result):
    titles = []
    for line in result.splitlines():
        line = line.strip()
        if not line:
            continue
        if "." in line[:4]:
            line = line.split(".", 1)[1].strip()
        elif "、" in line[:4]:
            line = line.split("、", 1)[1].strip()
        if line:
            titles.append(line)
    return titles


def generate_titles(topic, video_type):
    print_title("正在生成10个标题")

    prompt = f"""
你是一名非常懂抖音短视频的内容策划。

请围绕以下内容生成10个短视频标题。

视频类型：{video_type}
视频主题：{topic}

要求：

1. 适合抖音
2. 口语化
3. 不要太像广告
4. 有真实感
5. 能激发点击欲望
6. 尽量避免空泛鸡汤
7. 标题长度控制在15-30字左右
8. 适合普通人创作者
9. 不要夸张到虚假
10. 必须输出10个标题
11. 严禁虚构创作者本人已经发生的真实经历。
12. 严禁使用未经用户明确提供的第一人称事实，例如“我赚了”“我月入”“我接单”“我的客户”、
    “我被裁”“我辞职”“我裸辞”“我靠AI赚了钱”“我的真实收入”“第一单”等。
13. 不得暗示创作者已经获得收入、客户、订单、盈利或创业成绩。
14. 可以使用“我准备”“我想试试”“我正在记录”等表达，但必须是计划、尝试或记录，不能是假装已经成功。
15. 默认优先使用“普通人”“新手”“不会写代码的人”“想做AI创业的人”等非事实型表达。
16. 如果一个标题容易让观众误以为创作者已经取得某项真实成绩，请改写成探索、方法、问题或计划型标题。

请严格按照以下格式：

1. 标题
2. 标题
3. 标题
...
10. 标题

不要添加其他解释。
"""

    result = call_ai(prompt)
    if not result:
        return []

    titles = validate_titles(parse_titles(result))

    if len(titles) < 10:
        retry_prompt = f"""
请重新生成10个抖音短视频标题。
视频类型：{video_type}
视频主题：{topic}

这是一次安全重生成：严禁虚构创作者本人的真实经历、收入、客户、订单、盈利或创业成绩。
严禁出现“我赚了”“我月入”“我接单”“我的客户”“第一单”“我被裁”“我辞职”“我裸辞”等个人事实表达。
优先使用普通人、新手、不会写代码的人、AI创业、怎么开始、怎么做、有哪些坑、值不值得做等表达。

只输出10个标题，每行一个，格式：
1. 标题
...
10. 标题
"""
        retry_result = call_ai(retry_prompt)
        titles = validate_titles(parse_titles(retry_result))

    return titles[:10]


# ============================================================
# 标题选择
# ============================================================

def choose_title(titles, topic, video_type):
    while True:
        print_title("标题列表")

        if not titles:
            print("没有生成出有效标题。")
            return None

        for i, title in enumerate(titles, 1):
            print(f"{i}. {title}")

        print("\n操作：")
        print("输入 1-10：选择标题")
        print("R：重新生成10个标题")
        print("Q：退出")

        choice = ask("\n请选择：").lower()

        if choice == "r":
            titles = generate_titles(
                topic,
                video_type
            )
            continue

        if choice == "q":
            return None

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(titles):
                selected = titles[number - 1]

                print("\n你选择的标题：")
                print(selected)

                confirm = ask(
                    "\n使用这个标题？"
                    "（Y=使用 / R=重新选择）："
                ).lower()

                if confirm == "y":
                    return selected

                if confirm == "r":
                    continue

        print("输入错误，请重新选择。")


# ============================================================
# 口播脚本生成
# ============================================================

def generate_script(topic, video_type, selected_title):
    print_title("正在生成60秒口播脚本")

    prompt = f"""
你是一名抖音短视频编剧。

请根据下面的信息写一条约60秒的中文口播脚本。

视频类型：{video_type}
主题：{topic}
标题：{selected_title}

要求：

1. 开头3秒抓住注意力
2. 语言像真人说话
3. 不要书面腔
4. 有具体内容
5. 有情绪变化
6. 结尾自然
7. 不要强行营销
8. 控制在约180-250字
9. 适合AI配音
10. 只输出口播正文
11. 不得虚构用户本人经历、客户、订单、收入、金额、时间、身份或真实结果
12. 如果内容需要个人经历，只能使用“可以这样做”“例如”“假设”等表达，不要写成用户已经发生的事实

请直接输出脚本。
"""

    return call_ai(prompt)


# ============================================================
# 脚本确认
# ============================================================

def confirm_script(topic, video_type, selected_title):
    while True:

        script = generate_script(
            topic,
            video_type,
            selected_title
        )

        if not script:
            print("脚本生成失败。")
            return None

        print_title("60秒口播脚本")
        print(script)

        print("\n操作：")
        print("Y：使用这个脚本")
        print("R：重新生成")
        print("Q：退出")

        choice = ask("\n请选择：").lower()

        if choice == "y":
            return script

        if choice == "r":
            continue

        if choice == "q":
            return None

        print("输入错误。")


# ============================================================
# 分镜生成
# ============================================================

def generate_storyboard(selected_title, script_text):
    print_title("正在生成10镜头分镜")

    prompt = f"""
你是一名专业的抖音短视频导演。

根据下面的标题和口播脚本，设计10个镜头。

标题：
{selected_title}

口播脚本：
{script_text}

必须严格生成10个镜头。

请严格按照以下格式：

镜头1：
画面：
旁白：

镜头2：
画面：
旁白：

镜头3：
画面：
旁白：

一直到：

镜头10：
画面：
旁白：

要求：

1. 整条视频约60秒
2. 每个镜头约5-7秒
3. 画面具体
4. 尽量使用普通人容易获得的素材
5. 可以使用AI生成画面
6. 不需要真人露脸
7. 画面与旁白必须对应
8. 镜头之间要有连贯性
"""

    return call_ai(prompt)


# ============================================================
# 分镜解析
# ============================================================

def parse_storyboard(storyboard_text):
    """
    将AI返回的分镜文本拆成10个镜头。
    """

    if not storyboard_text:
        return []

    shots = []

    lines = storyboard_text.splitlines()

    current_shot = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("镜头") and current_shot:
            shots.append("\n".join(current_shot))
            current_shot = []

        current_shot.append(line)

    if current_shot:
        shots.append("\n".join(current_shot))

    return shots[:10]


# ============================================================
# 显示分镜
# ============================================================

def show_storyboard(storyboard_text):
    shots = parse_storyboard(storyboard_text)

    print_title("当前分镜")

    if not shots:
        print(storyboard_text)
        return

    for i, shot in enumerate(shots, 1):
        print(f"\n【镜头{i}】")
        print(shot)


# ============================================================
# 重新生成全部分镜
# ============================================================

def regenerate_storyboard(selected_title, script_text):
    return generate_storyboard(
        selected_title,
        script_text
    )


# ============================================================
# 单独重新生成一个镜头
# ============================================================

def regenerate_single_shot(
    selected_title,
    script_text,
    storyboard_text,
    shot_number
):

    shots = parse_storyboard(storyboard_text)

    if shot_number < 1 or shot_number > len(shots):
        print("镜头编号不存在。")
        return storyboard_text

    old_shot = shots[shot_number - 1]

    prompt = f"""
你是一名专业短视频导演。

现在需要重新设计第{shot_number}个镜头。

视频标题：
{selected_title}

完整口播：
{script_text}

当前第{shot_number}个镜头：
{old_shot}

请重新设计这个镜头。

要求：

1. 必须与整条视频主题一致
2. 必须与口播内容对应
3. 不需要真人露脸
4. 画面要容易制作
5. 可以使用AI生成画面
6. 比原来的镜头更具体
7. 只输出新的这个镜头

严格按照：

镜头{shot_number}：
画面：
旁白：
"""

    new_shot = call_ai(prompt)

    if not new_shot:
        print("重新生成失败，保留原镜头。")
        return storyboard_text

    shots[shot_number - 1] = new_shot

    return "\n\n".join(shots)


# ============================================================
# 分镜管理
# ============================================================

def manage_storyboard(selected_title, script_text):

    storyboard_text = generate_storyboard(
        selected_title,
        script_text
    )

    if not storyboard_text:
        return None

    while True:

        show_storyboard(storyboard_text)

        print("\n操作：")
        print("1. 使用当前分镜")
        print("2. 重新生成全部分镜")
        print("3. 重新生成指定镜头")
        print("4. 查看当前分镜")
        print("Q. 退出")

        choice = ask("\n请选择：").lower()

        # 使用
        if choice == "1":
            return storyboard_text

        # 全部重新生成
        elif choice == "2":

            new_storyboard = regenerate_storyboard(
                selected_title,
                script_text
            )

            if new_storyboard:
                storyboard_text = new_storyboard

        # 指定镜头
        elif choice == "3":

            number = ask(
                "\n请输入需要重新生成的镜头编号（1-10）："
            )

            if not number.isdigit():
                print("请输入数字。")
                continue

            shot_number = int(number)

            storyboard_text = regenerate_single_shot(
                selected_title,
                script_text,
                storyboard_text,
                shot_number
            )

        # 查看
        elif choice == "4":
            show_storyboard(storyboard_text)

        # 退出
        elif choice == "q":
            return None

        else:
            print("输入错误，请重新选择。")


# ============================================================
# AI画面提示词
# ============================================================

def generate_visual_prompts(
    selected_title,
    storyboard_text
):

    print_title("正在生成AI画面提示词")

    prompt = f"""
你是一名AI视频视觉导演。

根据下面的标题和分镜，为10个镜头生成AI画面提示词。

标题：
{selected_title}

分镜：
{storyboard_text}

要求：

1. 一镜一个提示词
2. 中文
3. 具体描述人物、环境、动作、光线、镜头
4. 适合AI图片或AI视频生成
5. 画面具有短视频感
6. 不要求真人露脸
7. 保持整条视频视觉风格统一
8. 必须对应10个镜头

格式：

镜头1：
提示词：

镜头2：
提示词：

一直到：

镜头10：
提示词：
"""

    return call_ai(prompt)


# ============================================================
# 剪映制作清单
# ============================================================

def generate_editing_plan(
    selected_title,
    script_text,
    storyboard_text
):

    print_title("正在生成剪映制作清单")

    prompt = f"""
你是一名专业短视频剪辑师。

请根据下面的视频内容，制作一份适合剪映执行的剪辑清单。

标题：
{selected_title}

口播：
{script_text}

分镜：
{storyboard_text}

请包含：

1. 视频比例
2. 建议时长
3. 画面节奏
4. 字幕建议
5. 字体大小建议
6. BGM建议
7. 音效建议
8. 转场建议
9. 每个镜头的大致时长
10. 最后发布前检查清单

要求简单、具体、可以直接照着做。
"""

    return call_ai(prompt)


# ============================================================
# 视频素材清单
# ============================================================

def generate_material_list(
    selected_title,
    script_text,
    storyboard_text
):
    print_title("正在生成视频素材清单")

    prompt = f"""
你是一名专业的短视频制作统筹。

请根据下面的标题、口播脚本和10个镜头分镜，制作一份“视频素材清单”。

标题：
{selected_title}

口播脚本：
{script_text}

分镜：
{storyboard_text}

你的任务不是重新写分镜，而是告诉普通创作者：
“每个镜头具体需要准备什么素材，以及最容易用什么方式获得”。

请严格按照以下格式输出：

镜头1：
素材类型：
素材内容：
获取方式：
具体要求：
备注：

镜头2：
素材类型：
素材内容：
获取方式：
具体要求：
备注：

一直到镜头10。

素材类型只能从以下几类中选择：
- 图片
- 视频
- 屏幕录制
- 手机实拍
- AI图片
- AI视频
- 文字/图形

获取方式只能优先从以下方式中选择：
- 自己拍摄
- 手机录屏
- 电脑录屏
- AI生成
- 自己制作
- 网络公开素材

要求：

1. 每个镜头必须有明确素材。
2. 优先考虑普通人可以低成本获得的素材。
3. 不需要真人露脸。
4. 如果某个镜头适合录屏，优先建议录屏。
5. 如果某个镜头适合手机拍摄，说明具体拍什么。
6. 如果适合AI生成，说明应该生成什么。
7. 不要推荐付费素材作为默认方案。
8. 不要虚构用户已经拥有某些设备、客户、订单或真实经历。
9. 每个镜头的素材必须与对应旁白和画面一致。
10. 最后增加一个“整条视频素材总清单”，按以下格式：

【整条视频素材总清单】
1. ...
2. ...
3. ...

【最低成本制作方案】
说明这条视频如果尽量不花钱，应该优先准备哪些素材。

只输出素材清单，不要写其他解释。
"""

    return call_ai(prompt)


# ============================================================
# 事实安全检查
# ============================================================

def fact_safety_check(selected_title, script_text, storyboard_text, material_list):
    """检查AI生成内容中可能被误认为真实事实的表达。"""
    print_title("正在进行事实安全检查")

    combined = f"标题：{selected_title}\n\n口播脚本：\n{script_text}\n\n分镜：\n{storyboard_text}\n\n素材清单：\n{material_list}"

    risk_patterns = [
        "官方通知", "客户微信", "客户聊天", "客户咨询", "订单截图", "收款截图",
        "到账", "月入", "月赚", "真实收入", "第一单", "我的客户", "我的订单",
        "某某公司", "产品手册", "内部数据", "后台数据", "用户数据", "真实案例",
        "已上线", "停止维护", "不再维护", "正式发布", "官方宣布", "最新版本",
        "V3.0", "V4.0", "V5.0"
    ]

    local_flags = []
    for pattern in risk_patterns:
        if pattern.lower() in combined.lower():
            local_flags.append(pattern)

    prompt = f"""
你是一名短视频事实安全审核员。

请检查下面的标题、口播脚本、分镜和素材清单，重点判断是否存在“AI为了让画面更真实而虚构事实”的问题。

内容：
{combined}

重点检查：
1. 虚构公司、品牌、客户、人物或项目名称。
2. 虚构订单、收入、利润、客户咨询、聊天记录、后台数据、产品手册等。
3. 虚构具体日期、金额、数量、用户数、增长率等并把它们说成事实。
4. 虚构“官方通知”“新闻”“产品发布”“模型版本上线”“接口停止维护”等外部事实。
5. 把“示例/假设/模拟”写成像真实发生过的事情。

请严格输出：
风险等级：低 / 中 / 高

需要核实或修改：
1. ...
2. ...

安全建议：
1. ...
2. ...

如果没有明显问题，写：需要核实或修改：无明显问题。
不要重新创作内容。
"""

    ai_report = call_ai(prompt)

    if local_flags:
        local_text = "本地规则命中：" + "、".join(local_flags)
    else:
        local_text = "本地规则命中：未发现明显高风险关键词"

    if ai_report:
        return local_text + "\n\n" + ai_report

    return local_text + "\n\nAI审核暂时失败，请人工快速检查标题、脚本和分镜中的具体公司、客户、数据、新闻和产品版本。"


# ============================================================
# 创建项目文件夹
# ============================================================

def create_project_folder(topic):

    now = datetime.now().strftime("%Y%m%d_%H%M")

    safe_topic = topic

    invalid_chars = [
        "/",
        "\\",
        ":",
        "*",
        "?",
        '"',
        "<",
        ">",
        "|"
    ]

    for char in invalid_chars:
        safe_topic = safe_topic.replace(
            char,
            "_"
        )

    folder_name = f"{safe_topic}_{now}"

    project_path = os.path.join(
        os.getcwd(),
        folder_name
    )

    os.makedirs(
        project_path,
        exist_ok=True
    )

    return project_path


# ============================================================
# 保存文件
# ============================================================

def save_text_file(
    project_path,
    filename,
    content
):

    file_path = os.path.join(
        project_path,
        filename
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)

    return file_path


# ============================================================
# 保存完整项目
# ============================================================

def save_project(
    project_path,
    selected_title,
    script_text,
    storyboard_text,
    visual_prompts,
    editing_plan,
    material_list,
    fact_report
):

    save_text_file(
        project_path,
        "01_标题.txt",
        selected_title
    )

    save_text_file(
        project_path,
        "02_口播脚本.txt",
        script_text
    )

    save_text_file(
        project_path,
        "03_分镜.txt",
        storyboard_text
    )

    save_text_file(
        project_path,
        "04_AI画面提示词.txt",
        visual_prompts
    )

    save_text_file(
        project_path,
        "05_剪映制作清单.txt",
        editing_plan
    )

    save_text_file(
        project_path,
        "06_视频素材清单.txt",
        material_list
    )

    save_text_file(
        project_path,
        "07_事实安全检查.txt",
        fact_report
    )

    full_plan = f"""
==============================
七分少年 AI短视频完整方案
==============================


【标题】

{selected_title}


【口播脚本】

{script_text}


【分镜】

{storyboard_text}


【AI画面提示词】

{visual_prompts}


【剪映制作清单】

{editing_plan}


【视频素材清单】

{material_list}
"""

    save_text_file(
        project_path,
        "08_完整方案.txt",
        full_plan
    )


# ============================================================
# 主程序
# ============================================================

def main():

    print_title(APP_NAME)

    # --------------------------------------------------------
    # 1. 视频类型
    # --------------------------------------------------------

    video_type = choose_video_type()

    # --------------------------------------------------------
    # 2. 主题
    # --------------------------------------------------------

    topic = get_topic()

    # --------------------------------------------------------
    # 3. 标题
    # --------------------------------------------------------

    titles = generate_titles(
        topic,
        video_type
    )

    selected_title = choose_title(
        titles,
        topic,
        video_type
    )

    if not selected_title:
        print("\n程序结束。")
        return

    # --------------------------------------------------------
    # 4. 脚本
    # --------------------------------------------------------

    script_text = confirm_script(
        topic,
        video_type,
        selected_title
    )

    if not script_text:
        print("\n程序结束。")
        return

    # --------------------------------------------------------
    # 5. 分镜管理
    # --------------------------------------------------------

    storyboard_text = manage_storyboard(
        selected_title,
        script_text
    )

    if not storyboard_text:
        print("\n程序结束。")
        return

    # --------------------------------------------------------
    # 6. AI画面提示词
    # --------------------------------------------------------

    visual_prompts = generate_visual_prompts(
        selected_title,
        storyboard_text
    )

    if not visual_prompts:
        print("\nAI画面提示词生成失败。")
        return

    # --------------------------------------------------------
    # 7. 剪映制作清单
    # --------------------------------------------------------

    editing_plan = generate_editing_plan(
        selected_title,
        script_text,
        storyboard_text
    )

    if not editing_plan:
        print("\n剪映制作清单生成失败。")
        return

    # --------------------------------------------------------
    # 8. 视频素材清单
    # --------------------------------------------------------

    material_list = generate_material_list(
        selected_title,
        script_text,
        storyboard_text
    )

    if not material_list:
        print("\n视频素材清单生成失败。")
        return

    # --------------------------------------------------------
    # 9. 事实安全检查
    # --------------------------------------------------------

    fact_report = fact_safety_check(
        selected_title,
        script_text,
        storyboard_text,
        material_list
    )

    print("\n" + fact_report)

    # --------------------------------------------------------
    # 10. 创建项目
    # --------------------------------------------------------

    project_path = create_project_folder(
        topic
    )

    # --------------------------------------------------------
    # 9. 保存
    # --------------------------------------------------------

    save_project(
        project_path,
        selected_title,
        script_text,
        storyboard_text,
        visual_prompts,
        editing_plan,
        material_list,
        fact_report
    )

    # --------------------------------------------------------
    # 10. 完成
    # --------------------------------------------------------

    print_title("项目生成完成")

    print("项目目录：")
    print(project_path)

    print("\n已生成：")

    print("01_标题.txt")
    print("02_口播脚本.txt")
    print("03_分镜.txt")
    print("04_AI画面提示词.txt")
    print("05_剪映制作清单.txt")
    print("06_视频素材清单.txt")
    print("07_事实安全检查.txt")
    print("08_完整方案.txt")

    print("\n下一步：")
    print("打开项目文件夹")
    print("按照剪映制作清单开始制作视频。")

    print_line()


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":
    main()