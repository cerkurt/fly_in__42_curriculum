from pydantic import BaseModel
from typing import Literal
from . import data_classes, graph


class DroneTurnState(BaseModel):
    drone_id: int
    current_location: data_classes.Zone | data_classes.Connection
    current_situation: Literal["moved", "in_transit", "waiting", "delivered"]


class TurnResult(BaseModel):
    drone_states: list[DroneTurnState]
    turn_round_number: int


class SimulationEngine:
    """Manages the tours, drone movements, waits and capacity controls."""

    def __init__(
        self,
        graphic_object: graph.Graph,
        drone_list: list[data_classes.Drone],
        end_zone: data_classes.Zone,
    ) -> None:
        self.round_counter = 0
        self.graph = graphic_object
        self.drone_list = drone_list
        self.end_zone = end_zone

    def run_move_turn(self) -> TurnResult:
        raise NotImplementedError
