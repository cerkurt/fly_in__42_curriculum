#  run the file with 'uv run python -m pytest -s -q' from the root

from source import parser, graph, pathfinder

parser_instance = parser.Parser()
graph_instance = graph.Graph()


def test_route_finder() -> None:
    print("==== Test pathfinder route find ====\n")
    parsed_map = parser_instance.parse_map(
        "/Users/ceren/Desktop/Codam/Milestone_03"
        "/fly_in/maps/hard/02_capacity_hell.txt"
    )

    drone_count, map_graph = parsed_map
    pathfinder_instance = pathfinder.Pathfinder(map_graph)

    for zone in map_graph.zones_dictionary.values():
        if zone.hub_type == "start_hub":
            start_zone = zone
        elif zone.hub_type == "end_hub":
            end_zone = zone

    solved_path = pathfinder_instance.find_route(start_zone, end_zone)

    print(*solved_path, sep="\n")
