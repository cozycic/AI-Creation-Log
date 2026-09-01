topic = input("请输入视频主题：")
duration = input("请输入视频时长：")

print()
print("请选择视频风格：")
print("1. 故事型")
print("2. 干货型")
print("3. 情绪型")

style = input("请输入数字 1-3：")

print()
print("===== AI短视频文案 =====")
print("主题：" + topic)
print("时长：" + duration)

if style == "1":
    print()
    print("【故事型】")
    print("你有没有想过，" + topic + "背后，其实藏着一个普通人的机会？")
    print("故事往往就是从一个不起眼的决定开始的。")
    print("也许今天，就是你改变自己的开始。")

elif style == "2":
    print()
    print("【干货型】")
    print("关于" + topic + "，普通人首先要知道三件事。")
    print("第一，先了解它。")
    print("第二，找到适合自己的使用方法。")
    print("第三，坚持实践，而不是只停留在了解阶段。")

elif style == "3":
    print()
    print("【情绪型】")
    print("很多人都看到了" + topic + "的变化，")
    print("但真正焦虑的，是那些不知道下一步该怎么办的人。")
    print("如果你也不想被时代甩下，那么现在开始还不晚。")

else:
    print("你输入的风格编号不正确。")