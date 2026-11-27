from . import data_classes, graph


class Pathfinder:
    """Calculates the available routes and their costs on graph"""

    def __init__(self, graphic_object: graph.Graph) -> None:
        self.graph = graphic_object

    def find_route(
        self, start_zone: data_classes.Zone, end_zone: data_classes.Zone
    ) -> list[data_classes.Zone]:
        raise NotImplementedError
