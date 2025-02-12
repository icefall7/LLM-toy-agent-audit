# LLM-toy-agent-audit

An AI-powered interactive audit system that compares and reconciles user profiles across different databases using LLM capabilities and LangChain.

## Features

- Interactive terminal-based profile auditing
- SQLite database integration with sample data
- Compare user profiles across two databases
- Intelligent analysis of differences using LLM
- Streaming responses for better user experience
- Interactive profile correction workflow
- Automatic database updates when profiles match
- Support for multiple LLM models
- Rich terminal output with color coding

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- SQLite (comes with Python)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LLM-toy-agent-audit.git
cd LLM-toy-agent-audit
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```

## Database Structure

The system uses two SQLite databases to simulate different data sources. Each database contains:
- User profiles with fields:
  - user_id (PRIMARY KEY)
  - email
  - phone
  - address
  - birthday

Sample data is automatically seeded when you run the application.

## Usage

1. Run the interactive auditor:
```bash
python3 main.py
```

2. Select your preferred LLM model when prompted:
   - 1: gpt-4o-mini
   - 2: gpt-4o
   - 3: gpt-3.5-turbo

3. Enter a user ID to audit (e.g., 123 or 124)

4. The system will:
   - Fetch profiles from both databases
   - Show current profile data
   - Analyze differences
   - Provide recommendations

5. When prompted, enter corrected profile data in JSON format:
```json
{
    "user_id": 123,
    "email": "user@example.com",
    "phone": "734-777-7777",
    "address": "77 Massachusetts Avenue, Cambridge, MA 02139",
    "birthday": "02/11/2025"
}
```

6. Continue updating profiles until they match
7. Databases will be automatically updated when profiles match

## Example Workflow

```bash
$ python3 main.py

Available Models:
1: gpt-4o-mini
2: gpt-4o
3: gpt-3.5-turbo

Select model number: 1

Enter User ID to audit: 123

Current Profiles:
Profile 1: {"user_id": 123, "email": "aaa@gmail.com", ...}
Profile 2: {"user_id": 123, "email": "aa.a@hotmail.com", ...}

Analyzing profiles...

DIFFERENCES:
- email: aaa@gmail.com vs aa.a@hotmail.com (recommended: aaa@gmail.com)
- phone: 7347777777 vs 1-734-777-7777 (recommended: 734-777-7777)
...
```

## Project Structure

- `main.py`: Entry point and model selection
- `interactive_audit_service.py`: Core interactive audit logic
- `database/db_manager.py`: Database operations
- `database/`: SQLite database files
- `requirements.txt`: Project dependencies

## Error Handling

The system handles various scenarios:
- Invalid user IDs
- Missing database records
- JSON parsing errors
- Database update failures
- API errors

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Notes

- The sample databases are recreated each time the application runs
- For production use, replace SQLite with your actual database system
- Adjust the LLM model based on your needs for speed vs accuracy