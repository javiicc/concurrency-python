import logging

from concurrency.operations.io_bound import io_bound_operation
from concurrency.utils import get_saving_path, postprocess_times
from concurrency.visualize import barh


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def sequential(n: int = 10, secs: float | int = 1) -> None:
    """Perform n I/O-bound operations of secs seconds sequentially in one thread
    and plot a horizontal bar chart.
    """
    # Perform n I/O-bound operations, save a tuple for each task
    times = [io_bound_operation(secs) for _ in range(n)]
    start_points, end_points = postprocess_times(times)

    barh(
        title="Sequential execution, 1 thread, 10 I/O-bound tasks of 1s",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path("threading/images/ex_1_one_thread.png"),
    )


if __name__ == "__main__":
    logging.info(f"Init sequential tasks")
    sequential(n=10, secs=1)
    logging.info(f"Finish sequential tasks")
