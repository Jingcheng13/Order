from pathlib import Path

import yaml


def get_skills_list():
    """获取技能列表"""

    skills_dir = Path(__file__).parent.parent.parent / 'agent' / 'skills'

    skills_list = ''

    # 只匹配 skills_dir 的直接子文件夹里的 skill.md
    skill_files = [
        f for f in skills_dir.glob("*/*.md")
        if f.name.lower() == "skill.md"
    ]

    for file in skill_files:
        content = file.read_text(encoding="utf-8")
        parts = content.split("---")
        if len(parts) >= 2:
            metadata = yaml.safe_load(parts[1])
            skills_list += \
f'''  <skill>
    <name>{metadata["name"]}</name>
    <description>{metadata["description"]}</description>
    <location>{file}</location>
  </skill>
'''

    
    return \
f'''<available_skills>
{skills_list}
</available_skills>
'''

if __name__ == '__main__':
    from rich.markdown import Markdown
    from rich import print
    print(Markdown(f'```\n{get_skills_list()}\n```'))
