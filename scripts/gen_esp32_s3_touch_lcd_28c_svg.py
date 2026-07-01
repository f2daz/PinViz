#!/usr/bin/env python3
"""Regenerate the Waveshare ESP32-S3-Touch-LCD-2.8C (round) board SVG for PinViz.

Personal board (not part of the upstream PR). Round 2.8" 480x480 display board;
the externally usable pins are two 4-pin edge headers at the bottom:
    UART: GND, RXD(GPIO44), TXD(GPIO43), 3V3      -> left column
    I2C : GND, 3V3, SCL(GPIO7), SDA(GPIO15)       -> right column

Output: ``src/pinviz/assets/esp32_s3_touch_lcd_28c_mod.svg``

Layout constants MUST stay in sync with the board config
``src/pinviz/board_configs/esp32_s3_touch_lcd_28c.json``:
    left_col_x=95, right_col_x=135, start_y=235, row_spacing=15, width=230, height=300
"""

# ruff: noqa: E501  (SVG element strings are intentionally kept on one line)

from pathlib import Path

W, H = 230.0, 300.0
CX, CY, R_PCB, R_SCR = 115.0, 110.0, 105.0, 92.0
LEFT_X, RIGHT_X = 95.0, 135.0
START_Y, ROW = 235.0, 15.0
N = 4  # rows (4 per column, 8 pins total)

UART = ["GND", "RXD", "TXD", "3V3"]   # left column, top -> bottom
I2C = ["GND", "3V3", "SCL", "SDA"]    # right column, top -> bottom


def build() -> str:
    s = ['<?xml version="1.0" encoding="UTF-8"?>']
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    # --- neck connecting the round board to the bottom header tab ---
    s.append(f'<rect x="{CX - 42}" y="{CY + 70}" width="84" height="70" rx="6" fill="#17171c" stroke="#33333a" stroke-width="0.8"/>')
    # --- header tab (bottom) ---
    s.append(f'<rect x="{CX - 60}" y="222" width="120" height="72" rx="7" fill="#1b1b20" stroke="#3a3a42" stroke-width="1.1"/>')
    # --- round PCB ---
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_PCB}" fill="#1b1b20" stroke="#3a3a42" stroke-width="1.4"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_PCB - 3}" fill="none" stroke="#2c2c34" stroke-width="0.6"/>')
    # mounting holes around the ring (4)
    import math
    for ang in (45, 135, 225, 315):
        hx = CX + (R_PCB - 6) * math.cos(math.radians(ang))
        hy = CY - (R_PCB - 6) * math.sin(math.radians(ang))
        s.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="3.2" fill="#0d0d10" stroke="#8a8a90" stroke-width="0.8"/>')
    # --- round display (bezel + screen) ---
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_SCR + 2}" fill="#0a0a0c" stroke="#45454e" stroke-width="1"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_SCR}" fill="#0c0f14"/>')
    # subtle screen glass highlight
    s.append(f'<ellipse cx="{CX - 26}" cy="{CY - 34}" rx="40" ry="26" fill="#12161d" opacity="0.7"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_SCR - 1}" fill="none" stroke="#20242c" stroke-width="0.5"/>')
    # screen label
    s.append(f'<text x="{CX}" y="{CY - 6}" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#3a4048" text-anchor="middle">ESP32-S3</text>')
    s.append(f'<text x="{CX}" y="{CY + 6}" font-family="Arial, sans-serif" font-size="6" fill="#333942" text-anchor="middle">Touch LCD 2.8C</text>')
    s.append(f'<text x="{CX}" y="{CY + 16}" font-family="Arial, sans-serif" font-size="5" fill="#2f353d" text-anchor="middle">480 x 480</text>')
    # --- USB-C at top edge (top-down, overhangs the ring) ---
    s.append(f'<rect x="{CX - 12}" y="{CY - R_PCB - 4}" width="24" height="15" rx="2.4" fill="#d3d6dc" stroke="#7d818a" stroke-width="0.9"/>')
    s.append(f'<rect x="{CX - 10.5}" y="{CY - R_PCB - 2.4}" width="21" height="12" rx="1.6" fill="none" stroke="#b9bdc4" stroke-width="0.5"/>')
    # --- battery MX1.25 connector (right edge) ---
    s.append(f'<rect x="{CX + R_PCB - 12}" y="{CY - 8}" width="12" height="16" rx="1.4" fill="#e6e7ea" stroke="#8a8a90" stroke-width="0.6"/>')
    s.append(f'<text x="{CX + R_PCB - 6}" y="{CY + 20}" font-family="Arial, sans-serif" font-size="4" fill="#7f7f88" text-anchor="middle">BAT</text>')
    # charge LED
    s.append(f'<circle cx="{CX - R_PCB + 12}" cy="{CY}" r="2.4" fill="#8fe0a0" stroke="#5a8a66" stroke-width="0.4"/>')
    # --- header group titles ---
    s.append(f'<text x="{LEFT_X}" y="228" font-family="Arial, sans-serif" font-size="5.5" font-weight="bold" fill="#8f939b" text-anchor="middle">UART</text>')
    s.append(f'<text x="{RIGHT_X}" y="228" font-family="Arial, sans-serif" font-size="5.5" font-weight="bold" fill="#8f939b" text-anchor="middle">I2C</text>')
    # --- pads + silkscreen labels ---
    def label(x, y, txt, anchor, dx):
        s.append(f'<text x="{x + dx}" y="{y + 1.5}" font-family="Consolas, Menlo, monospace" font-size="5" fill="#e9e9ef" text-anchor="{anchor}">{txt}</text>')

    for i in range(N):
        y = START_Y + i * ROW
        s.append(f'<circle cx="{LEFT_X}" cy="{y}" r="4.4" fill="#d8b24a" stroke="#8a6f22" stroke-width="0.5"/>')
        s.append(f'<circle cx="{RIGHT_X}" cy="{y}" r="4.4" fill="#d8b24a" stroke="#8a6f22" stroke-width="0.5"/>')
        label(LEFT_X, y, UART[i], "end", -6.5)    # UART labels flank left
        label(RIGHT_X, y, I2C[i], "start", 6.5)   # I2C labels flank right
    s.append("</svg>")
    return "\n".join(s) + "\n"


def main() -> None:
    out = Path(__file__).resolve().parents[1] / "src" / "pinviz" / "assets" / "esp32_s3_touch_lcd_28c_mod.svg"
    out.write_text(build())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
