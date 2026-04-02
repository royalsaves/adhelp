# Identity Access Support Console

Portfolio-friendly demo of an internal operations console for account onboarding, password lifecycle workflows, access recovery, and support triage.

## What It Shows

- Hexagonal backend structure with `domain`, `application`, and `adapters`
- Stable HTTP API while infrastructure dependencies stay behind ports
- Demo mode for local execution without AWS, LDAP, Slack, or SMTP credentials
- Small React frontend that exercises the main workflows end to end

## Architecture

```text
frontend -> flask api -> application services -> ports -> adapters
```

Adapter examples:

- Directory adapter: demo or AWS Directory Service
- Identity verifier: demo or LDAP bind
- Notification adapter: console or Slack webhook
- Email adapter: console or SES
- AI adapter: canned demo responder or Bedrock
- Automation adapter: console or external job runner

More detail: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Project Layout

```text
backend/
  app.py
  ad_console/
    api.py
    app.py
    config.py
    domain/
    application/
    adapters/
frontend/
  src/
docs/
```

## Local Run

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Default mode is `demo`, so cloud credentials are not required.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api` to `http://127.0.0.1:5001`.

### 3. Production-style local build

```bash
cd frontend
npm run build
cd ../backend
python app.py
```

The Flask server will serve `frontend/dist`.

## Container Run

No local `npm install` is required for containerized use.

```bash
docker compose up --build
```

Then open `http://127.0.0.1:5001`.

The image builds the React frontend in a Node stage and serves the built assets from the Flask container.

## Demo Workflows

- Request a new account
- Change a password
- Send a reset code and complete a reset
- Request an account unlock
- Ask the support assistant a question

In demo mode, the app logs simulated side effects to stdout instead of calling live services.

## Notes For Public GitHub Use

- No real company names, domains, tokens, or internal URLs are included
- `.env` is ignored and only `.env.example` is committed
- The public frontend uses generic support content rather than internal wiki references

## Next Improvements

- Replace in-memory repositories with PostgreSQL
- Add automated tests around application services
- Add Docker Compose for one-command local startup
- Add role-based auth for admin approval screens
