# Agno Multi-Agent Prompt Generation System

This project is an AI agent orchestration system that transforms general user requests into detailed, production-ready prompts through the collaborative work of specialized AI agents.

## Project Structure
- `agno_server/` - Main server and agent logic
- `tests/` - Pytest-based unit tests, mirrors main structure
- `.env.example` - Example environment variables (Supabase URL, Service Role Key, Gemini API key)

## Setup
1. Copy `.env.example` to `.env` and fill in your Supabase credentials and Gemini API key.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the tests:
   ```sh
   pytest --maxfail=3 --disable-warnings -q
   ```
4. Start the server (for development):
   ```sh
   uvicorn agno_server.main:app --reload
   ```

## Environment Variables
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Your Supabase service role key
- `GEMINI_API_KEY`: Your Google Gemini 2.5 Pro API key

## API Endpoints

### Supabase Tools
- `POST /tools/read_rows` — Read rows from a table
- `POST /tools/create_record` — Insert records into a table
- `POST /tools/update_record` — Update records in a table
- `POST /tools/delete_record` — Delete records from a table

### Multi-Agent Prompt Refinement
- `POST /refine_prompt` — Refine a rough user idea into a production-ready prompt
  - Request: `{ "user_idea": "<your idea>" }`
  - Response: `{ "prompt": "<refined prompt>" }`
- `POST /refine_prompt_agno` — Refine a rough user idea into a production-ready prompt using Agno's official multi-agent abstractions
  - Request: `{ "user_idea": "<your idea>" }`
  - Response: `{ "prompt": "<refined prompt>" }`

## Features (Planned)
- Multi-agent workflow (Team Lead, Researcher, Tagger, PRD Writer, Prompt Crafter)
- Tool integration (WebSearch, DBQuery)
- Memory and knowledge base
- Modular, testable codebase
- **Agno-native agent stack** for rapid prototyping and model/tool flexibility

## Agent Roles & Responsibilities
- **Team Lead:** Orchestrates workflow, clarifies goals, assigns tasks, ensures alignment with user intent.
- **Internet Researcher:** Gathers external data and examples using WebSearch, cites sources.
- **Info Tagger & Structurer:** Organizes findings into logical categories (features, flows, tech, etc.), leverages DBQuery and shared Memory.
- **PRD Writer:** Drafts a concise Product Requirements Document from structured info.
- **Final Prompt Crafter:** Synthesizes all outputs into a detailed, production-ready prompt in Markdown.

## Conversation Flow
1. Team Lead clarifies the goal and sets the agenda.
2. Researcher gathers and presents findings.
3. Info Tagger organizes findings.
4. PRD Writer drafts requirements.
5. Final Prompt Crafter produces the final prompt.

## Tools & Memory
- **WebSearch:** Real-time search for external info.
- **DBQuery:** Query internal knowledge base for best practices, templates, and technical info.
- **Memory:** Persistent, shared memory for findings and decisions throughout the workflow.

## Output Format
The final output is a Markdown block with the following sections (as relevant):

```
🚀 Final Generated Prompt: [Project Name or Request]
🎯 Overall Task/Goal:
🎭 Persona (Optional):

Sections/Components:
- [Section 1]
- [Section 2]

Detailed Requirements:
- [Details for each section/component]

UI/UX & Design Guidelines:
- [Design principles, style]

Technical Specifications:
- [Stack, DB, APIs, integrations]

Key Considerations:
- [Accessibility, performance, etc.]

Examples (Optional):
- [Relevant examples]
```

## Example User Input
> "אני רוצה לבנות פלטפורמה חדשנית לניהול משימות אישיות..." (see above for full example)

## Example API Request
```json
{
  "user_idea": "Build a minimal, intuitive personal task manager platform with smart reminders and sharing."
}
```

## Example API Response (Markdown)
```
🚀 Final Generated Prompt: Personal Task Manager Platform
🎯 Overall Task/Goal: Build an intuitive, minimal platform for managing personal tasks with smart, context-aware reminders and task sharing.

Sections/Components:
- Task List
- Smart Reminders
- Sharing & Collaboration

Detailed Requirements:
- Users can add, edit, and delete tasks.
- Reminders are triggered based on location/context.
- Tasks can be shared with friends.

UI/UX & Design Guidelines:
- Minimalist, distraction-free interface.
- Mobile-first design.

Technical Specifications:
- Use Supabase for backend/storage.
- Integrate with location APIs for reminders.

Key Considerations:
- Accessibility for all users.
- Real-time sync.

Examples (Optional):
- Todoist, Google Tasks
```

## Testing
Tests are located in the `/tests` directory and follow Pytest conventions. Each feature includes tests for expected, edge, and failure cases.

## Contributing
Please follow PEP8, use type hints, and format code with Black. Add docstrings (Google style) and # Reason: comments for complex logic.

---
For more details, see `PLANNING.md` and `TASK.md`.
# Ragango
