import logging
from math import ceil
import os
from concurrent.futures import ProcessPoolExecutor
from time import perf_counter, time

from concurrency.utils import get_saving_path, postprocess_times
from concurrency.visualize import barh


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def cpu_bound_task(counts: int) -> tuple[float]:
    """Runs a CPU-bound task."""
    start = perf_counter()
    count = 0
    for i in range(counts):
        count += i
    finish = perf_counter()

    logging.info(f"-------- Process: {os.getpid()} --------")
    logging.info(f"time - {round(finish - start, 4)}\n")
    return start, finish


def main():

    n_tasks = 24
    args = [50000000] * n_tasks
    max_workers = 4
    chunksize = 3

    start = time()
    # Use ProcessPoolExecutor to manage concurrency
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks
        results = executor.map(
            cpu_bound_task, args, chunksize=chunksize
        )  # does not block

        # Retrieve results
        times = [result for result in results]  # blocks
    end = time()

    total_time = end - start
    logging.info(f"Total time: {total_time}")

    # Just some processing for chart
    start_points, end_points = postprocess_times(times)

    barh(
        title="Parallel execution, 4 workers, 24 CPU-bound tasks of 1 sec each approx",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path(
            "process-pool-executor/images/ex4_ProcessPoolExecutor.png"
        ),
        n=n_tasks,  # number of tasks
        color=(0.5, 0.2, 0.9, 0.8),
        secs=ceil(total_time),
    )


if __name__ == "__main__":
    logging.info("Init parallel program")
    main()
    logging.info("Finish parallel program")
