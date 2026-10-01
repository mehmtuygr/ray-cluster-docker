import math
import os
import socket
import time

import ray


@ray.remote(num_cpus=1)
def find_primes(start, end):
    """Calculate prime numbers in the given interval as a Ray task."""
    hostname = socket.gethostname()
    pid = os.getpid()
    start_time = time.perf_counter()

    primes = []

    for number in range(max(2, start), end):
        is_prime = True
        limit = math.isqrt(number)

        for divisor in range(2, limit + 1):
            if number % divisor == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(number)

    elapsed_time = time.perf_counter() - start_time

    return {
        "start": start,
        "end": end,
        "prime_count": len(primes),
        "hostname": hostname,
        "pid": pid,
        "elapsed_time": elapsed_time,
    }


def build_ranges(first_number, last_number, chunk_size):
    ranges = []
    start = first_number

    while start <= last_number:
        end = min(start + chunk_size, last_number + 1)
        ranges.append((start, end))
        start = end

    return ranges


def main():
    print("\nRAY PARALLEL PRIME JOB\n")

    ray.init(address="auto")

    print("Ray cluster connection successful.\n")
    print("Cluster resources:")
    print(ray.cluster_resources())

    ranges = build_ranges(
        first_number=2,
        last_number=2_000_000,
        chunk_size=250_000,
    )

    print(f"\n{len(ranges)} Ray tasks will be created.")
    print("\nSubmitting tasks to the cluster...\n")

    job_start_time = time.perf_counter()

    futures = [find_primes.remote(start, end) for start, end in ranges]
    results = ray.get(futures)

    total_time = time.perf_counter() - job_start_time
    total_primes = 0

    print("TASK RESULTS\n")

    for index, result in enumerate(results, start=1):
        total_primes += result["prime_count"]

        print(f"Task {index}")
        print(f'Range        : {result["start"]:,} - {result["end"] - 1:,}')
        print(f'Worker       : {result["hostname"]}')
        print(f'Process ID   : {result["pid"]}')
        print(f'Prime count  : {result["prime_count"]}')
        print(f'Elapsed time : {result["elapsed_time"]:.3f} seconds')
        print("--------------------------------------------")

    print("\nFINAL RESULT")
    print(f"\nTotal prime count        : {total_primes}")
    print(f"Total parallel run time  : {total_time:.3f} seconds")
    print("\nJob completed successfully.")

    ray.shutdown()


if __name__ == "__main__":
    main()
