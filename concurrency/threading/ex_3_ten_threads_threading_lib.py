import logging
from threading import Thread

from concurrency.operations.io_bound import io_bound_operation
from concurrency.utils import flaten_list_of_lists, get_saving_path, postprocess_times
from concurrency.visualize import barh


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


shared_list = []  # threads from the same process share data


def thread_io_bound_operations(n: int, secs: float | int) -> None:
    """Run n I/O-bound tasks of secs seconds and append the results to shared_list."""
    shared_list.append([io_bound_operation(secs) for _ in range(n)])


def threading_two_threads() -> None:
    threads = []
    # Create ten thread objects, each thread will one I/O-bound tasks
    for _ in range(10):
        t = Thread(target=thread_io_bound_operations, args=(1, 1))
        t.start()
        threads.append(t)

    # Block the calling thread -> Avoids continuing to run without threads being finished
    [thread.join() for thread in threads]

    logging.info(f"shared_list {shared_list}")

    # Just some processing for chart
    start_points, end_points = postprocess_times(flaten_list_of_lists(shared_list))

    barh(
        title="Concurrent execution, 10 threads, 1 I/O-bound tasks of 1s each",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path("threading/images/ex_3_ten_threads_threading_lib.png"),
    )


if __name__ == "__main__":
    logging.info(f"Init concurrent tasks")
    threading_two_threads()
    logging.info(f"Finish concurrent tasks")
