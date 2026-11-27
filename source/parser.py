from . import data_classes, graph

import re
from enum import Enum


class RegularExpressions(Enum):
    METADATA_COMPLETE_REGEX_PATTERN = (
        r"(?:zone\s*=\s*(?:priority|normal|blocked|restricted)|color"
        r"\s*=\s*[A-Za-z]+|max_drones\s*=\s*-?\d+)"
    )

    COMBINED_METADATA_REGEX_SEARCH = re.compile(
        rf"\s*{METADATA_COMPLETE_REGEX_PATTERN}(?:\s+"
        rf"{METADATA_COMPLETE_REGEX_PATTERN})*\s*"
    )

    METADATA_DICT_SPLIT_PATTERN = re.compile(r"([a-zA-Z_]+)\s*=\s*([^\s]+)")

    HUB_SEARCH_PATTERN = re.compile(
        r"(start_hub|hub|end_hub):\s*"
        r"(?=[A-Za-z0-9_]*[A-Za-z])([A-Za-z0-9_]+)\s+"
        r"(-?\d+)\s+(-?\d+)(?:\s*(\[[^\]]+\]))?"
    )

    LINK_CAPACITY_PATTERN = re.compile(
        r"\s*max_link_capacity\s*=\s*(-?\d+)\s*"
    )

    CONNECTION_NAME_PATTERN = re.compile(
        r"connection:\s*"
        r"(?=[A-Za-z0-9_]*[A-Za-z])([A-Za-z0-9_]+)-"
        r"(?=[A-Za-z0-9_]*[A-Za-z])([A-Za-z0-9_]+)"
        r"(?:\s*(\[[^\]]+\]))?"
    )

    DRONE_NB_SEARCH_PATTERN = re.compile(r"\s*(nb_drones:\s+)(\d+)\s*")

    def __init__(self, raw_or_compiled: str | re.Pattern[str]) -> None:
        if isinstance(raw_or_compiled, re.Pattern):
            self.pattern: re.Pattern[str] = raw_or_compiled
        else:
            self.pattern = re.compile(raw_or_compiled)

    def fullmatch(self, text: str) -> re.Match[str] | None:
        return self.pattern.fullmatch(text)


class Parser:
    """Reads the text files, validates and turns them into objects."""

    def parse_link_capacity(self, raw_string: str) -> int:
        inside_the_brackets = raw_string.strip()[1:-1]

        match_the_pattern = RegularExpressions.LINK_CAPACITY_PATTERN.fullmatch(
            inside_the_brackets
        )

        if not match_the_pattern:
            raise ValueError(f"Invalid link capacity format: {raw_string}.")

        connection_link_capacity = int(match_the_pattern.group(1))
        if connection_link_capacity <= 0:
            raise ValueError(
                f"Max link capacity value must be a positive integer. "
                f"Current input value: {connection_link_capacity!r}."
            )

        return connection_link_capacity

    def parse_connection_info(self, map_line: str) -> tuple[str, str, int]:
        cleaned_line = map_line.strip()

        match_the_pattern = (
            RegularExpressions.CONNECTION_NAME_PATTERN.fullmatch(cleaned_line)
        )
        if not match_the_pattern:
            raise ValueError(f"Invalid text format for map as {map_line!r}.")

        zone_1, zone_2, capacity_metadata = match_the_pattern.groups()
        if capacity_metadata is None:
            capacity = 1
        else:
            capacity = self.parse_link_capacity(capacity_metadata)

        return zone_1, zone_2, capacity

    def is_valid_connection(
        self, map_line: str, graphic_info: graph.Graph
    ) -> None:
        connection_info = self.parse_connection_info(map_line)

        first_zone_name, second_zone_name, connection_link = connection_info

        first_zone = graphic_info.get_zone(first_zone_name)
        second_zone = graphic_info.get_zone(second_zone_name)

        if (first_zone is None) and (second_zone is None):
            raise ValueError(
                f"Invalid zone names for the connections "
                f"{first_zone_name!r}, {second_zone_name!r}."
            )
        elif first_zone is None:
            raise ValueError(
                f"Invalid zone name for the connection {first_zone_name!r}."
            )
        elif second_zone is None:
            raise ValueError(
                f"Invalid zone name for the connection {second_zone_name!r}."
            )

        neighbors = graphic_info.get_neighbors(first_zone_name)
        if second_zone in neighbors:
            raise ValueError(
                f"Invalid connection attempt as duplicate connection between "
                f"{first_zone_name!r} and {second_zone_name!r}."
            )

        new_connection = data_classes.Connection(
            zone_a=first_zone,
            zone_b=second_zone,
            max_link_capacity=connection_link,
        )

        graphic_info.add_connection(new_connection)

    def parse_zone_metadata(
        self, raw_string: str | None, hub_type: data_classes.HubType
    ) -> dict[str, str | int]:
        if not raw_string:
            return {}

        inside_brackets = raw_string.strip()[1:-1]

        meta_match = (
            RegularExpressions.COMBINED_METADATA_REGEX_SEARCH.fullmatch(
                inside_brackets
            )
        )
        if not meta_match:
            raise ValueError(f"Invalid metadata format as {raw_string!r}.")

        result_dict: dict[str, str | int] = {}

        for (
            dict_pair
        ) in RegularExpressions.METADATA_DICT_SPLIT_PATTERN.pattern.finditer(
            inside_brackets
        ):
            key, value = dict_pair.groups()
            if key == "zone":
                result_dict["zone"] = value

            elif key == "color":
                result_dict["color"] = value.lower()

            elif key == "max_drones":
                if hub_type in [
                    data_classes.HubType.START,
                    data_classes.HubType.END,
                ]:
                    continue

                elif hub_type == data_classes.HubType.REGULAR:
                    int_value = int(value)
                    if int_value <= 0:
                        raise ValueError(
                            f"Max drone count must be a positive integer.\n"
                            f"Current input value: {value}."
                        )
                    result_dict["max_drones"] = int_value

        return result_dict

    def parse_zone_info(self, map_line: str) -> data_classes.Zone:
        cleaned_line = map_line.strip()

        match_to_pattern = RegularExpressions.HUB_SEARCH_PATTERN.fullmatch(
            cleaned_line
        )

        if not match_to_pattern:
            raise ValueError(
                f"Invalid hub entry format aa {map_line!r}."
                f"Hubs types should be one of these options: "
                f"start_hub / hub / end_hub."
            )

        hub_type, zone_name, coord_x, coord_y, zone_metadata = (
            match_to_pattern.groups()
        )

        hub_type = data_classes.HubType(hub_type)
        zone_type = data_classes.ZoneType.NORMAL

        if hub_type in [data_classes.HubType.START, data_classes.HubType.END]:
            drone_count = None
        elif hub_type == data_classes.HubType.REGULAR:
            drone_count = 1

        color_info: str | None = None
        parsed_metadata = self.parse_zone_metadata(zone_metadata, hub_type)

        for key, value in parsed_metadata.items():
            if key == "zone":
                zone_type = data_classes.ZoneType(value)
            elif key == "color" and isinstance(value, str):
                color_info = value
            elif key == "max_drones" and isinstance(value, int):
                drone_count = value
            else:
                raise ValueError(
                    f"Invalid metadata entry as {parsed_metadata!r}."
                )

        new_zone = data_classes.Zone(
            name=zone_name,
            coordinate=(int(coord_x), int(coord_y)),
            hub_type=data_classes.HubType(hub_type),
            zone_type=zone_type,
            max_drones=drone_count,
            color=color_info,
        )

        return new_zone

    # tuple[graph.Graph, int]
    def parse_map(self, path: str) -> tuple[int, graph.Graph]:
        with open(path, "r") as map_file:
            text_lines = map_file.readlines()

        if not text_lines:
            raise ValueError("Map file cannot be empty.")

        map_graph = graph.Graph()

        drone_count = None
        for line_number, line in enumerate(text_lines, start=1):
            raw_line = line.strip()
            if raw_line.startswith("#") or len(raw_line) == 0:
                continue

            if drone_count is None:
                match_to_pattern = (
                    RegularExpressions.DRONE_NB_SEARCH_PATTERN.fullmatch(
                        raw_line
                    )
                )
                if not match_to_pattern:
                    raise ValueError(
                        f"Map file must always start with the drone count "
                        f"info at line {line_number}.\n"
                        f"Current start: {raw_line}."
                    )

                else:
                    drone_count = int(match_to_pattern.group(2))
                    if drone_count == 0:
                        raise ValueError(
                            f"Invalid value on line {line_number}"
                            f" in map file.\nMap drone count must be "
                            f"a positive integer value.\n"
                            f"Current input: {drone_count}."
                        )
                    continue

            if raw_line.startswith(("start_hub", "hub", "end_hub")):
                try:
                    parsed_new_zone = self.parse_zone_info(raw_line)
                    map_graph.add_zone(parsed_new_zone)

                except ValueError as e:
                    raise ValueError(
                        f"[{type(e).__name__}]: {e}.\n"
                        f"Invalid map input at line "
                        f"{line_number}."
                    ) from e

            elif raw_line.startswith("connection"):
                try:
                    self.is_valid_connection(raw_line, map_graph)
                except ValueError as e:
                    raise ValueError(
                        f"[{type(e).__name__}]: {e}.\n"
                        f"Invalid map input at line "
                        f"{line_number}."
                    ) from e

            else:
                raise ValueError(
                    f"Unrecognized map entry at line {line_number} as "
                    f"{raw_line}."
                )

        if drone_count is None:
            raise ValueError(
                "Number of drones is not specified in the map file."
            )

        start_hub_count = 0
        end_hub_count = 0
        for zone in map_graph.zones_dictionary.values():
            if zone.hub_type == data_classes.HubType.START:
                start_hub_count += 1
            elif zone.hub_type == data_classes.HubType.END:
                end_hub_count += 1

        if start_hub_count != 1:
            raise ValueError(
                f"Invalid input in map file. Maps can have only 1 start hub.\n"
                f"Current count: {start_hub_count}."
            )

        if end_hub_count != 1:
            raise ValueError(
                f"Invalid input in map file. Maps can have only 1 end hub.\n"
                f"Current count: {end_hub_count}."
            )

        return drone_count, map_graph
