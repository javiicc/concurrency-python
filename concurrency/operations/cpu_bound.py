import logging
from time import perf_counter, sleep


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def cpu_bound_operation(n: int) -> tuple[float]:
    """CPU-bound task."""
    start = perf_counter()
    count = 0
    for i in range(n):
        count += i
    finish = perf_counter()

    return start, finish


if __name__ == "__main__":
    n = 50000000
    # n = 20000000
    logging.info("Starting CPU-bound task")
    start, stop = cpu_bound_operation(n)
    logging.info(f"Task took {stop - start} secs")
