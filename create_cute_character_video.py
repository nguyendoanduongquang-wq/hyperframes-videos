#!/usr/bin/env python3
"""Generate a 5-second animated video with a cute 3D character."""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 24
TOTAL_FRAMES = 5 * FPS  # 120 frames for 5 seconds

# Colors
BG_COLOR_1 = np.array([232, 220, 200])  # #E8DCC8 - warm tan
BG_COLOR_2 = np.array([245, 240, 232])  # #F5F0E8 - soft cream
WHITE = np.array([255, 255, 255])
BEIGE = np.array([230, 210, 190])
BLACK = np.array([0, 0, 0])
SHADOW = np.array([100, 100, 100])

def create_gradient_background():
    """Create a soft beige/cream gradient background."""
    bg = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = BG_COLOR_1 * (1 - ratio) + BG_COLOR_2 * ratio
        bg[y, :] = color.astype(np.uint8)
    return bg

def draw_circle_gradient(image, center, radius, color, shadow_offset=10):
    """Draw a circle with subtle 3D effect using gradient shading."""
    x, y = center

    # Draw shadow
    for i in range(shadow_offset, 0, -1):
        alpha = (shadow_offset - i) / shadow_offset * 0.3
        shadow_center = (int(x + i * 0.3), int(y + i * 0.5))
        cv2.circle(image, shadow_center, int(radius * 0.8), SHADOW, -1)

    # Draw main circle with lighting
    for i in range(radius, 0, -1):
        # Lighter on top, darker on bottom for 3D effect
        ratio = i / radius
        if ratio > 0.7:  # Top part - lighter
            shade = color * 1.1
        elif ratio > 0.4:  # Middle - normal
            shade = color
        else:  # Bottom - darker for shadow
            shade = color * 0.85

        shade = np.clip(shade, 0, 255)
        cv2.circle(image, center, i, shade.astype(np.uint8), 1)

    # Fill with gradient
    cv2.circle(image, center, radius, color.astype(np.uint8), -1)
    return image

def draw_cute_character(frame, position, scale=1.0, opacity=1.0):
    """Draw a cute 3D character on the frame."""
    x, y = position

    # Convert to PIL for better drawing capabilities
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image, 'RGBA')

    # Calculate opacity as alpha
    alpha = int(255 * opacity)

    # Sizes
    head_radius = int(100 * scale)
    eye_width = int(35 * scale)
    eye_height = int(45 * scale)
    body_height = int(150 * scale)
    body_width = int(110 * scale)
    arm_length = int(60 * scale)
    arm_width = int(25 * scale)

    # Draw body (rounded rectangle/dress shape)
    body_top = y + head_radius + int(20 * scale)
    body_bottom = body_top + body_height

    # Body outline for shading
    for i in range(int(body_width * 0.8), 0, -1):
        shade_alpha = int(20 * (body_width - i) / body_width)
        draw.ellipse(
            [x - i, body_top, x + i, body_bottom],
            fill=(220, 220, 220, max(0, alpha - shade_alpha))
        )

    # Main body
    draw.ellipse(
        [x - body_width // 2, body_top, x + body_width // 2, body_bottom],
        fill=(255, 255, 255, alpha)
    )

    # Arms
    arm_y = body_top + int(30 * scale)
    # Left arm
    draw.ellipse(
        [x - body_width // 2 - arm_length, arm_y - arm_width // 2,
         x - body_width // 2, arm_y + arm_width // 2],
        fill=(255, 255, 255, alpha)
    )
    # Right arm
    draw.ellipse(
        [x + body_width // 2, arm_y - arm_width // 2,
         x + body_width // 2 + arm_length, arm_y + arm_width // 2],
        fill=(255, 255, 255, alpha)
    )

    # Head with shading
    head_top = y - head_radius
    head_bottom = y + head_radius

    # Head shading/3D effect
    for i in range(head_radius, 0, -2):
        shade_alpha = int(15 * (head_radius - i) / head_radius)
        draw.ellipse(
            [x - i, head_top + (head_radius - i), x + i, head_bottom + (head_radius - i)],
            fill=(200, 200, 200, max(0, shade_alpha))
        )

    # Main head
    draw.ellipse(
        [x - head_radius, head_top, x + head_radius, head_bottom],
        fill=(255, 255, 255, alpha)
    )

    # Eyes
    eye_top = y - int(30 * scale)
    eye_bottom = eye_top + eye_height

    # Left eye
    draw.ellipse(
        [x - int(60 * scale) - eye_width // 2, eye_top,
         x - int(60 * scale) + eye_width // 2, eye_bottom],
        fill=(0, 0, 0, alpha)
    )
    # Right eye
    draw.ellipse(
        [x + int(60 * scale) - eye_width // 2, eye_top,
         x + int(60 * scale) + eye_width // 2, eye_bottom],
        fill=(0, 0, 0, alpha)
    )

    # Eye highlights (shine)
    highlight_radius = int(8 * scale)
    draw.ellipse(
        [x - int(60 * scale) - highlight_radius, eye_top + int(10 * scale),
         x - int(60 * scale) + highlight_radius, eye_top + highlight_radius + int(10 * scale)],
        fill=(255, 255, 255, alpha)
    )
    draw.ellipse(
        [x + int(60 * scale) - highlight_radius, eye_top + int(10 * scale),
         x + int(60 * scale) + highlight_radius, eye_top + highlight_radius + int(10 * scale)],
        fill=(255, 255, 255, alpha)
    )

    # Smile (curved line)
    mouth_y = y + int(20 * scale)
    mouth_width = int(40 * scale)

    # Create smile using arc-like points
    for px in range(-mouth_width, mouth_width + 1, 2):
        curve = (px * px) / (mouth_width * mouth_width) - 0.5
        draw.ellipse(
            [x + px - 2, mouth_y + int(curve * 20 * scale) - 2,
             x + px + 2, mouth_y + int(curve * 20 * scale) + 2],
            fill=(200, 180, 160, alpha)
        )

    # Convert back to OpenCV format
    rgb_image = np.array(pil_image)
    return cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

def calculate_animation_params(frame_num):
    """Calculate animation parameters for the current frame."""
    # Timeline
    fade_in_frames = 24  # 1 second
    main_frames = 72     # 3 seconds
    fade_out_frames = 24 # 1 second

    # Fade in/out
    if frame_num < fade_in_frames:
        opacity = frame_num / fade_in_frames
    elif frame_num < fade_in_frames + main_frames:
        opacity = 1.0
    else:
        opacity = 1.0 - (frame_num - fade_in_frames - main_frames) / fade_out_frames

    opacity = max(0, min(1, opacity))

    # Animation only during main sequence
    anim_frame = max(0, frame_num - fade_in_frames)

    # Bobbing motion (gentle up and down, 20px max)
    bob_amplitude = 20
    bob_speed = 0.05
    bob_offset = bob_amplitude * math.sin(anim_frame * bob_speed)

    # Swaying motion (±3 degrees)
    sway_angle = 3 * math.sin(anim_frame * 0.03)

    # Breathing effect (98% to 102%)
    breathing_scale = 1.0 + 0.02 * math.sin(anim_frame * 0.04)

    # Combine all motions
    scale = breathing_scale

    return {
        'opacity': opacity,
        'y_offset': bob_offset,
        'sway_angle': sway_angle,
        'scale': scale
    }

def main():
    """Generate the complete video."""
    print("Creating cute 3D character animation video...")

    output_path = "/home/user/hyperframes-videos/cute_character_animation.mp4"

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))

    print("  Generating frames...")
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    for frame_num in range(TOTAL_FRAMES):
        # Create background with gradient
        frame = create_gradient_background()

        # Calculate animation parameters
        params = calculate_animation_params(frame_num)

        # Apply sway rotation (simple approximation)
        # Note: actual rotation would require more complex transforms

        # Calculate character position with bob motion
        char_x = center_x
        char_y = int(center_y + params['y_offset'])

        # Draw character
        frame = draw_cute_character(
            frame,
            (char_x, char_y),
            scale=params['scale'],
            opacity=params['opacity']
        )

        # Write frame to video
        out.write(frame)

        # Progress indicator
        if (frame_num + 1) % 24 == 0:
            seconds = (frame_num + 1) / FPS
            print(f"    Frame {frame_num + 1}/{TOTAL_FRAMES} ({seconds:.1f}s)")

    out.release()

    print(f"✓ Video created successfully!")
    print(f"  Duration: 5 seconds")
    print(f"  Resolution: {WIDTH}x{HEIGHT}")
    print(f"  Frame rate: {FPS} fps")
    print(f"  File: {output_path}")

if __name__ == "__main__":
    main()
