from . import data_classes, graph

from collections import deque


class Pathfinder:
    """Calculates the available routes and their costs on graph"""

    def __init__(self, graphic_object: graph.Graph) -> None:
        self.graph = graphic_object

    def find_route(
        self, start_zone: data_classes.Zone, end_zone: data_classes.Zone
    ) -> list[data_classes.Zone]:
        discovered_zone_names: set[str] = set()
        discovered_zone_names.add(start_zone.name)

        zones_to_visit: deque[data_classes.Zone] = deque()
        zones_to_visit.append(start_zone)

        path_family_tree: dict[str, data_classes.Zone | None] = {}
        path_family_tree[start_zone.name] = None

        while len(zones_to_visit) != 0:
            current_zone = zones_to_visit.popleft()

            if current_zone == end_zone:
                break

            current_neighbors = self.graph.get_neighbors(current_zone.name)

            for neighbor in current_neighbors:
                if neighbor.name not in discovered_zone_names:
                    zones_to_visit.append(neighbor)
                    discovered_zone_names.add(neighbor.name)
                    path_family_tree[neighbor.name] = current_zone

        if end_zone.name not in path_family_tree.keys():
            raise ValueError(
                f"Invalid route. Cannot reach the end zone named as "
                f"{end_zone.name}"
            )
        else:
            last_zone: data_classes.Zone | None = end_zone
            backtrace_path_list: list[data_classes.Zone] = []

            while last_zone is not None:
                backtrace_path_list.append(last_zone)
                last_zone = path_family_tree[last_zone.name]

        solved_route = list(reversed(backtrace_path_list))

        return solved_route
