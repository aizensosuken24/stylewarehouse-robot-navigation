"""Tests for Robot and FleetManager."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from src.robot.robot import Robot, RobotStatus
from src.robot.fleet import FleetManager


@pytest.fixture
def robot():
    return Robot("R1", "Alpha", x=0, y=0, battery=100.0)


@pytest.fixture
def fleet():
    fm = FleetManager()
    fm.add_robot(Robot("R1", "Alpha", x=0, y=0, battery=100.0))
    fm.add_robot(Robot("R2", "Beta", x=10, y=10, battery=85.0))
    fm.add_robot(Robot("R3", "Gamma", x=5, y=5, battery=15.0))  # Low battery
    return fm


class TestRobot:
    def test_initial_state(self, robot):
        assert robot.id == "R1"
        assert robot.battery == 100.0
        assert robot.status == RobotStatus.IDLE
        assert robot.position == (0, 0)
        assert robot.is_available

    def test_move_drains_battery(self, robot):
        path = [(0, 0), (1, 0), (2, 0), (3, 0)]
        robot.move_to(path)
        assert robot.battery < 100.0
        assert robot.position == (3, 0)
        assert robot.status == RobotStatus.IDLE

    def test_move_skip_starting_cell(self, robot):
        path = [(0, 0), (1, 0)]
        initial_battery = robot.battery
        robot.move_to(path)
        assert robot.battery == initial_battery - 0.5
        assert robot.total_distance == 1.0

    def test_move_empty_path(self, robot):
        result = robot.move_to([])
        assert result is True
        assert robot.position == (0, 0)

    def test_insufficient_battery_move(self):
        r = Robot("R99", "Low", battery=0.1)
        result = r.move_to([(0, 0), (1, 0), (2, 0)])
        assert result is False
        assert r.status == RobotStatus.ERROR

    def test_pick_item(self, robot):
        result = robot.pick_item("ITM001")
        assert result is True
        assert robot.total_picks == 1
        assert robot.battery < 100.0

    def test_charge(self, robot):
        robot.battery = 30.0
        robot.charge(100.0)
        assert robot.battery == 100.0
        assert robot.status == RobotStatus.IDLE

    def test_low_battery_flag(self):
        r = Robot("R2", "Beta", battery=15.0)
        assert r.is_low_battery
        assert not r.is_available

    def test_to_dict(self, robot):
        d = robot.to_dict()
        assert d["id"] == "R1"
        assert "battery" in d
        assert "status" in d
        assert "x" in d and "y" in d

    def test_error_and_clear(self, robot):
        robot.set_error("Test error")
        assert robot.status == RobotStatus.ERROR
        robot.clear_error()
        assert robot.status == RobotStatus.IDLE
        assert robot.error_message is None


class TestFleetManager:
    def test_get_robot(self, fleet):
        r = fleet.get_robot("R1")
        assert r is not None
        assert r.name == "Alpha"

    def test_get_missing_robot(self, fleet):
        assert fleet.get_robot("R99") is None

    def test_get_available_robot(self, fleet):
        r = fleet.get_available_robot()
        assert r is not None
        assert r.is_available

    def test_nearest_available_robot(self, fleet):
        # R3 has low battery so shouldn't be returned
        r = fleet.get_nearest_available_robot(9, 9)
        assert r is not None
        assert r.id == "R2"  # closest with good battery

    def test_fleet_summary(self, fleet):
        summary = fleet.fleet_summary()
        assert summary["total"] == 3
        assert "average_battery" in summary
        assert summary["low_battery"] == 1

    def test_all_robots_status(self, fleet):
        statuses = fleet.all_robots_status()
        assert len(statuses) == 3
