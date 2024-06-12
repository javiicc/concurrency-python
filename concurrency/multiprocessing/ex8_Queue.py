import logging
from time import perf_counter
from concurrency.operations.cpu_bound import cpu_bound_operation
from multiprocessing import Process, Queue

from concurrency.utils import flaten_list_of_lists, get_saving_path, postprocess_times
from concurrency.visualize import barh


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


# Threads from the same process share memory space
# Processes have different memory space
shared_list = []


def cpu_bound_task_1(counts: int) -> None:
    """Runs a CPU-bound task and appends the results to shared_list."""
    time = cpu_bound_operation(counts)
    logging.info(f"time 1 - {time}")
    logging.info(f"shared_list 1 {shared_list}")
    shared_list.append([time])
    logging.info(f"shared_list 1 {shared_list}")


def cpu_bound_task_2(counts: int, q: Queue) -> None:
    """Runs a CPU-bound task and sends the results to parent."""
    time = cpu_bound_operation(counts)
    logging.info(f"time 2 -  {time}")
    q.put([time])  # Add items to the queue


def multiprocessing() -> None:

    q = Queue()

    start = perf_counter()
    # Run in a child process - 2
    p = Process(target=cpu_bound_task_2, args=(150000000, q))
    p.start()  # Starts the process and calls the target function

    # Run in the main process - 1
    cpu_bound_task_1(150000000)

    child_time = q.get()  # Remove and return an item from the queue
    logging.info(f"child process time: {child_time}")
    shared_list.append(child_time)

    p.join()  # Blocks the thread

    logging.info(f"final shared_list {shared_list}")
    end = perf_counter()

    logging.info(f"Total time :: {round(end - start, 4)} secs")

    # Just some processing for chart
    start_points, end_points = postprocess_times(flaten_list_of_lists(shared_list))

    barh(
        title="Parallel execution, 2 processes, 2 CPU-bound tasks of 3.25 secs each approx",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path("multiprocessing/images/ex8_Queue.png"),
        n=2,  # number of tasks
        color=(0.9, 0.8, 0.1, 0.8),
    )


if __name__ == "__main__":
    logging.info("Init parallel program")
    multiprocessing()
    logging.info("Finish parallel program")
