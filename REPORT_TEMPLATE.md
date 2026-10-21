# Mini Project Report: Cloud-Based To-Do List Application

> Replace every bracketed placeholder with your own details. Add real screenshots and URLs only after you have run and deployed the application.

## Cover Page
- **Course:** Introduction to Cloud Computing (TE7948)
- **Project title:** Cloud-Based To-Do List Application
- **Student name:** [Your name]
- **Roll number:** [Your roll number]
- **Faculty:** [Faculty name]
- **Institute:** [Institute name]
- **Submission date:** [Date]

## 1. Abstract
This project implements a simple task-management web application using Python Flask, HTML, CSS and SQLite. Users can add, edit, complete and delete tasks. GitHub is used for version control, GitHub Actions runs automated checks, and Render is used as the cloud deployment platform. The project demonstrates a basic web application deployment workflow.

## 2. Problem Statement
People need a simple way to maintain a list of tasks and track their completion. The project provides a browser-based task list that can be accessed through a hosted URL after deployment.

## 3. Objectives
1. Build a simple modular web application.
2. Implement task creation, completion and deletion.
3. Store task data using SQLite.
4. Maintain source code in GitHub.
5. Run automated checks through GitHub Actions.
6. Deploy the application on a cloud hosting platform.

## 4. Technology Stack
| Component | Technology | Purpose |
|---|---|---|
| Frontend | HTML, CSS | User interface |
| Backend | Python, Flask | Routes and application logic |
| Database | SQLite | Task storage |
| Version control | Git, GitHub | Source code history |
| CI | GitHub Actions | Automated compile check and tests |
| Cloud hosting | Render | Public web deployment |

## 5. System Design
The browser sends HTTP requests to the Flask application. Flask processes task actions and reads/writes records in SQLite. The HTML template displays the task list. GitHub stores the source code and GitHub Actions runs automated checks when code is pushed or a pull request is opened. Render hosts the web service.

**Architecture flow:** User Browser → Flask Web Application → SQLite Database  
**Delivery flow:** Developer → GitHub Repository → GitHub Actions CI → Render Deployment

## 6. Main Features
- Add a task
- Edit a task's title
- Mark a task complete or pending
- Delete a task (with confirmation)
- Display total, pending and completed counts with a progress bar
- Input validation, success/error messages and 400/404 error pages
- CSRF protection on all forms
- Health endpoint at `/health` that also checks the database

## 7. Implementation
Describe the key files:
- `app.py`: Flask routes, SQLite database setup and task operations.
- `templates/base.html`, `index.html`, `error.html`: shared layout, task page and error page.
- `static/style.css`: page styling and responsive layout.
- `tests/test_app.py`: automated tests.
- `.github/workflows/ci.yml`: continuous integration workflow.
- `render.yaml` and `Procfile`: cloud service configuration.

## 8. Local Setup and Testing
Write the exact Python version and commands used. Include screenshots of:
1. Application running locally.
2. Adding a task.
3. Marking a task complete.
4. GitHub Actions checks passing.

## 9. Cloud Deployment
- **Platform:** Render
- **GitHub repository URL:** [Paste your real repository URL]
- **Live application URL:** [Paste your real deployed URL]
- **Health check:** [Paste live URL followed by `/health`]
- **Deployment steps:** Connect the GitHub repository, configure build command `pip install -r requirements.txt`, start command `gunicorn app:app`, set `SECRET_KEY`, then deploy.
- Add a screenshot of the live application.

## 10. CI/CD Configuration
The GitHub Actions workflow triggers on pushes and pull requests to `main`. It checks out the code, sets up Python, installs dependencies, compiles `app.py`, and runs unit tests. Render deployment is configured separately through the connected repository; verify the live service after deployment.

## 11. Results
[Describe only what you actually tested. Record the test results and include real screenshots.]

## 12. Limitations and Future Scope
This starter version uses SQLite, and the database file on an ephemeral cloud instance may not persist through redeployments or restarts. Future improvements include managed PostgreSQL, user login, task due dates, priorities and reminders.

## 13. Conclusion
The project demonstrates a basic modular web application and a practical development workflow involving source control, automated testing and cloud hosting. It provides a small example of how a web application can be built, tested and made accessible through a public URL.

## References
- Flask documentation: https://flask.palletsprojects.com/
- GitHub Actions documentation: https://docs.github.com/actions
- Render documentation: https://render.com/docs
