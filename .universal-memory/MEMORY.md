# Agent Memory

## Project Context
- 项目名称：Universal Memory Skill
- 功能：跨会话记忆系统，支持Claude/Cursor/Trae等AI工具
- 已完成：skills/ scripts/ cli/ tests/ demos/
- 待完善：简化文档，优化示例

## 技术决策
- 使用Markdown存储记忆（通用性）
- MEMORY.md存储Agent知识（限制2200字符）
- USER.md存储用户偏好（限制1500字符）
- 记忆按类型分类：偏好/项目/模式/事实

## 已知问题
- 中文提取模式需要优化
- Demo示例需要更真实

## 测试验证
- 基础记忆提取：✅ 工作正常
- 跨会话保持：✅ 工作正常
- CLI工具：✅ 工作正常
- pytest测试：✅ 71个测试通过

## 改进方向
- 进一步简化README
- 优化中文提取准确性
- 增强示例的实用性
