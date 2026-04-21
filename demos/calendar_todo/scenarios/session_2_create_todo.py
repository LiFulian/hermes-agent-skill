"""场景2：创建待办任务 - AI使用记忆中的偏好"""

SESSION_2_CONVERSATION = """
用户：我需要添加几个待办事项

AI助手：好的，我看到你使用Google日历，要同步到日历吗？
根据你之前的偏好，我会为待办设置提醒。

用户：好的。第一个是完成项目文档，截止日期是周五

AI助手：已创建待办：
✅ 任务：完成项目文档
📅 截止：周五
⏰ 提醒：提前1天（根据你的偏好调整）

还有什么需要添加的？

用户：第二个是准备产品演示，下周三之前完成

AI助手：已创建：
✅ 任务：准备产品演示
📅 截止：下周三
⏰ 提醒：提前30分钟（默认偏好）

用户：好的，我通常在下午处理文档工作

AI助手：好的，我记下了。以后会尽量在下午安排文档类任务。
"""

EXPECTED_MEMORY_UPDATES = {
    "user_md": [
        "提醒偏好更新：重要事项提前1天",
        "下午处理文档工作",
    ],
    "memory_md": [
        "待办与Google日历集成",
        "产品演示任务",
    ]
}

def get_conversation():
    return SESSION_2_CONVERSATION

def get_expected_updates():
    return EXPECTED_MEMORY_UPDATES
