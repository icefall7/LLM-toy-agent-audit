from profile_auditor import ProfileAuditor

def main():
    # Example profiles
    profile1 = {
        "user_id": 123,
        "email": "aaa@gmail.com",
        "phone": "7347777777",
        "address": "77 Massachusetts Avenue, Cambridge, MA 02139-4307",
        "birthday": "02/11/2025"
    }

    profile2 = {
        "user_id": 123,
        "email": "aa.a@hotmail.com",
        "phone": "1-734-777-7777",
        "address": "77 Massachusetts Ave, Cambridge, MA 02139",
        "birthday": "02/11/2025"
    }

    # Initialize auditor
    auditor = ProfileAuditor()

    # Compare profiles
    result = auditor.compare_profiles(profile1, profile2)

    # Print results
    print("\nLLM Analysis:")
    print("-" * 50)
    print(result["llm_analysis"])
    
    print("\nProgrammatic Differences:")
    print("-" * 50)
    for field, (val1, val2) in result["programmatic_differences"].items():
        print(f"{field}:")
        print(f"  Profile 1: {val1}")
        print(f"  Profile 2: {val2}")

if __name__ == "__main__":
    main() 