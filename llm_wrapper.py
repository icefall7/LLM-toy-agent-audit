import os
from typing import Dict, Any
import openai
from openai import OpenAI


class LLMWrapper:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def analyze_differences(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> str:
        """
        Analyze differences between two profiles using LLM.
        """
        prompt = f"""
        You are an expert data auditor. Compare these two user profiles and identify any differences, 
        potential data quality issues, or inconsistencies. Provide a detailed analysis.
        
        Profile 1: {profile1}
        Profile 2: {profile2}
        
        Please analyze:
        1. Are these profiles likely referring to the same person?
        2. What specific differences exist between the profiles?
        3. Are there any formatting inconsistencies?
        4. Which version of each field appears more standardized?
        5. Provide recommendations for data standardization if needed.
        
        Format your response as a structured audit report.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # You can adjust the model as needed
                messages=[
                    {"role": "system", "content": "You are a precise data auditing assistant that analyzes user profile data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1  # Low temperature for more consistent outputs
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during LLM analysis: {str(e)}" 