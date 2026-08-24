# Local App URLs and Startup Commands

## Verified working apps

### 1) JobTracker
- Local URL: http://localhost:4173/
- Vercel production URL: https://jobtrackerai-fxst1982v-aib-lueprint4x.vercel.app
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

## Notes
- These were verified locally in the current environment.
- JobTracker is also deployed to Vercel and available at https://jobtrackerai-fxst1982v-aib-lueprint4x.vercel.app
- Use these URLs for quick access while the apps are running.
