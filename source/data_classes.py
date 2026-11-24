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

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone(BaseModel):
    """Contains the information such as: name, coordinate, type and
    max_drones."""

    name: str = Field(...)
    coordinate: tuple[int, int] = Field(...)
    hub_type: HubType = Field(...)
    zone_type: ZoneType = ZoneType.NORMAL
    max_drones: int | None = Field(default=1, gt=0)
    color: str | None = None


class Connection(BaseModel):
    """Contains the information about the connection between two zones and
    their capacity."""


@dataclass
class Drone:
    """Contains the ID, position, status and the route assigned to it."""


class Graph:
    """Manages the Zone and Connection objects and their neighborhood
    relationship."""


class Parser:
    """Reads the text files, validates and turns them into objects."""


class Pathfinder:
    """Calculates the available routes and their costs on graph"""


class SimulationEngine:
    """Manages the tours, drone movements, waits and capacity controls."""
