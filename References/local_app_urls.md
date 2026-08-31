# Local App URLs and Startup Commands

## Verified working apps

### 1) JobTracker
- Local URL: http://localhost:4173/
- Vercel production URL: https://jobtrackerai-five.vercel.app
- Project folder: `C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\05_Chapter_JobTrackerAI`
- Start command:
  ```powershell
  cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\05_Chapter_JobTrackerAI"
  npm run dev -- --host 0.0.0.0 --port 4173
  ```

### 2) Jira Test Case Generator
- Local URL: http://localhost:8501/
- Vercel production URL: https://jira-test-case-generator-delta.vercel.app
- Project folder: `C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\03_Chapter_Local_TC_Generator`
- Start command:
  ```powershell
  cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\03_Chapter_Local_TC_Generator"
  python -m uvicorn api.index:app --host 0.0.0.0 --port 8000
  ```

### 3) Jira Test Plan Generator
- Local URL: http://localhost:8502/
- Vercel production URL: https://jira-test-plan-generator.vercel.app
- Vercel project dashboard: https://vercel.com/aib-lueprint4x/jira-test-plan-generator
- Project folder: `C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\07_Chapter_AI_Agents\Test-Plan-Agent-Blast`
- Start command:
  ```powershell
  cd "C:\Users\rajra\Documents\AI\4X AI Tester Blueprint\07_Chapter_AI_Agents\Test-Plan-Agent-Blast"
  python -m streamlit run streamlit_app.py --server.address localhost --server.port 8502
  ```
- Usage: Enter a Jira reference such as `SCRUM-6`, then generate and download the test plan in Markdown, JSON, or HTML.
- Deployment note: The hosted app uses Groq for AI enhancement because Vercel cannot access local Ollama. Jira and Groq credentials are configured as Vercel production secrets.

## Notes
- These were verified locally in the current environment.
- JobTracker is also deployed to Vercel and available at https://jobtrackerai-five.vercel.app
- Use these URLs for quick access while the apps are running.
