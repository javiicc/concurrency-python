import logging
from time import perf_counter, time
from concurrency.operations.cpu_bound import cpu_bound_operation
from multiprocessing import Process


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


# Threads from the same process share memory space
# Processes have different memory space
shared_list = []


def cpu_bound_task_1(counts: int) -> None:
    """Run a CPU-bound task and append the results to shared_list."""
    time = cpu_bound_operation(counts)
    logging.info(f"time 1 - {time}")
    logging.info(f"shared_list 1 {shared_list}")
    shared_list.append([time])
    logging.info(f"shared_list 1 {shared_list}")


def cpu_bound_task_2(counts: int) -> None:
    """Run a CPU-bound task and append the results to shared_list."""
    time = cpu_bound_operation(counts)
    logging.info(f"time 2 -  {time}")
    logging.info(f"shared_list 2 {shared_list}")
    shared_list.append([time])
    logging.info(f"shared_list 2 {shared_list}")


def multiprocessing() -> None:

    start = perf_counter()
    # Run in the main process - 1
    cpu_bound_task_1(150000000)

    # Run in a child process - 2
    p = Process(target=cpu_bound_task_2, args=(150000000,))
    p.start()  # Starts the process and calls the target function
    p.join()  # Blocks the thread

    logging.info(f"final shared_list {shared_list}")
    end = perf_counter()

    logging.info(f"Total time :: {round(end - start, 4)} secs")


if __name__ == "__main__":
    logging.info("Init program")
    multiprocessing()
    logging.info("Finish program")
