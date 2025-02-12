from interactive_audit_service import InteractiveAuditService
from rich.prompt import Prompt

def main():
    # Let user choose the model
    model_choices = {
        "1": "gpt-4o-mini",
        "2": "gpt-4o",
        "3": "gpt-3.5-turbo"
    }
    
    print("\nAvailable Models:")
    for key, model in model_choices.items():
        print(f"{key}: {model}")
    
    choice = Prompt.ask(
        "Select model number", 
        choices=list(model_choices.keys()), 
        default="1"
    )
    
    # Initialize service with chosen model
    service = InteractiveAuditService(model_name=model_choices[choice])
    service.run_interactive_session()

if __name__ == "__main__":
    main() 