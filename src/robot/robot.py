"""
Robot module: Represents a warehouse robot with state, movement, and battery management.
"""
from typing import List, Tuple, Optional
from enum import Enum
import time


class RobotStatus(str, Enum):
    IDLE = "idle"
    MOVING = "moving"
    PICKING = "picking"
    CHARGING = "charging"
    ERROR = "error"
    RETURNING = "returning"


class Robot:
    """
    Warehouse robot with position tracking, battery management,
    and task execution.
    """

    BATTERY_PER_MOVE = 0.5       # % battery consumed per grid cell
    BATTERY_PER_PICK = 1.0       # % battery consumed per pick action
    BATTERY_CHARGE_RATE = 2.0    # % battery charged per second (simulated)
    LOW_BATTERY_THRESHOLD = 20.0 # % battery to trigger return-to-charge

    def __init__(self, robot_id: str, name: str,
                 x: int = 0, y: int = 0, battery: float = 100.0):
        self.id = robot_id
        self.name = name
        self.x = x
        self.y = y
        self.battery = min(100.0, max(0.0, battery))
        self.status = RobotStatus.IDLE
        self.current_path: List[Tuple[int, int]] = []
        self.current_task: Optional[dict] = None
        self.completed_tasks: List[dict] = []
        self.error_message: Optional[str] = None
        self.total_distance: float = 0.0
        self.total_picks: int = 0

    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)

    @property
    def is_low_battery(self) -> bool:
        return self.battery <= self.LOW_BATTERY_THRESHOLD

    @property
    def is_available(self) -> bool:
        return self.status in (RobotStatus.IDLE,) and not self.is_low_battery

    def move_to(self, path: List[Tuple[int, int]]) -> bool:
        """
        Simulate movement along a path.
        Deducts battery per step.
        Returns True if movement completed successfully.
        """
        if not path:
            return True

        # Skip the first element if the robot is already at that position
        actual_steps = path
        if path[0] == (self.x, self.y):
            actual_steps = path[1:]

        required_battery = len(actual_steps) * self.BATTERY_PER_MOVE
        if self.battery < required_battery:
            self.status = RobotStatus.ERROR
            self.error_message = "Insufficient battery for path"
            return False

        self.status = RobotStatus.MOVING
        self.current_path = list(path)

        for step in actual_steps:
            self.x, self.y = step
            self.battery = max(0.0, self.battery - self.BATTERY_PER_MOVE)
            self.total_distance += 1.0

        self.current_path = []
        self.status = RobotStatus.IDLE
        return True

    def pick_item(self, item_id: str) -> bool:
        """
        Simulate picking an item at current location.
        """
        if self.battery < self.BATTERY_PER_PICK:
            self.error_message = "Insufficient battery to pick item"
            return False

        self.status = RobotStatus.PICKING
        self.battery = max(0.0, self.battery - self.BATTERY_PER_PICK)
        self.total_picks += 1
        self.status = RobotStatus.IDLE
        return True

    def charge(self, target_level: float = 100.0):
        """Charge robot to target battery level."""
        self.status = RobotStatus.CHARGING
        self.battery = min(100.0, target_level)
        if self.battery >= 100.0:
            self.status = RobotStatus.IDLE

    def set_error(self, message: str):
        self.status = RobotStatus.ERROR
        self.error_message = message

    def clear_error(self):
        self.status = RobotStatus.IDLE
        self.error_message = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "battery": round(self.battery, 1),
            "status": self.status.value,
            "is_low_battery": self.is_low_battery,
            "is_available": self.is_available,
            "total_distance": round(self.total_distance, 1),
            "total_picks": self.total_picks,
            "error_message": self.error_message,
            "current_task": self.current_task
        }

    def __repr__(self):
        return f"Robot({self.id}, {self.name}, pos=({self.x},{self.y}), battery={self.battery:.0f}%)"
