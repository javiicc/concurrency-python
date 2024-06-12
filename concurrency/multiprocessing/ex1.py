# Example using multiprocessing.Process to create a child process and verify
# that two processes cannot share data directly through a simple variable
# because each process has its own separate memory space.
import logging
from concurrency.operations.cpu_bound import cpu_bound_operation
from multiprocessing import Process


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def cpu_bound_task(counts: int) -> None:
    """Run a CPU-bound task and append the results to shared_list."""
    time = cpu_bound_operation(counts)
    logging.info(f"time - {time}")


def multiprocessing() -> None:

    # Run in a child process ; 150000000 is 3.25 secs aprox in my laptop
    p = Process(target=cpu_bound_task, args=(150000000,))
    p.start()  # Starts the process and calls the target function
    p.join()  # Blocks the thread


if __name__ == "__main__":
    logging.info("Init program")
    multiprocessing()
    logging.info("Finish program")
