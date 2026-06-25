"""
Fleet manager: manages multiple robots and task assignment.
"""
from typing import List, Optional, Dict
from .robot import Robot, RobotStatus


class FleetManager:
    """
    Manages a fleet of warehouse robots.
    Handles task assignment and robot status tracking.
    """

    def __init__(self):
        self.robots: Dict[str, Robot] = {}

    def add_robot(self, robot: Robot):
        self.robots[robot.id] = robot

    def remove_robot(self, robot_id: str):
        self.robots.pop(robot_id, None)

    def get_robot(self, robot_id: str) -> Optional[Robot]:
        return self.robots.get(robot_id)

    def get_available_robot(self) -> Optional[Robot]:
        """Return first available robot."""
        for robot in self.robots.values():
            if robot.is_available:
                return robot
        return None

    def get_nearest_available_robot(self,
                                    target_x: int,
                                    target_y: int) -> Optional[Robot]:
        """Return nearest available robot to target position."""
        available = [r for r in self.robots.values() if r.is_available]
        if not available:
            return None
        return min(available,
                   key=lambda r: abs(r.x - target_x) + abs(r.y - target_y))

    def all_robots_status(self) -> List[dict]:
        return [r.to_dict() for r in self.robots.values()]

    def fleet_summary(self) -> dict:
        robots = list(self.robots.values())
        return {
            "total": len(robots),
            "idle": sum(1 for r in robots if r.status == RobotStatus.IDLE),
            "moving": sum(1 for r in robots if r.status == RobotStatus.MOVING),
            "picking": sum(1 for r in robots if r.status == RobotStatus.PICKING),
            "charging": sum(1 for r in robots if r.status == RobotStatus.CHARGING),
            "error": sum(1 for r in robots if r.status == RobotStatus.ERROR),
            "low_battery": sum(1 for r in robots if r.is_low_battery),
            "average_battery": round(
                sum(r.battery for r in robots) / len(robots), 1
            ) if robots else 0
        }
