from math import ceil
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import perf_counter, time
import urllib.request
import logging

from concurrency.utils import flaten_list_of_lists, get_saving_path, postprocess_times
from concurrency.visualize import barh


format = "%(levelname)s %(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


URLS = [
    [
        "https://en.wikipedia.org/wiki/Emu",
        "https://en.wikipedia.org/wiki/Wombat",
        "https://en.wikipedia.org/wiki/Kangaroo",
        "https://en.wikipedia.org/wiki/Platypus",
        "https://en.wikipedia.org/wiki/Koala",
    ],
    [
        "https://en.wikipedia.org/wiki/Tasmanian_devil",
        "https://en.wikipedia.org/wiki/Echidna",
        "https://en.wikipedia.org/wiki/Dingo",
        "https://en.wikipedia.org/wiki/Kookaburra",
        "https://en.wikipedia.org/wiki/Wallaby",
    ],
    [
        "https://en.wikipedia.org/wiki/Macrotis",
        "https://en.wikipedia.org/wiki/Quokka",
        "https://en.wikipedia.org/wiki/Cassowary",
        "https://en.wikipedia.org/wiki/Sugar_glider",
        "https://en.wikipedia.org/wiki/Laughing_kookaburra",
    ],
    [
        "https://en.wikipedia.org/wiki/Rainbow_lorikeet",
        "https://en.wikipedia.org/wiki/Coastal_taipan",
        "https://en.wikipedia.org/wiki/Mistletoebird",
        "https://en.wikipedia.org/wiki/Thylacine",
        "https://en.wikipedia.org/wiki/Quoll",
    ],
]


animals = {}
counts = 0


# I/O-bound operation
def load_url(url: str) -> tuple[float]:
    """Retrieve a single page and return start and finish times."""
    logging.info(f"PID: {os.getpid()} ; url: {url}")

    start = perf_counter()
    try:
        with urllib.request.urlopen(url) as conn:
            animals[url] = conn.read()
    except Exception:
        logging.error(f"PID: {os.getpid()} ; url: {url}")
        return start, start
    finish = perf_counter()

    global counts
    counts += len(animals[url]) * 4

    return start, finish


def cpu_bound_task(counts: int) -> tuple[float]:
    """Runs a CPU-bound task."""
    logging.info(f"PID: {os.getpid()} ; counts: {counts}")

    start = perf_counter()
    count = 0
    for i in range(counts):
        count += i
    finish = perf_counter()
    return start, finish


def task(urls: list[str]) -> list:
    logging.info(f"Loading australian animals... PID: {os.getpid()}")

    start = perf_counter()
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        # Use the map method to apply load_url to each URL
        results = executor.map(load_url, urls)  # does not block

        # Process the results and times
        times = [result for result in results]  # blocks

    logging.info(f"Australian animals loaded! PID: {os.getpid()}")

    times.append(cpu_bound_task(counts))

    finish = perf_counter()
    logging.info(f"PID: {os.getpid()} time - {round(finish - start, 4)}")

    return times


def main():

    n_tasks = 20 + 4
    max_workers = 4

    start = time()
    # Use ProcessPoolExecutor to manage concurrency
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks
        results = executor.map(task, URLS)  # does not block

        # Retrieve results
        times = [result for result in results]  # blocks
    end = time()

    total_time = end - start
    logging.info(f"Total time: {total_time}")

    # logging.info(f"len(animals) = {len(animals)}")

    # Just some processing for chart
    times = flaten_list_of_lists(times)
    start_points, end_points = postprocess_times(times)

    barh(
        title="Parallel execution, 4 workers, I/O-bound + CPU-bound",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path(
            "process-pool-executor/images/ex5_ProcessPoolExecutor.png"
        ),
        n=n_tasks,  # number of tasks
        color=(0.5, 0.2, 0.9, 0.8),
        secs=ceil(total_time),
    )


if __name__ == "__main__":
    logging.info("Init parallel program")
    main()
    logging.info("Finish parallel program")
