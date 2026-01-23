# Copilot Instructions for example-application

## Architecture Overview

This is a **two-tier Flask microservices demo** deployed on Kubernetes:

- **Frontend** (`frontend/frontend.py`): Flask app that renders HTML and calls the backend API
- **Backend** (`backend/app.py`): Flask REST API that returns JSON responses with hostname
- **Data Flow**: Frontend (port 80) → requests `BACKEND_URL` → Backend Service (`flask-api-service`)
- **K8s Integration**: Frontend discovers backend via `flask-api-service.workshop-basic-app.svc.cluster.local` (DNS-based service discovery)

## Key Conventions & Patterns

### Python Components
- Both components are **Flask-based microservices** with minimal dependencies
- Dependencies: `flask` (backend), `flask` + `requests` (frontend)
- Apps bind to `0.0.0.0:80` for container deployment
- Use **environment variables** for configuration (e.g., `BACKEND_URL` in frontend)

### Kubernetes Deployment
- **Service names are DNS hostnames**: Frontend uses `BACKEND_URL=http://flask-api-service.workshop-basic-app.svc.cluster.local`
- Service discovery relies on **ClusterIP** services (internal DNS only)
- Images are stored in **GHCR**: `ghcr.io/{owner}/example-application/{component}-demo`
- Image tags: `:dev` for development builds, `:latest` and `:vX.Y.Z` for releases

### Versioning & Release Workflow
- Version managed in `version` file (simple `X.Y.Z` format)
- Patch version auto-incremented on every merge to `main`
- Two-stage CI/CD:
  1. `push-dev.yaml`: Tests → Build `:dev` images → Bump version → Auto-tag
  2. `tag-release.yaml`: Triggered by successful tag → Build `:latest` + `:vX.Y.Z` images → Create GH Release

## Developer Workflows

### Testing
```bash
./run-tests.sh
```
Runs startup checks for both components:
- Creates isolated venv per component
- Installs requirements
- Validates Python syntax with `compileall` or actual startup (for Flask apps)
- Runs sequentially (frontend first, then backend)

### Local Development
1. Create venv: `python -m venv venv && source venv/bin/activate`
2. Install deps: `pip install -r {backend|frontend}/requirements.txt`
3. Run Flask app: `python {backend|frontend}/app.py` (starts on `0.0.0.0:80`)

### Docker & Registry
- Each component has own `Dockerfile` (in component directory)
- Push to GHCR happens in CI workflows only
- Credentials: Uses `GITHUB_TOKEN` + `github.actor` for authentication

## Critical Integration Points

1. **Frontend-Backend Communication**: Frontend must set `BACKEND_URL` env var; K8s YAML uses cluster-internal DNS name
2. **Service Discovery**: K8s DNS resolves `flask-api-service` to backend pod IPs
3. **Version File**: Single source of truth (`version`); CI auto-increments; must be committed to trigger releases

## Important Constraints

- Both apps run on port **80** inside containers (hardcoded)
- Frontend uses `requests.get()` (synchronous) — no async patterns
- No databases, persistent storage, or authentication
- GitHub Actions expect write permissions for git operations (version commits/tags)
