"""
Navigation module: A* pathfinding for warehouse robot navigation.
"""
import heapq
import math
from typing import Iterable, List, Optional, Set, Tuple


class Node:
    """Represents a grid node for A* search."""

    def __init__(self, x: int, y: int, g: float = 0, h: float = 0, parent=None):
        self.x = x
        self.y = y
        self.g = g          # Cost from start
        self.h = h          # Heuristic to goal
        self.f = g + h      # Total estimated cost
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Node({self.x}, {self.y}, f={self.f:.2f})"


class AStarPathfinder:
    """
    A* pathfinding algorithm for warehouse grid navigation.
    Supports 4-directional and 8-directional movement.
    """

    DIRECTIONS_4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    DIRECTIONS_8 = [(0, 1), (1, 0), (0, -1), (-1, 0),
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(self, grid_width: int, grid_height: int,
                 obstacles: Optional[Iterable[Tuple[int, int]]] = None,
                 allow_diagonal: bool = False):
        self.width = grid_width
        self.height = grid_height
        self.obstacles: Set[Tuple[int, int]] = obstacles or set()
        self.allow_diagonal = allow_diagonal
        self.directions = self.DIRECTIONS_8 if allow_diagonal else self.DIRECTIONS_4

    def set_obstacles(self, obstacles: Iterable[Tuple[int, int]]):
        """Update the obstacle set."""
        self.obstacles = set(obstacles)

    def add_obstacle(self, x: int, y: int):
        self.obstacles.add((x, y))

    def remove_obstacle(self, x: int, y: int):
        self.obstacles.discard((x, y))

    def heuristic(self, a: Node, b: Node) -> float:
        """Heuristic function (Manhattan or Octile depending on diagonal setting)."""
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        if self.allow_diagonal:
            # Octile distance
            return (dx + dy) + (math.sqrt(2) - 2.0) * min(dx, dy)
        else:
            # Manhattan distance
            return dx + dy

    def is_valid(self, x: int, y: int) -> bool:
        """Check if a cell is within bounds and not an obstacle."""
        return (0 <= x < self.width and
                0 <= y < self.height and
                (x, y) not in self.obstacles)

    def find_path(self, start: Tuple[int, int],
                  goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Find shortest path from start to goal using A*.
        Returns list of (x, y) tuples or None if no path exists.
        """
        sx, sy = start
        gx, gy = goal

        if not self.is_valid(sx, sy) or not self.is_valid(gx, gy):
            return None

        if start == goal:
            return [start]

        start_node = Node(sx, sy, g=0, h=0)
        goal_node = Node(gx, gy)
        start_node.h = self.heuristic(start_node, goal_node)
        start_node.f = start_node.h

        open_heap: List[Node] = [start_node]
        open_set: dict = {(sx, sy): start_node}
        closed_set: Set[Tuple[int, int]] = set()

        while open_heap:
            current = heapq.heappop(open_heap)
            pos = (current.x, current.y)

            if pos in closed_set:
                continue

            if pos == (gx, gy):
                return self._reconstruct_path(current)

            closed_set.add(pos)

            for dx, dy in self.directions:
                nx, ny = current.x + dx, current.y + dy
                npos = (nx, ny)

                if not self.is_valid(nx, ny) or npos in closed_set:
                    continue

                move_cost = math.sqrt(2) if (dx != 0 and dy != 0) else 1.0
                tentative_g = current.g + move_cost

                if npos in open_set and open_set[npos].g <= tentative_g:
                    continue

                neighbor = Node(nx, ny, g=tentative_g, parent=current)
                neighbor.h = self.heuristic(neighbor, goal_node)
                neighbor.f = neighbor.g + neighbor.h

                heapq.heappush(open_heap, neighbor)
                open_set[npos] = neighbor

        return None  # No path found

    def _reconstruct_path(self, node: Node) -> List[Tuple[int, int]]:
        """Reconstruct path by backtracking parent nodes."""
        path = []
        current = node
        while current:
            path.append((current.x, current.y))
            current = current.parent
        return list(reversed(path))

    def path_length(self, path: List[Tuple[int, int]]) -> float:
        """Calculate total path length."""
        if not path or len(path) < 2:
            return 0.0
        total = 0.0
        for i in range(1, len(path)):
            dx = path[i][0] - path[i-1][0]
            dy = path[i][1] - path[i-1][1]
            total += (dx*dx + dy*dy) ** 0.5
        return total
