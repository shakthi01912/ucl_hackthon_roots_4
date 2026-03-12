from strands import tool
from prompts.skill_prompt import SKILL_EXTRACTOR_PROMPT


@tool
def extract_skills(module_name: str, module_description: str) -> dict:
    
    return {
        "module_name": module_name,
        "description": module_description,
        "prompt": SKILL_EXTRACTOR_PROMPT
    }