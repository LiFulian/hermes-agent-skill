"""场景3：重复提醒设置 - 发现定期模式"""

SESSION_3_CONVERSATION = """
用户：帮我设置一个每周例会，每周一下午3点，提醒我准备周报

AI助手：好的，我已创建重复日程：
🔄 每周例会
📅 时间：每周一 15:00
⏰ 提醒：提前2小时

我注意到你偏好提前准备，这样安排可以吗？

用户：好的。还有，我每周五下午要发周报给团队

AI助手：已记录：
📝 每周五下午：发送周报给产品团队

你的周报流程已设置：
1. 周一例会收集信息
2. 周五下午编写并发送
"""

EXPECTED_MEMORY_UPDATES = {
    "user_md": [
        "周报提醒：提前2小时",
    ],
    "memory_md": [
        "每周一下午3点例会",
        "周五下午发周报给团队",
        "周报流程：周一收集→周五发送",
    ]
}

def get_conversation():
    return SESSION_3_CONVERSATION

def get_expected_updates():
    return EXPECTED_MEMORY_UPDATES
