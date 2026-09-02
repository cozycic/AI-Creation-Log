import os
from datetime import datetime

from openai import OpenAI


# =========================
# 基础配置
# =========================

APP_NAME = "七分少年 AI短视频生成器 V2.1"
MODEL_NAME = "deepseek-v4-flash"
BASE_URL = "https://api.deepseek.com"


# =========================
# AI客户端
# =========================

def create_client():
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        print("\n错误：没有找到 DEEPSEEK_API_KEY")
        print("请先配置 DeepSeek API Key。")
        raise SystemExit(1)

    return OpenAI(
        api_key=api_key,
        base_url=BASE_URL
    )


client = create_client()


# =========================
# 界面工具
# =========================

def print_line():
    print("=" * 70)


def print_title(title):
    print_line()
    print(title)
    print_line()


def ask(prompt):
    return input(prompt).strip()


# =========================
# AI调用
# =========================

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


# =========================
# 视频类型
# =========================

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


# =========================
# 获取主题
# =========================

def get_topic():
    while True:
        topic = ask("\n请输入视频主题：")

        if topic:
            return topic

        print("主题不能为空，请重新输入。")


# =========================
# 标题生成
# =========================

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
10. 必须严格输出10个标题

请严格按照以下格式输出：

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

        # 去掉常见编号
        if "." in line[:4]:
            line = line.split(".", 1)[1].strip()

        elif "、" in line[:4]:
            line = line.split("、", 1)[1].strip()

        if line:
            titles.append(line)

    return titles[:10]


# =========================
# 选择标题
# =========================

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
            titles = generate_titles(topic, video_type)
            continue

        if choice == "q":
            return None

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(titles):
                selected = titles[number - 1]

                print("\n你选择的标题：")
                print(selected)

                confirm = ask("\n使用这个标题？（Y=使用 / R=重新选）：").lower()

                if confirm == "y":
                    return selected

                if confirm == "r":
                    continue

        print("输入错误，请重新选择。")


# =========================
# 生成口播脚本
# =========================

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
10. 只输出口播正文，不要解释

请直接输出脚本。
"""

    return call_ai(prompt)


# =========================
# 脚本确认
# =========================

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


# =========================
# 分镜
# =========================

def generate_storyboard(selected_title, script_text):
    print_title("正在生成10镜头分镜")

    prompt = f"""
你是一名抖音短视频导演。

根据下面的标题和口播脚本，设计10个镜头。

标题：
{selected_title}

口播脚本：
{script_text}

请严格按照以下格式：

镜头1：
画面：
旁白：

镜头2：
画面：
旁白：

一直到镜头10。

要求：

1. 适合60秒短视频
2. 每个镜头约5-7秒
3. 画面具体
4. 尽量使用普通人容易获得的素材
5. 可以使用AI生成画面
6. 不需要真人露脸
"""

    return call_ai(prompt)


# =========================
# AI画面提示词
# =========================

def generate_visual_prompts(selected_title, storyboard_text):
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
4. 适合AI图片/视频生成
5. 画面具有短视频感
6. 不要求真人露脸
7. 保持整条视频视觉风格统一

格式：

镜头1：
提示词：

镜头2：
提示词：

一直到镜头10。
"""

    return call_ai(prompt)


# =========================
# 剪映制作清单
# =========================

def generate_editing_plan(selected_title, script_text, storyboard_text):
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


# =========================
# 创建项目文件夹
# =========================

def create_project_folder(topic):
    now = datetime.now().strftime("%Y%m%d_%H%M")

    safe_topic = topic.replace("/", "_")
    safe_topic = safe_topic.replace("\\", "_")
    safe_topic = safe_topic.replace(":", "_")
    safe_topic = safe_topic.replace("*", "_")
    safe_topic = safe_topic.replace("?", "_")
    safe_topic = safe_topic.replace('"', "_")
    safe_topic = safe_topic.replace("<", "_")
    safe_topic = safe_topic.replace(">", "_")
    safe_topic = safe_topic.replace("|", "_")

    folder_name = f"{safe_topic}_{now}"

    project_path = os.path.join(
        os.getcwd(),
        folder_name
    )

    os.makedirs(project_path, exist_ok=True)

    return project_path


# =========================
# 保存文件
# =========================

def save_text_file(project_path, filename, content):
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


# =========================
# 保存完整项目
# =========================

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


# =========================
# 主程序
# =========================

def main():
    print_title(APP_NAME)

    video_type = choose_video_type()

    topic = get_topic()

    # =====================
    # 标题阶段
    # =====================

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

    # =====================
    # 脚本阶段
    # =====================

    script_text = confirm_script(
        topic,
        video_type,
        selected_title
    )

    if not script_text:
        print("\n程序结束。")
        return

    # =====================
    # 分镜阶段
    # =====================

    storyboard_text = generate_storyboard(
        selected_title,
        script_text
    )

    if not storyboard_text:
        print("\n分镜生成失败，程序结束。")
        return

    # =====================
    # AI画面阶段
    # =====================

    visual_prompts = generate_visual_prompts(
        selected_title,
        storyboard_text
    )

    if not visual_prompts:
        print("\nAI画面提示词生成失败，程序结束。")
        return

    # =====================
    # 剪映阶段
    # =====================

    editing_plan = generate_editing_plan(
        selected_title,
        script_text,
        storyboard_text
    )

    if not editing_plan:
        print("\n剪映制作清单生成失败，程序结束。")
        return

    # =====================
    # 保存
    # =====================

    project_path = create_project_folder(topic)

    save_project(
        project_path,
        selected_title,
        script_text,
        storyboard_text,
        visual_prompts,
        editing_plan
    )

    # =====================
    # 完成
    # =====================

    print_title("项目生成完成")

    print(f"项目目录：")
    print(project_path)

    print("\n已生成：")

    print("01_标题.txt")
    print("02_口播脚本.txt")
    print("03_分镜.txt")
    print("04_AI画面提示词.txt")
    print("05_剪映制作清单.txt")
    print("06_完整方案.txt")

    print("\n下一步：")
    print("打开项目文件夹 → 按照剪映制作清单开始剪视频。")

    print_line()


# =========================
# 程序入口
# =========================

if __name__ == "__main__":
    main()