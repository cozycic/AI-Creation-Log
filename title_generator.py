import os
import re
from datetime import datetime
from openai import OpenAI


# ============================================================
# 七分少年 AI短视频生成器 V2
# ============================================================

APP_NAME = "七分少年 AI短视频生成器"
MODEL_NAME = "deepseek-v4-flash"
BASE_URL = "https://api.deepseek.com"


# ============================================================
# 1. 初始化 DeepSeek
# ============================================================

def create_client():
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        print()
        print("❌ 错误：没有找到 DEEPSEEK_API_KEY")
        print("请先配置 DeepSeek API Key。")
        print()
        exit()

    return OpenAI(
        api_key=api_key,
        base_url=BASE_URL
    )


client = create_client()


# ============================================================
# 2. 通用工具
# ============================================================

def print_line():
    print("=" * 60)


def print_title(title):
    print()
    print_line()
    print(f"        {title}")
    print_line()
    print()


def ask(prompt):
    return input(prompt).strip()


def call_ai(prompt):
    """
    统一调用 DeepSeek。
    以后如果更换模型，只需要修改这里。
    """
    try:
        response = client.responses.create(
            model=MODEL_NAME,
            input=prompt
        )

        result = response.output_text.strip()

        if not result:
            raise ValueError("AI没有返回内容。")

        return result

    except Exception as error:
        print()
        print("❌ AI调用失败")
        print(f"错误信息：{error}")
        print()
        exit()


# ============================================================
# 3. 输入视频类型
# ============================================================

def choose_video_type():

    print_title("选择视频类型")

    video_types = {
        "1": "AI创业",
        "2": "AI工具",
        "3": "AI知识",
        "4": "个人成长",
        "5": "故事分享"
    }

    for number, name in video_types.items():
        print(f"{number}. {name}")

    print()

    while True:
        choice = ask("请选择视频类型（1-5）：")

        if choice in video_types:
            selected_type = video_types[choice]

            print()
            print(f"✅ 已选择：{selected_type}")

            return selected_type

        print("❌ 输入错误，请输入 1-5。")


# ============================================================
# 4. 输入主题
# ============================================================

def get_topic():

    print()
    topic = ask("请输入视频主题：")

    if not topic:
        print("❌ 视频主题不能为空。")
        exit()

    return topic


# ============================================================
# 5. 生成标题
# ============================================================

def generate_titles(topic, video_type):

    print_title("正在生成10个短视频标题")

    prompt = f"""
你是一名专业的抖音短视频运营专家。

账号名称：
七分少年

账号定位：
AI创业、AI工具、普通人如何利用AI创造机会。

账号特点：
不露脸、AI配音、真实记录、拒绝夸大赚钱。

视频类型：
{video_type}

视频主题：
{topic}

请围绕这个主题生成10个适合抖音的短视频标题。

要求：
1. 普通人能看懂
2. 有吸引力，但不能标题党
3. 像真人说话
4. 不要虚假承诺赚钱
5. 每个标题30字以内
6. 结合视频类型
7. 只输出10个标题

格式：

1. 标题
2. 标题
3. 标题
4. 标题
5. 标题
6. 标题
7. 标题
8. 标题
9. 标题
10. 标题
"""

    titles_text = call_ai(prompt)

    titles = []

    for line in titles_text.splitlines():

        match = re.match(r"^\s*\d+[\.、]\s*(.+)", line)

        if match:
            title = match.group(1).strip()

            if title:
                titles.append(title)

    if not titles:
        print("❌ 没有成功提取标题，请重新运行程序。")
        exit()

    print()
    print("===== AI生成的10个标题 =====")
    print()

    for index, title in enumerate(titles, start=1):
        print(f"{index}. {title}")

    return titles


# ============================================================
# 6. 选择标题
# ============================================================

def choose_title(titles):

    print()

    while True:

        choice = ask(f"请选择一个标题（1-{len(titles)}）：")

        try:
            number = int(choice)
        except ValueError:
            print("❌ 请输入数字。")
            continue

        if 1 <= number <= len(titles):
            selected_title = titles[number - 1]

            print()
            print("===== 你选择的标题 =====")
            print()
            print(selected_title)

            return selected_title

        print(f"❌ 请输入1-{len(titles)}之间的数字。")


# ============================================================
# 7. 生成60秒口播脚本
# ============================================================

def generate_script(topic, video_type, selected_title):

    print_title("正在生成60秒口播脚本")

    prompt = f"""
你是一名专业的抖音短视频编剧。

账号：
七分少年

账号定位：
记录一个普通人学习AI、实践AI创业的真实过程。

视频类型：
{video_type}

视频主题：
{topic}

视频标题：
{selected_title}

请创作一条60秒左右的短视频口播脚本。

要求：
1. 前3秒抓住注意力
2. 内容具体，有真实价值
3. 像真人分享，不像AI作文
4. 不使用虚假赚钱承诺
5. 适合不露脸视频
6. 适合AI配音
7. 语言简单、自然、有口语感
8. 最后加入自然互动
9. 不写画面，只写口播

严格按照：

【开头3秒】
...

【正文】
...

【结尾】
...

【互动】
...
"""

    script_text = call_ai(prompt)

    print()
    print("===== AI生成的60秒短视频脚本 =====")
    print()
    print(script_text)

    return script_text


# ============================================================
# 8. 生成分镜
# ============================================================

def generate_storyboard(selected_title, script_text):

    print_title("正在生成短视频分镜")

    prompt = f"""
你是一名专业的抖音短视频导演。

账号：
七分少年

视频标题：
{selected_title}

视频口播稿：
{script_text}

请根据口播稿设计适合“不露脸、AI配音”的短视频分镜。

要求：
1. 总时长约60秒
2. 8-10个镜头
3. 每个镜头都能用普通素材、AI图片或AI视频完成
4. 不需要真人正脸
5. 每个镜头必须对应口播
6. 给出素材关键词
7. 给出字幕重点
8. 不设计复杂电影镜头

格式：

【镜头1】
时间：
口播：
画面：
素材关键词：
字幕：

【镜头2】
时间：
口播：
画面：
素材关键词：
字幕：

一直到最后一个镜头。
"""

    storyboard_text = call_ai(prompt)

    print()
    print("===== AI生成的短视频分镜 =====")
    print()
    print(storyboard_text)

    return storyboard_text


# ============================================================
# 9. 生成AI画面提示词
# ============================================================

def generate_visual_prompts(selected_title, storyboard_text):

    print_title("正在生成AI画面提示词")

    prompt = f"""
你是一名专业的AI短视频视觉导演。

账号：
七分少年

视频标题：
{selected_title}

视频分镜：
{storyboard_text}

请根据每一个镜头，为AI图片或AI视频生成工具制作中文画面提示词。

要求：
1. 每个镜头对应一个提示词
2. 竖屏9:16
3. 不需要真人正脸
4. 真实、自然、生活化
5. 适合抖音
6. 尽量使用现实生活场景
7. 不要复杂到难以生成
8. 不要出现Logo、水印
9. 尽量避免画面出现可读文字
10. 每个提示词100-150字左右

格式：

【镜头1】
AI画面提示词：
...

【镜头2】
AI画面提示词：
...

一直到最后一个镜头。
"""

    visual_text = call_ai(prompt)

    print()
    print("===== AI生成的画面提示词 =====")
    print()
    print(visual_text)

    return visual_text


# ============================================================
# 10. 生成剪映制作清单
# ============================================================

def generate_editing_plan(selected_title, script_text, storyboard_text):

    print_title("正在生成剪映制作清单")

    prompt = f"""
你是一名专业的抖音短视频剪辑师。

账号：
七分少年

视频标题：
{selected_title}

口播脚本：
{script_text}

原始分镜：
{storyboard_text}

请把这条视频整理成一份可以直接照着剪映制作的《剪映制作清单》。

要求：

1. 总时长约60秒
2. 按镜头逐个整理
3. 每个镜头必须包含：
   - 时间
   - 口播
   - 画面
   - 素材类型
   - 素材关键词
   - 屏幕字幕
   - 音效建议
   - 转场建议

4. 素材类型只能从以下几个选：
   实拍素材
   AI图片
   AI视频
   屏幕录制
   图片素材

5. 字幕要短，适合手机观看
6. 一屏字幕尽量不要超过12个字
7. 不需要复杂剪辑
8. 全部适合不露脸视频
9. 最后增加一份《整条视频剪辑建议》

严格按照：

========== 镜头1 ==========

时间：
口播：
画面：
素材类型：
素材关键词：
字幕：
音效：
转场：

========== 镜头2 ==========

时间：
口播：
画面：
素材类型：
素材关键词：
字幕：
音效：
转场：

一直到最后一个镜头。

最后：

========== 整条视频剪辑建议 ==========

配音：
BGM：
字幕：
节奏：
封面：
发布注意事项：
"""

    editing_text = call_ai(prompt)

    print()
    print("===== AI生成的剪映制作清单 =====")
    print()
    print(editing_text)

    return editing_text


# ============================================================
# 11. 创建项目文件夹
# ============================================================

def create_project_folder(topic):

    now = datetime.now()

    date_text = now.strftime("%Y%m%d_%H%M")

    safe_topic = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        topic
    )

    project_name = f"{safe_topic}_{date_text}"

    project_path = os.path.join(
        os.getcwd(),
        project_name
    )

    os.makedirs(
        project_path,
        exist_ok=True
    )

    return project_path, now


# ============================================================
# 12. 保存文件
# ============================================================

def save_text_file(project_path, filename, content):

    file_path = os.path.join(
        project_path,
        filename
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)

    return file_path


# ============================================================
# 13. 保存整个项目
# ============================================================

def save_project(
    project_path,
    now,
    topic,
    video_type,
    titles_text,
    selected_title,
    script_text,
    storyboard_text,
    visual_text,
    editing_text
):

    # 01 标题
    save_text_file(
        project_path,
        "01_标题.txt",
        f"""视频主题：{topic}

视频类型：{video_type}

10个AI生成标题：

{titles_text}

你选择的标题：

{selected_title}
"""
    )

    # 02 口播脚本
    save_text_file(
        project_path,
        "02_口播脚本.txt",
        f"""视频主题：{topic}

视频类型：{video_type}

视频标题：
{selected_title}

{script_text}
"""
    )

    # 03 分镜
    save_text_file(
        project_path,
        "03_分镜.txt",
        f"""视频主题：{topic}

视频标题：
{selected_title}

{storyboard_text}
"""
    )

    # 04 AI画面提示词
    save_text_file(
        project_path,
        "04_AI画面提示词.txt",
        f"""视频主题：{topic}

视频标题：
{selected_title}

{visual_text}
"""
    )

    # 05 剪映制作清单
    save_text_file(
        project_path,
        "05_剪映制作清单.txt",
        f"""视频主题：{topic}

视频标题：
{selected_title}

{editing_text}
"""
    )

    # 06 完整方案
    full_content = f"""
============================================
        七分少年 AI短视频方案 V2
============================================

生成时间：
{now.strftime("%Y-%m-%d %H:%M:%S")}

视频类型：
{video_type}

视频主题：
{topic}

============================================
10个AI生成标题
============================================

{titles_text}

============================================
最终选择标题
============================================

{selected_title}

============================================
60秒口播脚本
============================================

{script_text}

============================================
短视频分镜
============================================

{storyboard_text}

============================================
AI画面提示词
============================================

{visual_text}

============================================
剪映制作清单
============================================

{editing_text}

============================================
        AI短视频生产完成
============================================
"""

    save_text_file(
        project_path,
        "06_完整方案.txt",
        full_content
    )


# ============================================================
# 14. 主程序
# ============================================================

def main():

    print()
    print_line()
    print(f"        {APP_NAME} V2")
    print_line()

    print()
    print("让AI帮你完成：")
    print("标题 → 脚本 → 分镜 → 画面 → 剪映")
    print()

    # 选择视频类型
    video_type = choose_video_type()

    # 输入主题
    topic = get_topic()

    print()
    print("开始生成视频方案...")
    print()

    # 生成标题
    titles = generate_titles(
        topic,
        video_type
    )

    titles_text = "\n".join(
        f"{index}. {title}"
        for index, title in enumerate(titles, start=1)
    )

    # 选择标题
    selected_title = choose_title(titles)

    # 生成脚本
    script_text = generate_script(
        topic,
        video_type,
        selected_title
    )

    # 生成分镜
    storyboard_text = generate_storyboard(
        selected_title,
        script_text
    )

    # 生成画面提示词
    visual_text = generate_visual_prompts(
        selected_title,
        storyboard_text
    )

    # 生成剪映清单
    editing_text = generate_editing_plan(
        selected_title,
        script_text,
        storyboard_text
    )

    # 创建项目
    project_path, now = create_project_folder(topic)

    # 保存项目
    save_project(
        project_path,
        now,
        topic,
        video_type,
        titles_text,
        selected_title,
        script_text,
        storyboard_text,
        visual_text,
        editing_text
    )

    # 最终结果
    print()
    print_line()
    print("        🎉 AI短视频生产完成")
    print_line()

    print()
    print("项目文件夹：")
    print(project_path)

    print()
    print("已生成文件：")

    files = [
        "01_标题.txt",
        "02_口播脚本.txt",
        "03_分镜.txt",
        "04_AI画面提示词.txt",
        "05_剪映制作清单.txt",
        "06_完整方案.txt"
    ]

    for filename in files:
        print(f"✅ {filename}")

    print()
    print_line()


# ============================================================
# 15. 程序入口
# ============================================================

if __name__ == "__main__":
    main()