## Global Team Manager

A modern, responsive cross-timezone team management application with a beautiful Vue.js frontend and FastAPI backend.

### Features

- **Modern UI**: Clean, responsive design with dark/light mode support
- **Team Management**: Create teams and manage members across different timezones
- **Meeting Scheduler**: Schedule meetings and see local times for all team members
- **Real-time Navigation**: Smooth navigation between home and team views
- **Error Handling**: Comprehensive error handling with user-friendly notifications
- **Loading States**: Visual feedback during API operations

### Structure

```
week_2/global_team/
  backend/
    app.py              # FastAPI backend with team management APIs
    requirements.txt    # Python dependencies
    data/              # JSON data storage
  frontend/
    src/
      App.vue          # Main Vue.js application
      main.js          # Vue app entry point
    dist/              # Built frontend assets
    index.html         # HTML template
```

### Run (macOS / Linux)

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r week_2/global_team/backend/requirements.txt
python week_2/global_team/run.py
```

Open `http://localhost:8000/app` in your browser.

### Frontend (Vue)

Dev server (optional):
```
cd week_2/global_team/frontend
npm install
npm run dev
```

Build for backend serving:
```
cd week_2/global_team/frontend
npm run build
```
Then refresh `http://localhost:8000/app` to use the built app.

### API Actions (via POST /app)

```json
{ "action": "list_members" }
```

```json
{ "action": "add_member", "name": "Alice", "timezone": "Europe/London" }
```

```json
{ "action": "propose_meeting", "utc_datetime": "2025-09-16T15:00:00Z" }
```

Data is stored as JSON at `week_2/global_team/backend/data/members.json`.


