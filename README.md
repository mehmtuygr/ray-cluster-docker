# Ray Cluster Demo with Docker

This project runs a local Ray cluster with Docker Compose:

- `ray-head`: Ray head node and dashboard / Jobs API
- `ray-worker-1`: worker node with 1 Ray CPU
- `ray-worker-2`: worker node with 1 Ray CPU

The Python job splits prime-number calculation into Ray tasks and submits them to the running cluster with `ray job submit`.

## Start the Cluster

```powershell
docker compose up -d
```

## Check Containers

```powershell
docker compose ps
```

## Check Ray Status

```powershell
docker exec ray-head ray status
```

You should see 1 head node, 2 worker nodes, and 2 total CPUs available for tasks.

## Submit the Job

```powershell
docker compose exec ray-head ray job submit --address=http://127.0.0.1:8265 --working-dir=/app -- python prime_job.py
```

The output should include both `ray-worker-1` and `ray-worker-2`, proving that the task chunks ran on separate Ray worker nodes.

## Open Dashboard

Visit:

```text
http://localhost:8265
```

## List Jobs

```powershell
docker compose exec ray-head ray job list --address=http://127.0.0.1:8265
```

## Stop the Cluster

```powershell
docker compose down
```
