from pathlib import Path


def get_skills_list():
    """获取技能列表（每次调用时重新计算路径、读取技能）"""
    skills_dir = Path(__file__).parent.parent.parent / 'agent/skills'
    
    return f'''
# 技能列表

重要：当需要技能时，请读取技能获取详细内容。

技能目录：{skills_dir}

name: web-design-engineer
description: |
  使用 HTML/CSS/JavaScript/React 构建高质量的视觉化 Web 制品——网页、着陆页、仪表盘、可交互原型、HTML 幻灯片、动画演示、UI 线框图、数据可视化等。
  当用户的需求涉及视觉、交互或前端交付物时，启用此技能，包括：
  - 创建网页、着陆页、仪表盘、营销页面
  - 构建可交互原型或 UI 线框图（含设备外框）
  - 构建 HTML 幻灯片 / 演示文稿
  - 创建 CSS/JS 动画或基于时间轴的动画演示
  - 将设计稿、截图或 PRD 转化为可交互的实现
  - 数据可视化（Chart.js / D3 等）
  - 设计系统 / UI 套件探索
  即使用户没有明确说"HTML"或"网页"，只要意图是产出视觉化、可交互或用于展示的内容，此技能即适用。
  不适用场景：纯后端逻辑、CLI 工具、数据处理脚本、无视觉要求的代码任务、命令行调试。
'''