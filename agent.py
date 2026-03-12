from strands import Agent
from tools.skill_extractor import extract_skills
from tools.role_matcher import match_roles
from prompts.skill_prompt import SKILL_EXTRACTOR_PROMPT
from prompts.matcher_prompt import MATCHER_PROMPT
from strands.models import BedrockModel

# System prompt for the agent
SYSTEM_PROMPT = f"""
You are a Career Advisor AI called "Career Roots" that helps UCL students 
understand how their modules connect to UK Government Digital & Data careers.

Your job:
1. Extract skills from a module description
2. Match those skills to DDaT framework job roles
3. Explain why each role is a good career match

{SKILL_EXTRACTOR_PROMPT}

{MATCHER_PROMPT}

Always be helpful, specific, and encouraging to students.
"""

# Create the agent with tools
from strands.models import BedrockModel


# Bedrock model
bedrock_model = BedrockModel(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region_name="eu-west-2"
)

# Create the agent with tools
agent = Agent(
    model=bedrock_model,
    system_prompt=SYSTEM_PROMPT,
    tools=[extract_skills, match_roles]
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
    2. Use the match_roles tool to find matching DDaT careers
    3. Explain why each career is a good match for students taking this module
    """
    
    result = agent(prompt)
    return result


if __name__ == "__main__":
    test_module = {
        "module_id": "COMP0261",
        "module_name": "AI for Knowledge Management and Education",
        "module_description": """
        Introduce students to different components related to building 
        AI-enabled knowledge intensive and educational applications.
        Fundamental techniques within developing content representations 
        and personalisation models, used to create user models for 
        educational/informational resources and facilitate learning pathways.
        Building reliable, robust and pedagogically sound intelligent systems 
        that can be used in education and information delivery.
        Topics include: Content Understanding and Representation, 
        Search and Recommendation Systems, Content Personalisation,
        Knowledge-aware and Educational Recommender Systems,
        Intelligent User Interfaces for Knowledge Management,
        Personalised Learning Systems.
        """
    }
    
    print("Analysing module...")
    print("-" * 50)
    result = analyse_module(test_module)
    print(result)