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

animals = {}


# Retrieve a single page and report the URL and contents
# I/O-bound operation
def load_url(url, timeout):
    start = perf_counter()
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        animals[url] = conn.read()
    finish = perf_counter()
    return start, finish


def synchronous_load_australian_animals():
    """Load Australian animals, measure time and generate a graph."""
    start = time()
    times = [load_url(url, 60) for url in URLS]
    start_points, end_points = postprocess_times(times)
    end = time()

    total_time = round(end - start) + 1

    barh(
        title="Synchronous execution, main thread, I/O-bound tasks, Australian animals",
        start_points=start_points,
        end_points=end_points,
        path=get_saving_path(
            "threading/images/load_australian_animals_synchronously.png"
        ),
        n=len(URLS),
        secs=total_time,
    )


if __name__ == "__main__":
    logging.info("Init synchronous tasks")
    synchronous_load_australian_animals()
    logging.info(f"len(animals): {len(animals)}")
    logging.info("Finish synchronous tasks")
