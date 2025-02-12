from typing import Dict, Any, Tuple
from rich.console import Console
from rich.prompt import Prompt
from rich import print as rprint
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os
from database.db_manager import DatabaseManager

class InteractiveAuditService:
    def __init__(self, model_name="gpt-4"):
        self.console = Console()
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.1,
            streaming=True
        )
        self.db_manager = DatabaseManager()
        
    def get_user_id_input(self) -> int:
        """Get user ID input"""
        while True:
            try:
                user_id = int(Prompt.ask("\n[bold blue]Enter User ID to audit[/bold blue]"))
                return user_id
            except ValueError:
                self.console.print("[red]Invalid user ID. Please enter a number.[/red]")

    def get_profiles_from_db(self, user_id: int) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Get profiles from both databases"""
        profile1 = self.db_manager.get_profile(user_id, 1)
        profile2 = self.db_manager.get_profile(user_id, 2)
        
        if not profile1 or not profile2:
            raise ValueError(f"User ID {user_id} not found in one or both databases")
            
        return profile1, profile2

    def update_profiles_in_db(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> bool:
        """Update profiles in both databases"""
        success1 = self.db_manager.update_profile(profile1, 1)
        success2 = self.db_manager.update_profile(profile2, 2)
        return success1 and success2

    def get_profile_input(self, profile_num: int) -> Dict[str, Any]:
        """Get profile input from user"""
        self.console.print(f"\n[bold blue]Enter Profile {profile_num} data[/bold blue]")
        self.console.print("Enter as JSON format, e.g., {\"user_id\": 123, \"email\": \"test@example.com\"}")
        
        while True:
            try:
                profile_str = Prompt.ask("Enter profile data")
                return json.loads(profile_str)
            except json.JSONDecodeError:
                self.console.print("[red]Invalid JSON format. Please try again.[/red]")

    def analyze_profiles(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> str:
        """Analyze differences between profiles using LangChain"""
        template = """
        Compare these profiles and provide a CONCISE analysis:
        Profile 1: {profile1}
        Profile 2: {profile2}

        Format your response EXACTLY like this:
        DIFFERENCES:
        - field_name: value1 vs value2 (recommended: suggested_format)

        ACTIONS NEEDED:
        1. Brief action item
        2. Brief action item
        """

        prompt = ChatPromptTemplate.from_template(template)
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        return chain.run(profile1=profile1, profile2=profile2)

    def verify_profiles_match(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> str:
        """Verify if profiles match after corrections"""
        template = """
        Compare these profiles CONCISELY:
        Profile 1: {profile1}
        Profile 2: {profile2}
        
        If identical, respond: "PROFILES_MATCH"
        If different, list ONLY the remaining differences:
        - field: value1 vs value2 (fix needed)
        """

        prompt = ChatPromptTemplate.from_template(template)
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        return chain.run(profile1=profile1, profile2=profile2)

    def run_interactive_session(self):
        """Run the interactive audit session"""
        self.console.print("[bold green]Welcome to the Interactive Profile Auditor![/bold green]")
        
        # Initialize databases with sample data
        self.db_manager.seed_sample_data()
        
        while True:
            try:
                # Get user ID and profiles from databases
                user_id = self.get_user_id_input()
                profile1, profile2 = self.get_profiles_from_db(user_id)
                
                # Show current profiles
                self.console.print("\n[bold blue]Current Profiles:[/bold blue]")
                self.console.print(f"Profile 1: {profile1}")
                self.console.print(f"Profile 2: {profile2}")
                
                # Analyze differences
                self.console.print("\n[bold yellow]Analyzing profiles...[/bold yellow]")
                analysis = self.analyze_profiles(profile1, profile2)
                self.console.print("\n[bold green]Analysis Results:[/bold green]")
                self.console.print(analysis)
                
                # Continue until profiles match
                while True:
                    if "PROFILES_MATCH" in analysis.upper():
                        self.console.print("\n[bold green]✓ Profiles now match![/bold green]")
                        # Update databases with final versions
                        if self.update_profiles_in_db(profile1, profile2):
                            self.console.print("[bold green]✓ Databases updated successfully![/bold green]")
                        else:
                            self.console.print("[bold red]× Failed to update databases![/bold red]")
                        break
                        
                    # Get updated profiles
                    self.console.print("\n[bold blue]Please enter the revised profiles based on the suggestions:[/bold blue]")
                    profile1 = self.get_profile_input(1)
                    profile2 = self.get_profile_input(2)
                    
                    # Verify if they match
                    self.console.print("\n[bold yellow]Verifying profiles...[/bold yellow]")
                    analysis = self.verify_profiles_match(profile1, profile2)
                    self.console.print("\n[bold green]Verification Results:[/bold green]")
                    self.console.print(analysis)
                
                # Ask if user wants to continue with another user
                if not Prompt.ask("\nWould you like to audit another user?", choices=["y", "n"]) == "y":
                    break
                    
            except ValueError as e:
                self.console.print(f"[bold red]Error: {str(e)}")
                continue
            except Exception as e:
                self.console.print(f"[bold red]Unexpected error: {str(e)}")
                continue
        
        self.console.print("[bold green]Thank you for using the Interactive Profile Auditor![/bold green]") 