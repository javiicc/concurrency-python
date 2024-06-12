import logging
from time import perf_counter, sleep
from concurrency.operations.cpu_bound import cpu_bound_operation

from concurrency.operations.io_bound import io_bound_operation


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def io_and_cpu_bound_operation(secs: float | int, n: int) -> tuple[float]:
    """Simulate an I/O-bound operation that lasts for one second."""
    start = perf_counter()
    io_bound_operation(secs)
    cpu_bound_operation(n)
    finish = perf_counter()

    return start, finish


if __name__ == "__main__":
    secs = 1
    n = 50000000
    logging.info(f"Starting I/O-bound and CPU-bound task")
    start, stop = io_and_cpu_bound_operation(secs, n)
    logging.info(f"Task took {stop - start} secs")
