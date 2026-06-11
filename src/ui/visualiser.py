"""
ui/visualiser.py
Renders the warehouse map in the terminal (always) and optionally in pygame.

Terminal rendering works with zero dependencies.
pygame rendering is optional — install with: pip install pygame
"""
from __future__ import annotations
import time
import sys
from typing import List, Optional, Tuple
from src.i18n import translate

Pos = Tuple[int, int]

# ANSI colour codes for terminal output
_RESET  = "\033[0m"
_RED    = "\033[31m"
_GREEN  = "\033[32m"
_YELLOW = "\033[33m"
_CYAN   = "\033[36m"
_BOLD   = "\033[1m"

# Map cell colours (pygame)
_PG_COLORS = {
    0: (230, 230, 230),   # OPEN   — light grey
    1: (100, 149, 237),   # SHELF  — cornflower blue
    2: (50, 205, 50),     # DEPOT  — lime green
    3: (50, 50, 50),      # OBSTACLE — dark
    4: (255, 255, 255),   # AISLE  — white
}
_PG_ROBOT  = (220, 20, 60)   # crimson
_PG_PATH   = (255, 215, 0)   # gold


# ── Terminal Visualiser ───────────────────────────────────────────────────────

def print_map(
    warehouse_map,
    robot_pos: Optional[Pos] = None,
    path: Optional[List[Pos]] = None,
    title: str = "",
    lang: str = "en",
) -> None:
    """Print a colourised ASCII map to stdout."""
    title = title or translate("app_title", lang)
    if title:
        print(f"\n{_BOLD}{title}{_RESET}")

    path_set = set(path) if path else set()

    # Column indices header
    header = "    " + "".join(f"{c%10}" for c in range(warehouse_map.cols))
    print(header)

    for r in range(warehouse_map.rows):
        row_str = f"{r:3} "
        for c in range(warehouse_map.cols):
            cell = warehouse_map.grid[r][c]
            pos  = (r, c)
            if robot_pos and pos == robot_pos:
                row_str += f"{_BOLD}{_RED}R{_RESET}"
            elif pos in path_set:
                row_str += f"{_YELLOW}·{_RESET}"
            elif cell == 2:   # DEPOT
                row_str += f"{_GREEN}D{_RESET}"
            elif cell == 1:   # SHELF
                row_str += f"{_CYAN}S{_RESET}"
            elif cell == 3:   # OBSTACLE
                row_str += "#"
            elif cell == 4:   # AISLE
                row_str += " "
            else:
                row_str += "."
        print(row_str)
    print()


def animate_path(
    warehouse_map,
    path: List[Pos],
    delay: float = 0.1,
    title: str = "",
    lang: str = "en",
) -> None:
    """
    Animate the robot moving step-by-step through a path in the terminal.
    Clears and redraws the map at each step.
    """
    for step, pos in enumerate(path):
        # Clear terminal (works on most Unix/Windows terminals)
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        step_info = translate("step_info", lang)
        try:
            print(step_info.format(step=step + 1, total=len(path), pos=pos))
        except Exception:
            print(f"Step {step + 1}/{len(path)}  Robot at {pos}")
        print_map(warehouse_map, robot_pos=pos, path=path[:step + 1], title=title, lang=lang)
        time.sleep(delay)


# ── pygame Visualiser ─────────────────────────────────────────────────────────

def animate_pygame(
    warehouse_map,
    path: List[Pos],
    cell_size: int = 30,
    fps: int = 10,
    title: str = "",
    lang: str = "en",
) -> None:
    """
    Animated pygame visualisation.
    Falls back to terminal warning if pygame is not installed.
    """
    try:
        import pygame
    except ImportError:
        msg = translate("pygame_missing", lang)
        print(msg)
        print(translate("terminal_fallback", lang))
        animate_path(warehouse_map, path, title=title or translate("app_title", lang), lang=lang)
        return

    pygame.init()
    rows, cols = warehouse_map.rows, warehouse_map.cols
    width  = cols * cell_size
    height = rows * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title or translate("app_title", lang))
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("monospace", 12)

    path_set: set = set()

    for step, robot_pos in enumerate(path):
        path_set.add(robot_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((200, 200, 200))

        # Draw cells
        for r in range(rows):
            for c in range(cols):
                cell_type = warehouse_map.grid[r][c]
                color = _PG_COLORS.get(cell_type, (200, 200, 200))
                rect  = (c * cell_size, r * cell_size, cell_size - 1, cell_size - 1)

                if (r, c) == robot_pos:
                    color = _PG_ROBOT
                elif (r, c) in path_set and (r, c) != robot_pos:
                    color = _PG_PATH

                pygame.draw.rect(screen, color, rect)

        # Step info
        step_info = translate("step_info", lang)
        try:
            label_text = step_info.format(step=step + 1, total=len(path), pos=robot_pos)
        except Exception:
            label_text = f"Step {step + 1}/{len(path)}  pos={robot_pos}"
        label = font.render(label_text, True, (0, 0, 0))
        screen.blit(label, (4, 4))

        pygame.display.flip()
        clock.tick(fps)

    # Pause at end
    pygame.time.wait(2000)
    pygame.quit()
