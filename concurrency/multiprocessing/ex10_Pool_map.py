import logging
import os
from multiprocessing import Pool

from concurrency.operations.cpu_bound import cpu_bound_operation
from concurrency.utils import flaten_list_of_lists, get_saving_path, postprocess_times
from concurrency.visualize import barh


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def cpu_bound_task(counts: int) -> None:
    """Runs a CPU-bound task."""
    time = cpu_bound_operation(counts)
    logging.info(f"-------- Process: {os.getpid()} --------")
    logging.info(f"time - {time}\n")
    return [time]


def multiprocessing() -> None:

    args = [50000000, 50000000, 50000000, 50000000, 50000000, 50000000]

    # Run in worker processes
    with Pool(processes=4) as pool:
        res = pool.map(cpu_bound_task, args)  # blocks until the result is ready

        logging.info(res)

    # Just some processing for chart
    start_points, end_points = postprocess_times(flaten_list_of_lists(res))

    barh(
        title="Parallel execution, 4 workers, 6 CPU-bound tasks of 1 sec each approx",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path("multiprocessing/images/ex10_Pool.png"),
        n=6,  # number of tasks
        color=(0.9, 0.8, 0.1, 0.8),
    )


if __name__ == "__main__":
    logging.info("Init parallel program")
    multiprocessing()
    logging.info("Finish parallel program")
