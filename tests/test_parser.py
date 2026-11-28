#  run the file with 'uv run python -m pytest -s -q' from the root

from source import parser

import pytest

parser_instance = parser.Parser()


def test_parse_linear_map() -> None:
    print("==== Test parse linear map ====\n")
    parsed_map = parser_instance.parse_map(
        "/Users/ceren/Desktop/Codam/Milestone_03"
        "/fly_in/maps/easy/01_linear_path.txt"
    )

    drone_count, map_graph = parsed_map

    for zone_name in map_graph.zones_dictionary.keys():
        print(f"Zone name: {zone_name}")

        connections = map_graph.get_connections(zone_name)
        for connection in connections:
            print(
                f"Connections: "
                f"{connection.zone_a.name} - {connection.zone_b.name}"
            )

        neighbors = map_graph.get_neighbors(zone_name)
        neighbor_name_list: list[str] = []
        for neighbor in neighbors:
            neighbor_name_list.append(neighbor.name)
            print(f"Neighbors: {", ".join(neighbor_name_list)}")

        print()


def test_parse_metadata_with_whitespace() -> None:
    print("==== Test parse metadata with space ====\n")
    parsed_map = parser_instance.parse_map(
        "/Users/ceren/Desktop/Codam/Milestone_03/"
        "fly_in/maps/easy/02_simple_fork.txt"
    )

    drone_count, map_graph = parsed_map
    print(f"Map drone count: {drone_count}")

    for zone in map_graph.zones_dictionary.values():
        print(
            f"Zone name: {zone.name}\n"
            f"Coordinate: {zone.coordinate}\n"
            f"Hub type: {zone.hub_type}\n"
            f"Zone type: {zone.zone_type}\n"
            f"Max drones: {zone.max_drones}\n"
            f"Color: {zone.color}\n"
        )


def test_reject_regular_hub_with_invalid_capacity() -> None:
    with pytest.raises(ValueError) as exc_info:
        parser_instance.parse_map(
            "/Users/ceren/Desktop/Codam/Milestone_03"
            "/fly_in/maps/easy/03_basic_capacity.txt"
        )

    assert "Max drone count must be a positive integer" in str(exc_info.value)
