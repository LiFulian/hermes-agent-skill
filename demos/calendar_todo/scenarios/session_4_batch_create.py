"""场景4：批量创建一周日程 - AI主动应用记忆"""

SESSION_4_CONVERSATION = """
用户：帮我把下周的日程排一下

AI助手：根据你的习惯和已有安排，我建议：

📅 下周日程安排：
周一：
- 10:00-11:00 产品团队Q2规划会议
- 15:00-16:00 每周例会（提醒：提前2小时）

周二到周四：
- 上午：项目工作时间（你的偏好）
- 下午：会议和协作时间

周五：
- 下午：周报编写和发送（提醒：提前1天准备）

需要调整吗？

用户：很好，另外加上周三下午的产品评审，还有周四的技术分享

AI助手：已添加：
✅ 周三下午：产品评审
✅ 周四下午：技术分享

完整日程已同步到Google日历，所有提醒已按你的偏好设置。
"""

EXPECTED_MEMORY_UPDATES = {
    "user_md": [
        "上午：项目工作时间",
        "下午：会议和协作时间",
    ],
    "memory_md": [
        "周三下午：产品评审",
        "周四下午：技术分享",
        "AI能主动推荐日程安排",
    ]
}

def get_conversation():
    return SESSION_4_CONVERSATION

def get_expected_updates():
    return EXPECTED_MEMORY_UPDATES
