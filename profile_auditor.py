from typing import Dict, Any, Tuple
from llm_wrapper import LLMWrapper

class ProfileAuditor:
    def __init__(self):
        self.llm = LLMWrapper()
        
    def compare_profiles(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare two user profiles and return audit results.
        """
        # Basic validation
        if profile1.get('user_id') != profile2.get('user_id'):
            return {"error": "Profiles have different user IDs"}
            
        # Get LLM analysis
        llm_analysis = self.llm.analyze_differences(profile1, profile2)
        
        # Perform programmatic comparison
        differences = self._find_differences(profile1, profile2)
        
        return {
            "llm_analysis": llm_analysis,
            "programmatic_differences": differences,
            "profiles_compared": {
                "profile1": profile1,
                "profile2": profile2
            }
        }
    
    def _find_differences(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> Dict[str, Tuple[Any, Any]]:
        """
        Programmatically find differences between profiles.
        """
        differences = {}
        all_keys = set(profile1.keys()) | set(profile2.keys())
        
        for key in all_keys:
            val1 = profile1.get(key)
            val2 = profile2.get(key)
            
            if val1 != val2:
                differences[key] = (val1, val2)
                
        return differences 