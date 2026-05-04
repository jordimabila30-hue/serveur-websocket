"""
Jeu de la vie de Conway (animation console).

Exemples :
  python ex1.py
  python ex1.py --w 80 --h 24 --steps 500 --fps 30 --seed 123
  python ex1.py --density 0.15 --wrap
"""

from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass


ALIVE = "█"
DEAD = " "


@dataclass(frozen=True)
class Config:
    w: int
    h: int
    steps: int
    fps: float
    density: float
    seed: int | None
    wrap: bool


def parse_args(argv: list[str]) -> Config:
    p = argparse.ArgumentParser(description="Jeu de la vie de Conway (console).")
    p.add_argument("--w", type=int, default=60, help="largeur de la grille")
    p.add_argument("--h", type=int, default=20, help="hauteur de la grille")
    p.add_argument("--steps", type=int, default=300, help="nombre d'itérations")
    p.add_argument("--fps", type=float, default=20.0, help="vitesse d'affichage")
    p.add_argument("--density", type=float, default=0.22, help="densité initiale (0..1)")
    p.add_argument("--seed", type=int, default=None, help="seed aléatoire (reproductible)")
    p.add_argument(
        "--wrap",
        action="store_true",
        help="grille torique (les bords se rejoignent)",
    )
    ns = p.parse_args(argv)

    w = max(5, min(ns.w, 240))
    h = max(5, min(ns.h, 80))
    steps = max(1, ns.steps)
    fps = max(1.0, ns.fps)
    density = max(0.0, min(1.0, ns.density))

    return Config(w=w, h=h, steps=steps, fps=fps, density=density, seed=ns.seed, wrap=ns.wrap)


def make_grid(cfg: Config) -> list[list[bool]]:
    if cfg.seed is not None:
        random.seed(cfg.seed)
    return [[random.random() < cfg.density for _ in range(cfg.w)] for _ in range(cfg.h)]


def neighbors_alive(grid: list[list[bool]], x: int, y: int, wrap: bool) -> int:
    h = len(grid)
    w = len(grid[0]) if h else 0
    alive = 0

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy
            if wrap:
                nx %= w
                ny %= h
                if grid[ny][nx]:
                    alive += 1
            else:
                if 0 <= nx < w and 0 <= ny < h and grid[ny][nx]:
                    alive += 1
    return alive


def step(grid: list[list[bool]], wrap: bool) -> list[list[bool]]:
    h = len(grid)
    w = len(grid[0]) if h else 0
    nxt = [[False] * w for _ in range(h)]

    for y in range(h):
        row = grid[y]
        out = nxt[y]
        for x in range(w):
            n = neighbors_alive(grid, x, y, wrap)
            if row[x]:
                out[x] = n in (2, 3)
            else:
                out[x] = n == 3
    return nxt


def render(grid: list[list[bool]], generation: int) -> str:
    h = len(grid)
    w = len(grid[0]) if h else 0
    alive_count = sum(1 for y in range(h) for x in range(w) if grid[y][x])

    lines: list[str] = []
    lines.append(f"Generation: {generation} | Alive: {alive_count} | Ctrl+C pour arrêter")
    lines.append("+" + "-" * w + "+")
    for y in range(h):
        lines.append("|" + "".join(ALIVE if grid[y][x] else DEAD for x in range(w)) + "|")
    lines.append("+" + "-" * w + "+")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    cfg = parse_args(argv)
    grid = make_grid(cfg)
    frame_time = 1.0 / cfg.fps

    try:
        for gen in range(cfg.steps):
            sys.stdout.write("\x1b[2J\x1b[H")  # clear + home (ANSI)
            sys.stdout.write(render(grid, gen) + "\n")
            sys.stdout.flush()
            grid = step(grid, cfg.wrap)
            time.sleep(frame_time)
    except KeyboardInterrupt:
        sys.stdout.write("\nArrêté.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
