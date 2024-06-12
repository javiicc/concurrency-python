import logging
from threading import Thread
from time import perf_counter, sleep

from concurrency.utils import flaten_list_of_lists, get_saving_path, postprocess_times
from concurrency.visualize import barh


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


shared_list = []  # threads from the same process share data


def io_bound_operation(secs: float | int) -> None:
    """Run 1 I/O-bound task of secs seconds and append the results to
    shared_list."""
    start = perf_counter()
    sleep(secs)
    finish = perf_counter()

    shared_list.append([(start, finish)])


def cpu_bound_operation(n: int) -> None:
    """CPU-bound task."""
    start = perf_counter()
    count = 0
    for i in range(n):
        count += i
    finish = perf_counter()

    shared_list.append([(start, finish)])
    # return start, finish


def threading_two_threads():
    # Create two thread objects
    t1 = Thread(target=io_bound_operation, args=(1,))
    t2 = Thread(target=cpu_bound_operation, args=(100000000,))

    # Start activity -> invokes run() method
    t1.start()
    sleep(0.1)
    t2.start()

    # Block the calling thread -> Avoids continuing to run without threads
    # being finished
    t1.join()
    t2.join()

    logging.info(f"shared_list {shared_list}")

    # Just some processing for chart
    start_points, end_points = postprocess_times(flaten_list_of_lists(shared_list))
    # start_points, end_points = postprocess_times(shared_list)

    barh(
        title="Concurrent execution, 2 threads, 1 I/O-bound task of 1s + 1 CPU-task of 3.5s aprox",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path("threading/images/first_multithreaded_program.png"),
        n=2,
    )


if __name__ == "__main__":
    # logging.info(f"Init CPU-bound operation")
    # start, finish = cpu_bound_operation(100000000)
    # logging.info(f"CPU-bound time: {round(finish - start, 4)}")
    # logging.info(f"Finish CPU-bound operation")

    logging.info(f"Init concurrent tasks")
    threading_two_threads()
    logging.info(f"Finish concurrent tasks")
