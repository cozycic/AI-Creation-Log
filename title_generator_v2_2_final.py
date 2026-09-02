import os
from datetime import datetime

from openai import OpenAI


# ============================================================
# 基础配置
# ============================================================

APP_NAME = "七分少年 AI短视频生成器 V2.2"
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
    editing_plan
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
"""

    save_text_file(
        project_path,
        "06_完整方案.txt",
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
    # 8. 创建项目
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
        editing_plan
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
    print("06_完整方案.txt")

    print("\n下一步：")
    print("打开项目文件夹")
    print("按照剪映制作清单开始制作视频。")

    print_line()


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":
    main()