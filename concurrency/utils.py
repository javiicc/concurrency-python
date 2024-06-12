import os


def get_saving_path(path: str) -> str:
    cwd = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(cwd, path)


def postprocess_times(times: list[tuple[float]]) -> tuple[list[float]]:
    """Remove the start time of the first task from all tasks so
    that the overall start time is 0. Then split the start and end
    points to make it easier to represent later."""
    init_time = times[0][0]

    start_points, end_points = list(), list()
    for interval in times:
        start_points.append(interval[0] - init_time)
        end_points.append(interval[1] - init_time)

    return start_points, end_points


def flaten_list_of_lists(times: list[list]) -> tuple[list[float]]:
    return [time for time_list in times for time in time_list]
