#!/usr/bin/env python3
"""Generate a 5-second real estate infographic video."""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 24
NAVY_BLUE_RGB = (0, 51, 102)
GOLD_RGB = (212, 175, 55)
WHITE_RGB = (255, 255, 255)
# BGR format for OpenCV (reversed)
NAVY_BLUE = (102, 51, 0)
GOLD = (55, 175, 212)
WHITE = (255, 255, 255)

def create_blank_frame_cv2(color=NAVY_BLUE):
    """Create a blank frame with specified color using OpenCV."""
    return np.full((HEIGHT, WIDTH, 3), color, dtype=np.uint8)

def add_text_cv2(frame, text, position, font_size=2, color=WHITE, center=False):
    """Add text to frame using OpenCV."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 3

    if center:
        text_size = cv2.getTextSize(text, font, font_size, thickness)[0]
        x = (WIDTH - text_size[0]) // 2
        y = position[1]
        position = (x, y)

    cv2.putText(frame, text, position, font, font_size, color, thickness, cv2.LINE_AA)
    return frame

def add_multiline_text_cv2(frame, lines, y_start=400, color=WHITE, font_size=3):
    """Add multiple lines of text using OpenCV."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 3

    y = y_start
    for i, line in enumerate(lines):
        size = font_size if i == 0 else font_size * 0.6
        text_size = cv2.getTextSize(line, font, size, thickness)[0]
        x = (WIDTH - text_size[0]) // 2
        cv2.putText(frame, line, (x, y), font, size, color, thickness, cv2.LINE_AA)
        y += 150

    return frame

def create_opening_frame():
    """OPENING (0-1 second) - Title frame."""
    frame = create_blank_frame_cv2()
    frame = add_text_cv2(frame, "BDS & HA TANG", (100, 400), font_size=4, color=WHITE, center=True)
    return frame

def create_stock_frame(ticker, subtitle="Quy Dat Chien Luoc"):
    """Create a stock frame."""
    frame = create_blank_frame_cv2()
    frame = add_multiline_text_cv2(frame, [ticker, subtitle], y_start=400)
    return frame

def create_highlight_frame():
    """CENTER HIGHLIGHT (3.5-4 seconds) - Investment opportunity highlight."""
    frame = create_blank_frame_cv2()
    frame = add_multiline_text_cv2(frame, ["Co Hoi Dau Tu"], y_start=380, color=GOLD)

    # Add arrow using circle and line
    cv2.circle(frame, (WIDTH // 2, 700), 60, GOLD, -1)
    cv2.putText(frame, "^", (WIDTH // 2 - 30, 730), cv2.FONT_HERSHEY_SIMPLEX, 5, WHITE, 4)

    return frame

def create_closing_frame():
    """CLOSING (4-5 seconds) - Closing message."""
    frame = create_blank_frame_cv2()
    frame = add_text_cv2(frame, "Vi Tri Dac Dia", (100, 450), font_size=3, color=WHITE, center=True)
    return frame

def apply_fade_in(frame, alpha):
    """Apply fade in effect to frame."""
    return cv2.convertScaleAbs(frame * alpha)

def apply_fade_out(frame, alpha):
    """Apply fade out effect to frame."""
    return cv2.convertScaleAbs(frame * alpha)

def main():
    """Generate the complete video."""
    print("Creating real estate infographic video...")

    output_path = "/home/user/hyperframes-videos/real_estate_infographic.mp4"

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))

    total_frames = 5 * FPS  # 5 seconds at 24 fps = 120 frames
    current_frame = 0

    # Timeline:
    # 0-24 frames (0-1s): Opening
    # 24-36 frames (1-1.5s): Stock 1
    # 36-48 frames (1.5-2s): Stock 2
    # 48-60 frames (2-2.5s): Stock 3
    # 60-84 frames (2.5-3.5s): Stock 4
    # 84-96 frames (3.5-4s): Highlight
    # 96-120 frames (4-5s): Closing

    print("  Generating frames...")

    # Opening frame (0-1s, 24 frames)
    print("  Creating opening frames...")
    opening_frame = create_opening_frame()
    for i in range(24):
        alpha = min(1.0, i / 7)  # Fade in over ~0.3s
        faded = apply_fade_in(opening_frame, alpha)
        out.write(faded.astype(np.uint8))
        current_frame += 1

    # Stock frames
    stocks = [
        ("CII - Coteccons", 12),  # 0.5s = 12 frames
        ("TCH - Tan Cang", 12),
        ("VPI - Van Phu", 12),
        ("HUT - Hutuco", 24),  # 1s = 24 frames
    ]

    for ticker, num_frames in stocks:
        print(f"  Creating stock frames: {ticker}...")
        stock_frame = create_stock_frame(ticker)
        for i in range(num_frames):
            alpha = min(1.0, i / 4)  # Fade in quickly
            faded = apply_fade_in(stock_frame, alpha)
            out.write(faded.astype(np.uint8))

    # Highlight frame (3.5-4s, 12 frames)
    print("  Creating highlight frames...")
    highlight_frame = create_highlight_frame()
    for i in range(12):
        alpha = min(1.0, i / 5)  # Fade in
        faded = apply_fade_in(highlight_frame, alpha)
        out.write(faded.astype(np.uint8))

    # Closing frame (4-5s, 24 frames)
    print("  Creating closing frames...")
    closing_frame = create_closing_frame()
    for i in range(24):
        alpha = 1.0 - (i / 24)  # Fade out
        faded = apply_fade_out(closing_frame, alpha)
        out.write(faded.astype(np.uint8))

    out.release()

    print(f"✓ Video created successfully!")
    print(f"  Duration: 5 seconds")
    print(f"  Resolution: {WIDTH}x{HEIGHT}")
    print(f"  Frame rate: {FPS} fps")
    print(f"  File: {output_path}")

if __name__ == "__main__":
    main()
