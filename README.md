# Ray Cluster Demo with Docker

A simple distributed computing project that demonstrates how to run a local **Ray cluster with Docker Compose** and distribute CPU-bound tasks across multiple worker nodes.

The project calculates prime numbers up to **2,000,000** by splitting the workload into multiple Ray tasks and executing them across two worker containers.

## Architecture

The cluster consists of three Docker containers:

- **ray-head** — Ray head node, cluster management, Dashboard, and Jobs API
- **ray-worker-1** — Worker node with 1 Ray CPU
- **ray-worker-2** — Worker node with 1 Ray CPU

The head node is configured with `0` CPUs so computational tasks are executed only by the worker nodes.

```text
                    ┌─────────────────────┐
                    │      ray-head       │
                    │   Ray Head Node     │
                    │ Dashboard / Jobs API│
                    │      CPU: 0         │
                    └──────────┬──────────┘
                               │
                   Ray Cluster │
                      Port 6379│
                     ┌─────────┴─────────┐
                     │                   │
            ┌────────▼────────┐ ┌────────▼────────┐
            │  ray-worker-1   │ │  ray-worker-2   │
            │     CPU: 1      │ │     CPU: 1      │
            └─────────────────┘ └─────────────────┘
```

## Project Structure

```text
ray_project/
├── app/
│   └── prime_job.py
├── docker-compose.yml
└── README.md
```

## How It Works

The Python job:

1. Connects to the running Ray cluster.
2. Splits the range from `2` to `2,000,000` into multiple chunks.
3. Creates Ray remote tasks for each chunk.
4. Ray schedules the tasks across the available worker nodes.
5. Each worker calculates the number of primes in its assigned ranges.
6. The results are collected and combined into the final prime count.

Each task also reports its worker hostname, process ID, and execution time, making it possible to observe how the workload is distributed across the cluster.

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

The cluster should contain:

- 1 head node
- 2 worker nodes
- 2 CPUs available for computational tasks

## Submit the Job

```powershell
docker compose exec ray-head ray job submit --address=http://127.0.0.1:8265 --working-dir=/app -- python prime_job.py
```

## Example Output

Example output from a successful run:

```text
TASK RESULTS

Task 1
Range        : 2 - 250,001
Worker       : ray-worker-2
Process ID   : 222
Prime count  : 22044
Elapsed time : 0.277 seconds
--------------------------------------------

Task 2
Range        : 250,002 - 500,001
Worker       : ray-worker-1
Process ID   : 222
Prime count  : 19494
Elapsed time : 0.441 seconds
--------------------------------------------

...

Task 8
Range        : 1,750,002 - 2,000,000
Worker       : ray-worker-1
Process ID   : 222
Prime count  : 17325
Elapsed time : 0.848 seconds
--------------------------------------------

FINAL RESULT

Total prime count        : 148933
Total parallel run time  : 3.416 seconds
```

In this run, Ray distributed the tasks across both `ray-worker-1` and `ray-worker-2`, demonstrating parallel execution across separate worker nodes.

## Ray Dashboard

The Ray Dashboard can be used to inspect cluster resources, nodes, tasks, and jobs.

After starting the cluster, open:

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

## Technologies

- Python
- Ray
- Docker
- Docker Compose
- Distributed Computing
