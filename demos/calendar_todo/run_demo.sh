#!/bin/bash

echo "============================================="
echo "Universal Memory Skill - 日历待办Demo"
echo "============================================="

# 设置路径
cd "$(dirname "$0")/../.."
export PYTHONPATH=.

# 运行Demo
echo ""
echo "运行Demo..."
python3 demos/calendar_todo/demo_runner.py

# 运行测试
echo ""
echo "运行测试验证..."
pytest demos/calendar_todo/test_demo.py -v

echo ""
echo "============================================="
echo "Demo完成！"
echo "============================================="
