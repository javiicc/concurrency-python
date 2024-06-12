import matplotlib.pyplot as plt
import numpy as np


def barh(
    title: str,
    start_points: list[float],
    end_points: list[float],
    path: str,
    n: int = 10,
    secs: int = 11,
    color=(0.2, 0.65, 1, 0.8),
) -> None:

    with plt.style.context("dark_background"):
        plt.figure(figsize=(10, 4.5))

        plt.barh(
            range(n),
            left=start_points,
            width=np.array(end_points) - np.array(start_points),
            color=color,
            align="center",
        )

        plt.title(title)
        plt.ylabel("tasks")
        plt.xlabel("time (in secs)")
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.yticks(range(n))
        plt.xticks(range(secs))

    plt.savefig(path)
