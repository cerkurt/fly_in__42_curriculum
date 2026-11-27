from . import data_classes


class Graph:
    """Manages the Zone and Connection objects and their neighborhood
    relationship."""

    connections_by_zone: dict[str, list[data_classes.Connection]]
    zones_dictionary: dict[str, data_classes.Zone]

    def __init__(self) -> None:
        self.connections_by_zone = {}
        self.zones_dictionary = {}

    def add_zone(self, zone: data_classes.Zone) -> None:
        if zone.name not in self.zones_dictionary.keys():
            self.zones_dictionary[zone.name] = zone
        else:
            raise ValueError(f"Zone with {zone.name!r} name already exists!")

    def get_zone(self, zone_name: str) -> data_classes.Zone | None:
        return self.zones_dictionary.get(zone_name)

    def get_connections(self, zone_name: str) -> list[data_classes.Connection]:
        result_list: list[data_classes.Connection] = []
        if zone_name not in self.connections_by_zone.keys():
            return result_list
        else:
            return self.connections_by_zone[zone_name]

    def add_connection(
        self, connection_object: data_classes.Connection
    ) -> None:
        zone_key_1 = connection_object.zone_a.name
        zone_key_2 = connection_object.zone_b.name

        if zone_key_1 not in self.connections_by_zone:
            self.connections_by_zone[zone_key_1] = []
        self.connections_by_zone[zone_key_1].append(connection_object)

        if zone_key_2 not in self.connections_by_zone:
            self.connections_by_zone[zone_key_2] = []
        self.connections_by_zone[zone_key_2].append(connection_object)

    def get_neighbors(self, zone_name: str) -> list[data_classes.Zone]:
        connections_of_zone = self.get_connections(zone_name)

        neighbor_list = []

        for connection in connections_of_zone:
            if connection.zone_a.name == zone_name:
                neighbor_list.append(connection.zone_b)
            elif connection.zone_b.name == zone_name:
                neighbor_list.append(connection.zone_a)

        return neighbor_list
