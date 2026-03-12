import pandas as pd
from strands import tool


@tool
def match_roles(skills: list) -> list:
   
    df = pd.read_csv("ddat_data/roles.csv")
    

    roles = df["Role"].unique()
    
    matches = []
    
    for role in roles:
        # Get skills for this role
        role_data = df[df["Role"] == role]
        role_skills = role_data["Skill Name"].unique().tolist()
        role_family = role_data["Role Family"].iloc[0]
        role_description = role_data["Role Description"].iloc[0]
        
        # Calculate match - how many input skills match role skills
        input_skills_lower = [s.lower() for s in skills]
        role_skills_lower = [s.lower() for s in role_skills]
        
        matching_skills = []
        for skill in input_skills_lower:
            for role_skill in role_skills_lower:
                if skill in role_skill or role_skill in skill:
                    matching_skills.append(role_skill)
        
        # Calculate percentage
        if len(role_skills) > 0:
            match_pct = (len(matching_skills) / len(role_skills)) * 100
        else:
            match_pct = 0
        
        if match_pct > 0:
            matches.append({
                "role": role,
                "role_family": role_family,
                "role_description": role_description[:200] + "...",
                "match_percentage": round(match_pct, 1),
                "matching_skills": list(set(matching_skills)),
                "total_role_skills": len(role_skills)
            })
    
    # Sort by match percentage (highest first)
    matches.sort(key=lambda x: x["match_percentage"], reverse=True)
    
    # Return top 5 matches
    return matches[:5]