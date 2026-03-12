import pandas as pd
from strands import tool


@tool
def match_onet_roles(skills: list) -> list:

    df = pd.read_csv("ddat_data/onet_occupations.csv", sep="\t")
    
    matches = []
    
    for _, row in df.iterrows():
        title = row["Title"]
        description = row["Description"].lower()
      
        matching_skills = []
        for skill in skills:
            if skill.lower() in description:
                matching_skills.append(skill)
        
        if len(matching_skills) > 0:
            match_pct = (len(matching_skills) / len(skills)) * 100
            matches.append({
                "code": row["O*NET-SOC Code"],
                "title": title,
                "description": row["Description"][:200] + "...",
                "match_percentage": round(match_pct, 1),
                "matching_skills": matching_skills
            })
    
  
    matches.sort(key=lambda x: x["match_percentage"], reverse=True)
    
    return matches[:5]