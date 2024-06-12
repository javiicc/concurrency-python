import concurrent.futures
from time import perf_counter, time
import urllib.request
import logging

from concurrency.utils import get_saving_path, postprocess_times
from concurrency.visualize import barh


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


URLS = [
    "https://en.wikipedia.org/wiki/Emu",
    "https://en.wikipedia.org/wiki/Wombat",
    "https://en.wikipedia.org/wiki/Kangaroo",
    "https://en.wikipedia.org/wiki/Platypus",
    "https://en.wikipedia.org/wiki/Koala",
    "https://en.wikipedia.org/wiki/Tasmanian_devil",
    "https://en.wikipedia.org/wiki/Echidna",
    "https://en.wikipedia.org/wiki/Dingo",
    "https://en.wikipedia.org/wiki/Kookaburra",
    "https://en.wikipedia.org/wiki/Wallaby",
    "https://en.wikipedia.org/wiki/Macrotis",
    "https://en.wikipedia.org/wiki/Quokka",
    "https://en.wikipedia.org/wiki/Cassowary",
    "https://en.wikipedia.org/wiki/Sugar_glider",
    "https://en.wikipedia.org/wiki/Laughing_kookaburra",
    "https://en.wikipedia.org/wiki/Rainbow_lorikeet",
    "https://en.wikipedia.org/wiki/Coastal_taipan",
    "https://en.wikipedia.org/wiki/Mistletoebird",
    "https://en.wikipedia.org/wiki/Thylacine",
    "https://en.wikipedia.org/wiki/Quoll",
]

results = []  # threads from the same process share data
animals = {}


# I/O-bound operation
def load_url(url: str) -> tuple[float]:
    """Retrieve a single page and return start and finish times."""
    start = perf_counter()
    with urllib.request.urlopen(url) as conn:
        animals[url] = conn.read()
    finish = perf_counter()
    return start, finish


def asynchronous_load_australian_animals() -> None:
    start = time()
    # Use ThreadPoolExecutor to manage concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Use the submit method to apply load_url to each URL
        results = [executor.submit(load_url, url) for url in URLS]

        # Process the results and times
        times = [result.result() for result in concurrent.futures.as_completed(results)]
        start_points, end_points = postprocess_times(times)
    end = time()

    total_time = round(end - start) + 1

    barh(
        title="Asynchronous execution, 5 threads, I/O-bound tasks, Australian animals",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path("thread-pool-executor/images/ThreadPoolExecutor_ex2.png"),
        n=len(URLS),
        secs=total_time,
    )


if __name__ == "__main__":
    logging.info("Init asynchronous tasks")
    asynchronous_load_australian_animals()
    logging.info(f"len(animals): {len(animals)}")
    logging.info("Finish asynchronous tasks")
