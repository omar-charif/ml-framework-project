# ml-framework-project
Basic starter framework for ML-related utilities, packaged with a simple FastAPI service.

## Prerequisites
You can run the project in three common ways:

1) **Local Python (no containers)**: easiest if you already have Python + `uv` installed.
2) **Docker**: runs the API in an isolated container so your machine stays clean.
3) **Kubernetes (local)**: runs the same container in a local cluster (useful if you want to practice “real” deployment workflows).

If you are new to these tools, start with **Docker**.

### Which option should I use?
- Choose **Local (no Docker)** if you are just editing Python code and want the fastest feedback loop.
- Choose **Docker** if you want a consistent environment and a workflow closer to how apps run in production.
- Choose **Kubernetes (local)** if you want to practice deployment concepts (pods, services, rolling updates) using the same container image.

### What is `uv` and `uv.lock`?
This repo uses **uv** to manage Python dependencies.

- `pyproject.toml` declares which packages you want (for example: FastAPI, pandas).
- `uv.lock` pins the *exact* versions (and hashes) that were resolved.

Why it matters:
- **Reproducible installs**: the same dependency versions are installed on your machine, in Docker, and in CI.
- **Fewer “works on my machine” problems**.

## FastAPI
FastAPI is a Python web framework for building HTTP APIs.
In this repo it provides a small web server you can extend with ML endpoints later (for example: `/predict`, `/train`, `/metrics`).

API module: `ml_framework_project/api.py`

How it works (high level):
- You define endpoints with decorators like `@app.get("/health")`.
- A web server (Uvicorn) runs the app and listens on a port (here: `8000`).
- You call endpoints with a browser or `curl`.

Key concepts:
- **Route/endpoint**: a URL path + HTTP method (example: `GET /health`).
- **Request/response**: the client sends a request, the API returns JSON.
- **Port**: the network port the server listens on (here it’s `8000`).

Endpoints:
- `GET /`
- `GET /health`
- `POST /pipelines/diamonds/regression`
- `POST /pipelines/diamonds/classification`

Curl examples (Docker or local run):
```bash
curl -s http://localhost:8000/ | jq
curl -s http://localhost:8000/health | jq
```

If you don't have `jq`, you can omit it:
```bash
curl http://localhost:8000/
curl http://localhost:8000/health
```

Curl examples (run the pipelines):
```bash
curl -s -X POST http://localhost:8000/pipelines/diamonds/regression \
	-H 'Content-Type: application/json' \
	-d '{"file_path":"/path/to/diamonds.csv"}' | jq

curl -s -X POST http://localhost:8000/pipelines/diamonds/classification \
	-H 'Content-Type: application/json' \
	-d '{"file_path":"/path/to/diamonds.csv"}' | jq
```

Notes:
- The `file_path` is read by the server process. If you run via Docker/Kubernetes, the path must exist *inside the container* (mount the file into the container or bake it into the image).
- If you deployed to Kubernetes and are using `kubectl port-forward`, the same `curl http://localhost:8000/...` commands work.

## Docker
Docker lets you package your app (code + Python + dependencies) into an **image** and run it as an isolated **container**.
This makes your environment consistent across machines.

Terminology:
- **Image**: a packaged snapshot of a runnable environment (built once).
- **Container**: a running instance of an image (started/stopped many times).
- **Port mapping**: publishing a container port to your laptop (here: `8000:8000`).

In this repo:
- The image is built using the `Dockerfile`
- `docker-compose.yml` is a convenience wrapper to build and run the container
- Dependencies are installed with `uv` and pinned by `uv.lock` for reproducible builds

What happens during `docker compose build`:
- Docker reads `Dockerfile`
- Copies `pyproject.toml` and `uv.lock` into the image
- Runs `uv sync --frozen --no-dev` to install *exactly* what’s in the lock file
- Copies your source code into the image

The Docker image:
- Installs dependencies using `uv` + `uv.lock` (reproducible builds)
- Runs the FastAPI server with Uvicorn on port `8000`

Build:
```bash
docker compose build
```

Run:
```bash
docker compose up
```

What you should see:
- Logs from Uvicorn saying it is listening on `http://0.0.0.0:8000`
- The API becomes available at `http://localhost:8000`

Test:
```bash
curl http://localhost:8000/health
```

Troubleshooting Docker:
- If `curl` fails, check logs: `docker compose logs --tail=200`
- Check container status: `docker compose ps`
- If port `8000` is already in use, stop the other process or change the host port mapping in `docker-compose.yml`.

## Local (no Docker)
This runs the API directly on your machine (no containers).
It uses `uv` to create/manage a local virtual environment and install the dependencies.

Typical workflow:
- `uv sync` installs dependencies into a virtual environment
- `uv run ...` runs the command inside that environment

If you don’t have `uv` installed yet, see: https://docs.astral.sh/uv/

```bash
uv sync
uv run uvicorn ml_framework_project.api:app --host 0.0.0.0 --port 8000
```

### CLI entry points (pipelines)
This repo also defines two CLI commands (console scripts) to run the preprocessing pipelines:

```bash
uv run diamonds-regression path/to/diamonds.csv
uv run diamonds-classification path/to/diamonds.csv
```

## Kubernetes (local)
Kubernetes (K8s) is a system for running containers in a cluster.
Even on your laptop, you can run a “local cluster” (Docker Desktop Kubernetes, kind, or minikube).

In this repo, Kubernetes runs the API as:
- A **Deployment**: keeps the API container running and restarts it if it crashes
- A **Service**: a stable internal address for the Deployment (think “a named port to reach the app”)

Because local clusters typically don’t expose services to your laptop automatically, you use **port-forward** to access it.

How the main Kubernetes commands map to what’s happening:
- `kubectl apply -f ...` creates/updates resources described in the YAML.
- `kubectl get ...` lists resources (pods, services, deployments).
- `kubectl logs ...` shows application logs (like `docker logs`).
- `kubectl port-forward ...` creates a temporary tunnel from your laptop to the Service/Pod.

Important note about images:
- Kubernetes normally pulls images from a registry (Docker Hub, ECR, etc.).
- For local clusters, you often need to **load** your locally built image into the cluster (kind/minikube).
- This repo uses `imagePullPolicy: IfNotPresent` so the cluster will use a local image if available.

Manifest: `k8s/ml-framework-project.yaml` (Deployment + Service)

1) Build the local image:
```bash
docker compose build
```

2) Ensure your cluster can see the local image:

- Docker Desktop Kubernetes: usually works without extra steps
- kind:
```bash
kind load docker-image ml-framework-project:local
```
- minikube:
```bash
minikube image load ml-framework-project:local
```

3) Deploy:
```bash
kubectl apply -f k8s/ml-framework-project.yaml
```

Verify it started:
```bash
kubectl get pods
kubectl get svc
```

Wait until the pod shows `READY 1/1` and `STATUS Running`.

If the pod isn’t ready, inspect:
```bash
kubectl describe pod -l app=ml-framework-project
kubectl logs -l app=ml-framework-project --tail=200
```

Common fixes:
- If you changed Python dependencies: rebuild (`docker compose build`) and re-load the image into kind/minikube.
- If the pod is stuck in `ImagePullBackOff`: the cluster cannot find the image (load it into kind/minikube, or push to a registry).

4) Access locally:
```bash
kubectl port-forward svc/ml-framework-project 8000:8000
curl http://localhost:8000/health
```

Cleanup (remove from the cluster):
```bash
kubectl delete -f k8s/ml-framework-project.yaml
```
