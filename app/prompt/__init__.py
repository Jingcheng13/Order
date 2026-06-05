from pathlib import Path
import sys
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

def get_system_prompt():
    workspace_dir = Path(__file__).parent.parent.parent / 'agent/workspace'
    skills_dir = Path(__file__).parent.parent.parent / 'agent/skills'
    platform = sys.platform
    prompt = Path(__file__).parent / 'system.md'
    return prompt.read_text(encoding='utf-8').format_map(locals())


summary_prompt = Path(__file__).parent / 'summary.md'
summary_prompt = summary_prompt.read_text(encoding='utf-8')
system_prompt = get_system_prompt()
skills_list = get_skills_list()


__all__ = [
    'system_prompt',
    'summary_prompt',
    'skills_list',
]

if __name__ == '__main__':
    print(system_prompt)
    print(skills_list)
    print(summary_prompt)