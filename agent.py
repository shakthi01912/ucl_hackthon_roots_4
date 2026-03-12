from strands import Agent
from strands.models import BedrockModel
from tools.skill_extractor import extract_skills
from tools.role_matcher import match_roles
from tools.onet_matcher import match_onet_roles
from prompts.skill_prompt import SKILL_EXTRACTOR_PROMPT
from prompts.matcher_prompt import MATCHER_PROMPT

# System prompt for the agent
SYSTEM_PROMPT = f"""
You are a Career Advisor AI called "Career Roots" that helps UCL students 
understand how their modules connect to careers worldwide.

Your job:
1. Extract skills from a module description
2. Match those skills to UK Government DDaT roles (tech/digital careers)
3. Match those skills to O*NET occupations (universal global careers)
4. Explain why each role is a good career match

{SKILL_EXTRACTOR_PROMPT}

{MATCHER_PROMPT}

Always be helpful, specific, and encouraging to students.
Show BOTH UK government roles AND global career options.
"""

# Bedrock model
bedrock_model = BedrockModel(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region_name="eu-west-2"
)

# Create the agent with ALL tools
agent = Agent(
    model=bedrock_model,
    system_prompt=SYSTEM_PROMPT,
    tools=[extract_skills, match_roles, match_onet_roles]
)


def analyse_module(module_data: dict) -> str:
  
    prompt = f"""
    Analyse this UCL module for career matches:
    
    Module ID: {module_data.get('module_id', 'Unknown')}
    Module Name: {module_data.get('module_name', 'Unknown')}
    
    Description: 
    {module_data.get('module_description', '')}
    
    Please:
    1. Extract the key skills from this module
    2. Use match_roles tool for UK Government DDaT careers (tech/digital)
    3. Use match_onet_roles tool for universal global careers (all sectors)
    
    Return results as JSON format:
    {{
        "module_id": "...",
        "module_name": "...",
        "extracted_skills": ["skill1", "skill2", ...],
        "ddat_roles": [
            {{"role": "...", "match_percentage": 85, "matching_skills": ["...", "..."]}}
        ],
        "onet_roles": [
            {{"title": "...", "match_percentage": 72, "matching_skills": ["...", "..."]}}
        ]
    }}
    
    IMPORTANT: Include match_percentage for every role. Return ONLY valid JSON.
    """
    
    result = agent(prompt)
    return result


if __name__ == "__main__":
    test_module = {
        "module_id": "ANTH0232",
        "module_name": "Introduction to the Practice of Audio Storytelling for Radio and Podcast",
        "module_description": """
        This core module will run over term three, completing over the summer. 
        Students will independently make a feature-length audio work of duration 45-60 minutes. 
        This may be a single feature or a series of connected episodes. 
        It will involve a period of pre-production and research, the creation of a written proposal 
        and in-person pitch and finally the production of the audio work.
        
        Learning outcomes:
        - Devise and produce, using advanced narrative techniques, a feature length factual audio documentary
        - Writing a treatment for long-form audio and discuss ethical considerations
        - Comprehensive understanding of modes of creation and thinking about relations between form and content
        - Identify and deal with complex problems in media production workflows
        - Communicate ambitious concepts effectively and succinctly
        - Pitch and sell complex stories/product to potential clients
        - Use onward career skills (e.g. getting your work heard, design career roadmaps)
        
        Delivery: Seminars, Masterclasses, mentoring, independent study, group crits.
        Students will be allocated a mentor from the audio industry for one-to-one feedback.
        Masterclasses with visiting practitioners covering long-form production and career paths.
        """
    }
    
    print("Analysing module...")
    print("-" * 50)
    result = analyse_module(test_module)
    print(result)