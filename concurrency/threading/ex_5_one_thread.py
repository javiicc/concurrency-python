import logging

from concurrency.operations.cpu_bound import cpu_bound_operation
from concurrency.utils import get_saving_path, postprocess_times
from concurrency.visualize import barh


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def sequential(counts: int, n: int = 10) -> None:
    # Perform n CPU-bound operations, save a tuple for each task
    times = [cpu_bound_operation(counts) for _ in range(n)]
    start_points, end_points = postprocess_times(times)

    barh(
        title="Sequential execution, 1 thread, 2 CPU-bound tasks of 3.5s aprox",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path("threading/images/ex_5_one_thread.png"),
        n=n,
    )


if __name__ == "__main__":
    logging.info(f"Init sequential tasks")
    sequential(counts=100000000, n=2)
    logging.info(f"Finish sequential tasks")
