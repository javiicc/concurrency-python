import logging
from math import ceil
import os
from concurrent.futures import as_completed, ProcessPoolExecutor
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

    n_tasks = 8
    args = [50000000] * n_tasks

    # Run in worker processes
    start = time()
    # Use ProcessPoolExecutor to manage concurrency
    with ProcessPoolExecutor(max_workers=2) as executor:
        # Submit tasks
        results = executor.map(cpu_bound_task, args)  # does not block

        # Retrieve results
        times = [result for result in results]  # blocks
    end = time()

    total_time = end - start
    logging.info(f"Total time: {total_time}")

    # Just some processing for chart
    start_points, end_points = postprocess_times(times)

    barh(
        title="Parallel execution, 2 workers, 8 CPU-bound tasks of 1 sec each approx",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path(
            "process-pool-executor/images/ex3_ProcessPoolExecutor.png"
        ),
        n=n_tasks,  # number of tasks
        color=(0.5, 0.2, 0.9, 0.8),
        secs=ceil(total_time),
    )


if __name__ == "__main__":
    logging.info("Init parallel program")
    main()
    logging.info("Finish parallel program")
