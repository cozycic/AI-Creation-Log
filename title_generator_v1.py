import os
import re
from datetime import datetime
from openai import OpenAI

# =========================
# DeepSeek API
# =========================

api_key = os.environ.get("DEEPSEEK_API_KEY")

if not api_key:
    print("错误：没有找到 DEEPSEEK_API_KEY")
    print("请先配置 DeepSeek API Key。")
    exit()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)


# =========================
# 1. 输入主题
# =========================

topic = input("请输入视频主题：").strip()

if not topic:
    print("主题不能为空。")
    exit()


# =========================
# 2. 生成10个标题
# =========================

title_prompt = f"""
你是一名专业的抖音短视频运营专家。

账号名称：
七分少年

账号定位：
AI创业、AI工具、普通人如何利用AI创造机会。

账号特点：
不露脸、AI配音、真实记录、拒绝夸大赚钱。

请围绕「{topic}」生成10个适合抖音的短视频标题。

要求：
1. 普通人能看懂
2. 有吸引力，但不能标题党
3. 像真人说话
4. 不要虚假承诺赚钱
5. 每个标题30字以内
6. 只输出10个标题

格式：
1. 标题
2. 标题
3. 标题
"""

title_response = client.responses.create(
    model="deepseek-v4-flash",
    input=title_prompt
)

titles_text = title_response.output_text.strip()

print()
print("===== DeepSeek生成的10个标题 =====")
print()
print(titles_text)


# =========================
# 3. 提取标题
# =========================

titles = []

for line in titles_text.splitlines():
    match = re.match(r"^\s*\d+[\.、]\s*(.+)", line)

    if match:
        title = match.group(1).strip()
        titles.append(title)

if len(titles) == 0:
    print("没有成功提取标题，请重新运行程序。")
    exit()


# =========================
# 4. 选择标题
# =========================

choice = input("\n请选择一个标题（1-10）：").strip()

try:
    choice_number = int(choice)
except ValueError:
    print("请输入数字，例如：5")
    exit()

if choice_number < 1 or choice_number > len(titles):
    print(f"请输入1-{len(titles)}之间的数字。")
    exit()

selected_title = titles[choice_number - 1]

print()
print("===== 你选择的标题 =====")
print()
print(selected_title)


# =========================
# 5. 生成60秒口播脚本
# =========================

script_prompt = f"""
你是一名专业的抖音短视频编剧。

账号名称：
七分少年

账号定位：
记录一个普通人学习AI、实践AI创业的真实过程。

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

script_response = client.responses.create(
    model="deepseek-v4-flash",
    input=script_prompt
)

script_text = script_response.output_text.strip()

print()
print("===== AI生成的60秒短视频脚本 =====")
print()
print(script_text)


# =========================
# 6. 生成短视频分镜
# =========================

storyboard_prompt = f"""
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

storyboard_response = client.responses.create(
    model="deepseek-v4-flash",
    input=storyboard_prompt
)

storyboard_text = storyboard_response.output_text.strip()

print()
print("===== AI生成的短视频分镜 =====")
print()
print(storyboard_text)


# =========================
# 7. 生成AI画面提示词
# =========================

visual_prompt = f"""
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

visual_response = client.responses.create(
    model="deepseek-v4-flash",
    input=visual_prompt
)

visual_text = visual_response.output_text.strip()

print()
print("===== AI生成的画面提示词 =====")
print()
print(visual_text)


# =========================
# 8. 创建项目文件夹
# =========================

now = datetime.now()

date_text = now.strftime("%Y%m%d_%H%M")

safe_topic = re.sub(
    r'[\\/:*?"<>|]',
    '_',
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


# =========================
# 9. 保存标题
# =========================

title_path = os.path.join(
    project_path,
    "01_标题.txt"
)

with open(
    title_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(
        f"视频主题：{topic}\n\n"
        f"10个AI生成标题：\n\n"
        f"{titles_text}\n\n"
        f"你选择的标题：\n\n"
        f"{selected_title}\n"
    )


# =========================
# 10. 保存口播脚本
# =========================

script_path = os.path.join(
    project_path,
    "02_口播脚本.txt"
)

with open(
    script_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(
        f"视频主题：{topic}\n\n"
        f"视频标题：{selected_title}\n\n"
        f"{script_text}\n"
    )


# =========================
# 11. 保存分镜
# =========================

storyboard_path = os.path.join(
    project_path,
    "03_分镜.txt"
)

with open(
    storyboard_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(
        f"视频主题：{topic}\n\n"
        f"视频标题：{selected_title}\n\n"
        f"{storyboard_text}\n"
    )


# =========================
# 12. 保存AI画面提示词
# =========================

visual_path = os.path.join(
    project_path,
    "04_AI画面提示词.txt"
)

with open(
    visual_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(
        f"视频主题：{topic}\n\n"
        f"视频标题：{selected_title}\n\n"
        f"{visual_text}\n"
    )


# =========================
# 13. 保存完整方案
# =========================

full_path = os.path.join(
    project_path,
    "05_完整方案.txt"
)

full_content = f"""
==============================
        七分少年 AI短视频方案
==============================

生成时间：
{now.strftime("%Y-%m-%d %H:%M:%S")}

===== 视频主题 =====

{topic}

===== 10个AI生成标题 =====

{titles_text}

===== 你选择的标题 =====

{selected_title}

===== 60秒口播脚本 =====

{script_text}

===== 短视频分镜 =====

{storyboard_text}

===== AI画面提示词 =====

{visual_text}

==============================
        AI短视频生产完成
==============================
"""

with open(
    full_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(full_content)


# =========================
# 14. 生成剪映制作清单
# =========================

editing_prompt = f"""
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

editing_response = client.responses.create(
    model="deepseek-v4-flash",
    input=editing_prompt
)

editing_text = editing_response.output_text.strip()

print()
print("===== AI生成的剪映制作清单 =====")
print()
print(editing_text)


# =========================
# 15. 保存剪映制作清单
# =========================

editing_path = os.path.join(
    project_path,
    "06_剪映制作清单.txt"
)

with open(
    editing_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(
        f"视频主题：{topic}\n\n"
        f"视频标题：{selected_title}\n\n"
        f"{editing_text}\n"
    )


# =========================
# 16. 更新完整方案
# =========================

full_content = f"""
==============================
        七分少年 AI短视频方案
==============================

生成时间：
{now.strftime("%Y-%m-%d %H:%M:%S")}

===== 视频主题 =====

{topic}

===== 10个AI生成标题 =====

{titles_text}

===== 你选择的标题 =====

{selected_title}

===== 60秒口播脚本 =====

{script_text}

===== 短视频分镜 =====

{storyboard_text}

===== AI画面提示词 =====

{visual_text}

===== 剪映制作清单 =====

{editing_text}

==============================
        AI短视频生产完成
==============================
"""

with open(
    full_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(full_content)


# =========================
# 17. 最终结果
# =========================

print()
print("================================")
print("        AI短视频生产完成")
print("================================")
print()

print("项目文件夹：")
print(project_path)

print()
print("已生成文件：")
print("01_标题.txt")
print("02_口播脚本.txt")
print("03_分镜.txt")
print("04_AI画面提示词.txt")
print("05_完整方案.txt")
print("06_剪映制作清单.txt")

print()
print("================================")

print()
print("================================")
print("        AI短视频生产完成")
print("================================")
print()

print("项目文件夹：")
print(project_path)

print()
print("已生成文件：")
print("01_标题.txt")
print("02_口播脚本.txt")
print("03_分镜.txt")
print("04_AI画面提示词.txt")
print("05_完整方案.txt")

print()
print("================================")