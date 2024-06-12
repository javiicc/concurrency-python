import logging
from threading import Thread
from concurrency.operations.cpu_bound import cpu_bound_operation

from concurrency.operations.io_bound import io_bound_operation
from concurrency.utils import flaten_list_of_lists, get_saving_path, postprocess_times
from concurrency.visualize import barh


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


shared_list = []  # threads from the same process share data


def thread_io_bound_operations(n: int, secs: float | int) -> None:
    """Run n I/O-bound tasks of secs seconds and append the results to shared_list."""
    shared_list.append([io_bound_operation(secs) for _ in range(n)])


def thread_cpu_bound_operations(counts: int) -> None:
    """Run a CPU-bound task and append the results to shared_list."""
    shared_list.append([cpu_bound_operation(counts)])


def threading_six_threads() -> None:
    # Create two thread objects, each thread will perform five I/O-bound tasks
    t1 = Thread(target=thread_cpu_bound_operations, args=(100000000,))
    t2 = Thread(target=thread_cpu_bound_operations, args=(50000000,))
    t3 = Thread(target=thread_cpu_bound_operations, args=(20000000,))
    t4 = Thread(target=thread_io_bound_operations, args=(1, 1))
    t5 = Thread(target=thread_io_bound_operations, args=(1, 1))
    t6 = Thread(target=thread_io_bound_operations, args=(1, 1))

    # Start activity -> invokes run() method
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    # Block the calling thread -> Avoids continuing to run without threads being finished
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()

    logging.info(f"shared_list {shared_list}")

    # Just some processing for chart
    start_points, end_points = postprocess_times(flaten_list_of_lists(shared_list))

    barh(
        title="Concurrent execution, 6 threads, 3 I/O-bound tasks of 1s and 3 CPU-bound tasks",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path("threading/images/ex_7_six_threads_threading_lib.png"),
        n=6,
    )


if __name__ == "__main__":
    logging.info(f"Init concurrent tasks")
    threading_six_threads()
    logging.info(f"Finish concurrent tasks")
