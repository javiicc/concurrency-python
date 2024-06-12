import logging
from time import perf_counter, sleep


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def io_bound_operation(secs: float | int) -> tuple[float]:
    """Simulate an I/O-bound operation that lasts for one second."""
    start = perf_counter()
    sleep(secs)
    finish = perf_counter()

    return start, finish


if __name__ == "__main__":
    n = 10
    for i in range(n):
        start, stop = io_bound_operation()
        logging.info(f"Step {i} took {stop - start} secs")
