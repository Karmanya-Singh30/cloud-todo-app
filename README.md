# Cloud-Based To-Do List Application

A beginner-friendly cloud computing mini project built with Python, Flask, SQLite, HTML and CSS. It demonstrates a small web application, source control with GitHub, automated tests using GitHub Actions, and deployment to Render.

## Features
- Add a task
- Mark a task complete or pending
- Delete a task
- View total, pending and completed task counts
- Health endpoint at `/health`
- Automated tests through GitHub Actions

## Technology stack
- Python 3.11+
- Flask
- SQLite
- HTML/CSS
- Git and GitHub
- GitHub Actions (CI)
- Render (cloud deployment)

## Run locally (Windows)
1. Install Python 3.11 or newer.
2. Extract this folder and open it in VS Code.
3. Open Terminal in this folder.
4. Create a virtual environment:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, run `.venv\Scripts\activate.bat` from Command Prompt instead.
5. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Start the app:
   ```powershell
   python app.py
   ```
7. Open http://127.0.0.1:5000 in your browser.

## GitHub setup
Create an empty GitHub repository, then run these commands from this folder (replace the URL with your repository URL):
```bash
git init
git add .
git commit -m "Initial cloud todo application"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```
Do not include your real credentials or secret keys in the repository.

## Deploy to Render
1. Push the project to GitHub.
2. Sign in to Render and choose **New + → Web Service**.
3. Connect the GitHub repository.
4. Use these settings:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Add environment variable `SECRET_KEY` with a long random value (Render's `render.yaml` can generate one when using Blueprint deployment).
6. Deploy, then open the service URL. Test `/` and `/health`.

### Important database note
This starter project uses a local SQLite database. On cloud hosting, files on a free/ephemeral instance may be removed during redeploy or restart. This is acceptable for a simple classroom demonstration, but for durable cloud data, connect a managed PostgreSQL database or use persistent storage. Do not claim persistent storage unless it has actually been configured.

## CI/CD
The workflow in `.github/workflows/ci.yml` runs on pushes and pull requests to `main`. It installs dependencies, compiles the Python file and runs automated tests. Render can deploy from the connected GitHub repository; confirm the deployment settings in Render and test the live URL after each change.

## Project structure
```text
cloud_todo_project/
├── app.py
├── requirements.txt
├── Procfile
├── render.yaml
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── tests/
│   └── test_app.py
└── .github/
    └── workflows/
        └── ci.yml
```

## Mini-project report
Use `REPORT_TEMPLATE.md` as the report outline. Add your own name, roll number, faculty details, screenshots of the app running locally and in the cloud, your actual GitHub URL, and the actual deployed URL. Never invent deployment screenshots or claim a deployment succeeded until you have tested it.
