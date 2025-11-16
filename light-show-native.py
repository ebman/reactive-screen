#!/usr/bin/env python3
"""
Native Python Light Show - Spans all monitors using SDL/pygame
Works at a lower level than browser to properly handle multi-monitor setups
"""

import pygame
import pyaudio
import numpy as np
import math
import sys
import os
from pygame.locals import *

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class LightShow:
    def __init__(self):
        # Set SDL to position window at top-left spanning all monitors
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        os.environ['SDL_VIDEO_CENTERED'] = "0"

        pygame.init()

        # Manually set dimensions to span all 3 monitors
        # Don't rely on display_info as it might only report primary monitor
        self.width = 5760  # 3 monitors at 1920 each
        self.height = 1080

        print(f"Creating borderless window spanning all monitors: {self.width}x{self.height}")

        # Use NOFRAME for borderless window (not FULLSCREEN which picks one monitor)
        # HWSURFACE and DOUBLEBUF for hardware acceleration
        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            NOFRAME | HWSURFACE | DOUBLEBUF
        )

        pygame.display.set_caption("Reactive Light Show")
        pygame.mouse.set_visible(False)

        # Audio setup
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.setup_audio()

        # Animation state
        self.rotation = 0
        self.rotation2 = 0
        self.rotation3 = 0
        self.time = 0
        self.clock = pygame.time.Clock()

        # Colors
        self.colors = [
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (255, 255, 0),    # Yellow
            (255, 0, 0),      # Red
            (0, 255, 0),      # Green
            (0, 0, 255),      # Blue
            (255, 128, 0),    # Orange
            (128, 0, 255),    # Purple
        ]

    def setup_audio(self):
        """Setup microphone input"""
        try:
            self.stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            print("Microphone access granted")
        except Exception as e:
            print(f"Microphone access denied: {e}")
            self.stream = None

    def get_audio_data(self):
        """Get frequency spectrum from microphone"""
        if not self.stream:
            # Return random data if no mic
            return np.random.randint(0, 50, 128)

        try:
            # Read audio data
            data = self.stream.read(CHUNK, exception_on_overflow=False)

            # Convert to numpy array
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Perform FFT
            fft = np.fft.fft(audio_data)
            fft = np.abs(fft[:len(fft)//2])

            # Normalize to 0-255 range
            fft = fft / np.max(fft) * 255 if np.max(fft) > 0 else fft

            # Downsample to 128 frequency bins
            bins = 128
            freq_data = np.array([
                np.mean(fft[i:i+len(fft)//bins])
                for i in range(0, len(fft), len(fft)//bins)
            ][:bins])

            return freq_data.astype(int)
        except Exception as e:
            return np.zeros(128)

    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

    def draw_kaleidoscope(self, freq_data, bass, mid, treble, average):
        """Draw kaleidoscope visualization"""
        center_x = self.width // 2
        center_y = self.height // 2

        # Global pulse
        pulse = 1 + (bass / 255) * 0.3

        # Draw multiple rotating layers
        for layer in range(4):
            # Determine rotation speed for this layer
            if layer % 3 == 0:
                rotation = self.rotation
            elif layer % 3 == 1:
                rotation = self.rotation2
            else:
                rotation = self.rotation3

            # Symmetry count
            symmetry = 8

            for sym in range(symmetry):
                angle_offset = (2 * math.pi / symmetry) * sym + rotation

                # Draw spiral pattern
                points = []
                for i in range(0, len(freq_data), 2):
                    angle = (i / len(freq_data)) * math.pi * 4 + rotation * 2
                    intensity = freq_data[i] / 255
                    radius = (50 + layer * 50 + intensity * 200) * pulse

                    x = center_x + math.cos(angle + angle_offset) * radius
                    y = center_y + math.sin(angle + angle_offset) * radius
                    points.append((x, y))

                if len(points) > 2:
                    hue = (layer * 60 + self.time * 50 + sym * 30) % 360
                    color = self.hsv_to_rgb(hue, 1.0, 0.6 + average / 255 * 0.4)
                    pygame.draw.lines(self.screen, color, False, points,
                                    max(1, int(3 + bass / 255 * 8)))

    def draw_frequency_circles(self, freq_data, bass):
        """Draw circular frequency visualization"""
        center_x = self.width // 2
        center_y = self.height // 2

        num_circles = 2
        for circle in range(num_circles):
            base_radius = 100 + circle * 60

            for i in range(0, len(freq_data), 3):
                angle = (i / len(freq_data)) * 2 * math.pi + self.rotation2
                intensity = freq_data[i] / 255
                radius = base_radius + intensity * 150

                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
                size = max(1, int(3 + intensity * 20))

                hue = (i / len(freq_data) * 360 + self.time * 100 + circle * 120) % 360
                color = self.hsv_to_rgb(hue, 1.0, 0.6 + intensity * 0.4)

                pygame.draw.circle(self.screen, color, (int(x), int(y)), size)

    def draw_geometric_shapes(self, bass, mid, treble):
        """Draw pulsing geometric shapes"""
        center_x = self.width // 2
        center_y = self.height // 2

        num_shapes = 8
        for s in range(num_shapes):
            angle = (s / num_shapes) * 2 * math.pi - self.rotation3 * 0.5
            dist = 250 + math.sin(self.time * 2 + s) * 60
            x = center_x + math.cos(angle) * dist
            y = center_y + math.sin(angle) * dist

            # Choose frequency based on position
            freq = bass if s % 3 == 0 else (mid if s % 3 == 1 else treble)
            size = int(30 + (freq / 255) * 150)

            hue = (s * 45 + self.time * 100) % 360
            color = self.hsv_to_rgb(hue, 1.0, 0.6 + freq / 255 * 0.4)

            # Draw star shape
            points = []
            for i in range(10):
                r = size if i % 2 == 0 else size // 2
                a = (i / 10) * 2 * math.pi + self.rotation2 * 2
                px = x + math.cos(a) * r
                py = y + math.sin(a) * r
                points.append((px, py))

            if len(points) > 2:
                pygame.draw.polygon(self.screen, color, points)

    def run(self):
        """Main loop"""
        running = True

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key in (K_ESCAPE, K_q):
                        running = False

            # Get audio data
            freq_data = self.get_audio_data()

            # Calculate frequency bands
            third = len(freq_data) // 3
            bass = np.mean(freq_data[:third])
            mid = np.mean(freq_data[third:2*third])
            treble = np.mean(freq_data[2*third:])
            average = np.mean(freq_data)

            # Fade effect (trail)
            fade_surface = pygame.Surface((self.width, self.height))
            fade_surface.fill((0, 0, 0))
            fade_amount = max(0, min(255, int(255 * (0.15 - bass / 255 * 0.1))))
            fade_surface.set_alpha(fade_amount)
            self.screen.blit(fade_surface, (0, 0))

            # Flash white on massive beats
            if bass > 230:
                flash_surface = pygame.Surface((self.width, self.height))
                flash_surface.fill((255, 255, 255))
                flash_surface.set_alpha(int((bass - 230) / 255 * 76))
                self.screen.blit(flash_surface, (0, 0))

            # Update rotation speeds
            target_rotation_speed = 0.02 + (bass / 255) * 0.3
            self.rotation += target_rotation_speed
            self.rotation2 += target_rotation_speed * 0.7 + math.sin(self.time * 0.5) * 0.01
            self.rotation3 += target_rotation_speed * 1.3 + math.cos(self.time * 0.3) * 0.01
            self.time += 0.03

            # Draw visualizations
            self.draw_kaleidoscope(freq_data, bass, mid, treble, average)
            self.draw_frequency_circles(freq_data, bass)
            self.draw_geometric_shapes(bass, mid, treble)

            # Update display
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        pygame.quit()

if __name__ == "__main__":
    try:
        print("Starting native light show...")
        print("Press ESC or Q to exit")
        show = LightShow()
        show.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()
