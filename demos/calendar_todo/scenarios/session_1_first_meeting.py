"""场景1：首次创建会议 - 建立用户偏好"""

SESSION_1_CONVERSATION = """
用户：帮我创建一个会议，下周一上午10点和产品团队开会讨论Q2规划

AI助手：好的，我为你创建了以下日程：
📅 会议：产品团队Q2规划会议
🕐 时间：下周一 10:00-11:00
👥 参与人：产品团队
📝 主题：Q2规划讨论

我注意到这是你第一次创建会议，请问：
1. 你需要设置提醒吗？
2. 你通常使用哪个日历系统？

用户：是的，提前30分钟提醒我，我通常用Google日历

AI助手：好的，已设置：
⏰ 提醒：提前30分钟
📆 同步到：Google日历

我记下了你的偏好，以后创建日程会自动应用这些设置。
"""

EXPECTED_MEMORY_UPDATES = {
    "user_md": [
        "使用Google日历",
        "偏好工作日上午安排会议",
        "提醒偏好：提前30分钟",
    ],
    "memory_md": [
        "产品团队成员",
        "Q2规划项目",
    ]
}

def get_conversation():
    return SESSION_1_CONVERSATION

def get_expected_updates():
    return EXPECTED_MEMORY_UPDATES
