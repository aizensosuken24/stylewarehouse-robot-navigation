"""Terminal and pygame visualisers for the warehouse map."""
from __future__ import annotations

import sys
import time
from typing import List, Optional, Tuple

from src.i18n import translate
from src.utils.output import safe_print

Pos = Tuple[int, int]

_RESET = "\033[0m"
_RED = "\033[31m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_CYAN = "\033[36m"
_BOLD = "\033[1m"

_PG_COLORS = {
    0: (230, 230, 230),
    1: (100, 149, 237),
    2: (50, 205, 50),
    3: (50, 50, 50),
    4: (255, 255, 255),
}
_PG_ROBOT = (220, 20, 60)
_PG_PATH = (255, 215, 0)


def print_map(
    warehouse_map,
    robot_pos: Optional[Pos] = None,
    path: Optional[List[Pos]] = None,
    title: str = "",
    lang: str = "en",
) -> None:
    """Print a colorised ASCII map to stdout."""
    resolved_title = title or translate("app_title", lang)
    if resolved_title:
        safe_print(f"\n{_BOLD}{resolved_title}{_RESET}")

    path_set = set(path) if path else set()
    header = "    " + "".join(f"{col % 10}" for col in range(warehouse_map.cols))
    safe_print(header)

    for row in range(warehouse_map.rows):
        row_str = f"{row:3} "
        for col in range(warehouse_map.cols):
            cell = warehouse_map.grid[row][col]
            pos = (row, col)
            if robot_pos and pos == robot_pos:
                row_str += f"{_BOLD}{_RED}R{_RESET}"
            elif pos in path_set:
                row_str += f"{_YELLOW}*{_RESET}"
            elif cell == 2:
                row_str += f"{_GREEN}D{_RESET}"
            elif cell == 1:
                row_str += f"{_CYAN}S{_RESET}"
            elif cell == 3:
                row_str += "#"
            elif cell == 4:
                row_str += " "
            else:
                row_str += "."
        safe_print(row_str)
    safe_print()


def animate_path(
    warehouse_map,
    path: List[Pos],
    delay: float = 0.1,
    title: str = "",
    lang: str = "en",
) -> None:
    """Animate a robot path in the terminal."""
    for step, pos in enumerate(path):
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        step_info = translate("step_info", lang)
        try:
            safe_print(step_info.format(step=step + 1, total=len(path), pos=pos))
        except Exception:
            safe_print(f"Step {step + 1}/{len(path)}  Robot at {pos}")
        print_map(warehouse_map, robot_pos=pos, path=path[: step + 1], title=title, lang=lang)
        time.sleep(delay)


def animate_pygame(
    warehouse_map,
    path: List[Pos],
    cell_size: int = 30,
    fps: int = 10,
    title: str = "",
    lang: str = "en",
) -> None:
    """Animate a robot path in pygame when it is installed."""
    try:
        import pygame
    except ImportError:
        safe_print(translate("pygame_missing", lang))
        safe_print(translate("terminal_fallback", lang))
        animate_path(warehouse_map, path, title=title or translate("app_title", lang), lang=lang)
        return

    pygame.init()
    rows, cols = warehouse_map.rows, warehouse_map.cols
    width = cols * cell_size
    height = rows * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title or translate("app_title", lang))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 12)

    path_set: set[Pos] = set()

    for step, robot_pos in enumerate(path):
        path_set.add(robot_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((200, 200, 200))

        for row in range(rows):
            for col in range(cols):
                cell_type = warehouse_map.grid[row][col]
                color = _PG_COLORS.get(cell_type, (200, 200, 200))
                rect = (col * cell_size, row * cell_size, cell_size - 1, cell_size - 1)

                if (row, col) == robot_pos:
                    color = _PG_ROBOT
                elif (row, col) in path_set:
                    color = _PG_PATH

                pygame.draw.rect(screen, color, rect)

        step_info = translate("step_info", lang)
        try:
            label_text = step_info.format(step=step + 1, total=len(path), pos=robot_pos)
        except Exception:
            label_text = f"Step {step + 1}/{len(path)}  pos={robot_pos}"
        label = font.render(label_text, True, (0, 0, 0))
        screen.blit(label, (4, 4))

        pygame.display.flip()
        clock.tick(fps)

    pygame.time.wait(2000)
    pygame.quit()
