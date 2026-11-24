from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import dataclass


class HubType(str, Enum):
    """Define the role of a hub on the map."""

    START = "start_hub"
    REGULAR = "hub"
    END = "end_hub"


class ZoneType(str, Enum):
    """Define the movement permissions of a zone."""

    # Standard zone with 1 turn movement cost. (default)
    NORMAL = "normal"
    # Inaccessible zone. Drones must not enter or pass through this zone.
    # Any path using it is invalid.
    BLOCKED = "blocked"
    # A sensitive or dangerous zone. Movement to this zone costs 2 turns.
    RESTRICTED = "restricted"
    # A preferred zone. Movement to this zone costs 1 turn but should be
    # prioritized in pathfinding.
    PRIORITY = "priority"


class Zone(BaseModel):
    """Contains the information such as: name, coordinate, type and
    max_drones."""

    name: str
    coordinate: tuple[int, int]
    hub_type: HubType
    zone_type: ZoneType = ZoneType.NORMAL
    max_drones: int | None = Field(default=1, gt=0)
    color: str | None = None


class Connection(BaseModel):
    """Contains the information about the connection between two zones and
    their capacity."""

    zone_a: Zone
    zone_b: Zone
    max_link_capacity: int = Field(default=1, gt=0)


@dataclass
class Drone:
    """Contains the ID, position, status and the route assigned to it."""

    drone_id: int
    position: Zone | Connection
    transit_destination: Zone | None = None
    route: list[Zone] | None = None


class Graph:
    """Manages the Zone and Connection objects and their neighborhood
    relationship."""


class Parser:
    """Reads the text files, validates and turns them into objects."""


class Pathfinder:
    """Calculates the available routes and their costs on graph"""


class SimulationEngine:
    """Manages the tours, drone movements, waits and capacity controls."""
