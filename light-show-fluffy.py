#!/usr/bin/env python3
"""
Fluffy Triple Monitor Light Show - Ultra-smooth, cloud-like visuals
No harsh edges or points - everything soft, glowing, and dreamy
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

        # 3 monitors at 1920x1080 each
        self.monitor_width = 1920
        self.monitor_height = 1080
        self.num_monitors = 3
        self.width = self.monitor_width * self.num_monitors  # 5760
        self.height = self.monitor_height

        print(f"Creating borderless window: {self.width}x{self.height}")
        print(f"Will render on {self.num_monitors} monitors ({self.monitor_width}x{self.monitor_height} each)")

        # Borderless window
        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            NOFRAME | HWSURFACE | DOUBLEBUF
        )

        pygame.display.set_caption("Triple Monitor Light Show")
        pygame.mouse.set_visible(False)

        # Audio setup
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.setup_audio()

        # Animation state (matching HTML)
        self.rotation = 0
        self.rotation2 = 0
        self.rotation3 = 0
        self.time = 0
        self.target_rotation_speed = 0.02
        self.current_rotation_speed = 0.02
        self.clock = pygame.time.Clock()

        # Trail surface for fade effect
        self.trail_surface = pygame.Surface((self.width, self.height))

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
        """Get frequency spectrum from microphone (matching HTML bufferLength)"""
        if not self.stream:
            return np.random.randint(0, 30, 128)

        try:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            fft = np.fft.fft(audio_data)
            fft = np.abs(fft[:len(fft)//2])
            fft = fft / np.max(fft) * 255 if np.max(fft) > 0 else fft

            bins = 128
            freq_data = np.array([
                np.mean(fft[i:i+len(fft)//bins])
                for i in range(0, len(fft), len(fft)//bins)
            ][:bins])

            return freq_data.astype(int)
        except:
            return np.zeros(128)

    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB (0-255)"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if h < 60: r, g, b = c, x, 0
        elif h < 120: r, g, b = x, c, 0
        elif h < 180: r, g, b = 0, c, x
        elif h < 240: r, g, b = 0, x, c
        elif h < 300: r, g, b = x, 0, c
        else: r, g, b = c, 0, x

        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

    def draw_on_monitor(self, monitor_index, freq_data, bass, mid, treble, average):
        """Draw the full visualization on a single monitor with BIGGER effects that OVERLAP"""
        # Calculate center for this monitor
        center_x = monitor_index * self.monitor_width + self.monitor_width // 2
        center_y = self.monitor_height // 2

        # BIGGER global pulse for more overlap
        global_pulse = 1 + (bass / 255) * 0.5 + (average / 255) * 0.3

        # More dramatic wobble
        wobble_x = math.sin(self.time * 0.8) * 25 + math.cos(self.time * 0.5) * 20
        wobble_y = math.cos(self.time * 0.6) * 25 + math.sin(self.time * 0.7) * 20

        # Draw kaleidoscope layers - MUCH BIGGER for overlap
        layers = 4
        for layer in range(layers):
            if layer % 3 == 0:
                layer_rotation = self.rotation
            elif layer % 3 == 1:
                layer_rotation = self.rotation2
            else:
                layer_rotation = self.rotation3

            direction = 1 if layer % 2 == 0 else -1

            symmetry = 8
            for sym in range(symmetry):
                angle_offset = (math.pi * 2 / symmetry) * sym

                points = []
                step = 2
                for i in range(0, len(freq_data), step):
                    angle = (i / len(freq_data)) * math.pi * 4 + self.rotation * 2
                    intensity = freq_data[i] / 255
                    # MUCH BIGGER radius - increased from 200 to 400 for overlap!
                    radius = (80 + layer * 80 + intensity * 400) * global_pulse

                    total_angle = angle + angle_offset + layer_rotation * direction + math.sin(self.time + layer) * 0.2
                    x = center_x + wobble_x + math.cos(total_angle) * radius
                    y = center_y + wobble_y + math.sin(total_angle) * radius
                    points.append((int(x), int(y)))

                if len(points) > 2:
                    hue = (layer * 60 + self.time * 50 + sym * 30) % 360
                    alpha = 0.5 + (average / 255) * 0.5
                    color = self.hsv_to_rgb(hue, 0.8, 0.6 * alpha)  # Slightly less saturated
                    width = max(3, int(5 + (bass / 255) * 12))  # MUCH THICKER, FLUFFIER

                    try:
                        # Draw with soft glow
                        pygame.draw.lines(self.screen, color, False, points, width)
                    except:
                        pass

        # Organic particle clouds - more transparent
        num_circles = 3
        for circle in range(num_circles):
            base_radius = 150 + circle * 100

            for i in range(0, len(freq_data), 3):
                angle = (i / len(freq_data)) * 2 * math.pi + self.rotation2
                intensity = freq_data[i] / 255
                radius = (base_radius + intensity * 250) * global_pulse

                # Add organic offset
                organic_offset_x = math.sin(self.time + i * 0.1) * 20
                organic_offset_y = math.cos(self.time * 1.3 + i * 0.15) * 20

                x = int(center_x + wobble_x + math.cos(angle) * radius + organic_offset_x)
                y = int(center_y + wobble_y + math.sin(angle) * radius + organic_offset_y)
                size = max(3, int(4 + intensity * 20))  # BIGGER, FLUFFIER particles

                hue = (i / len(freq_data) * 360 + self.time * 100 + circle * 120) % 360
                color = self.hsv_to_rgb(hue, 0.7, 0.4 + intensity * 0.4)  # Softer

                # Create SOFT, FLUFFY glow with multiple layers
                glow_surf = pygame.Surface((size * 8, size * 8), pygame.SRCALPHA)

                # Multi-layer soft glow for fluffy effect
                for layer in range(4, 0, -1):
                    layer_size = int(size * (1 + layer * 0.5))
                    layer_alpha = int((80 + intensity * 100) * (layer / 5))
                    glow_color = (*color, layer_alpha)
                    pygame.draw.circle(glow_surf, glow_color, (size * 4, size * 4), layer_size)

                self.screen.blit(glow_surf, (x - size * 4, y - size * 4))

        # Fractal tendrils - organic branching structures
        num_tendrils = 8
        for t in range(num_tendrils):
            angle = (t / num_tendrils) * 2 * math.pi - self.rotation3 * 0.5
            freq = bass if t % 3 == 0 else (mid if t % 3 == 1 else treble)

            # Draw fractal branch
            self.draw_fractal_tendril(
                center_x + wobble_x,
                center_y + wobble_y,
                angle,
                (350 + math.sin(self.time * 2 + t) * 100) * global_pulse,
                freq / 255,
                depth=3,
                hue_offset=t * 45
            )

        # Tunneling rings - BIGGER
        ring_count = 15
        for r in range(ring_count):
            progress = ((r + self.time * 10) % ring_count) / ring_count
            # Can extend beyond monitor boundaries!
            radius = int(progress * self.monitor_width * 1.2 * global_pulse)

            freq_idx = int(progress * len(freq_data)) % len(freq_data)
            intensity = freq_data[freq_idx] / 255

            hue = (progress * 360 + self.time * 100) % 360
            alpha = 0.3 + intensity * 0.4
            color = self.hsv_to_rgb(hue, 1.0, 0.5 * alpha)
            width = max(1, int(3 + intensity * 10))

            pygame.draw.circle(self.screen, color,
                             (int(center_x + wobble_x), int(center_y + wobble_y)),
                             radius, width)

    def draw_fractal_tendril(self, x, y, angle, length, intensity, depth, hue_offset):
        """Draw organic fractal branching tendril"""
        if depth == 0 or length < 5:
            return

        # Calculate end point
        end_x = x + math.cos(angle) * length
        end_y = y + math.sin(angle) * length

        # Color with organic feel
        hue = (hue_offset + self.time * 50 + depth * 30) % 360
        color = self.hsv_to_rgb(hue, 0.7, 0.3 + intensity * 0.3)

        # Draw transparent line with alpha
        line_surf = pygame.Surface((abs(int(end_x - x)) + 4, abs(int(end_y - y)) + 4), pygame.SRCALPHA)
        start_on_surf = (2, 2) if end_x > x else (abs(int(end_x - x)) + 2, 2)
        end_on_surf = (abs(int(end_x - x)) + 2, abs(int(end_y - y)) + 2) if end_y > y else (abs(int(end_x - x)) + 2, 2)

        # Thinner, more transparent lines
        alpha = int(60 + intensity * 80)
        line_color = (*color, alpha)

        try:
            # Draw the main branch
            points = [(int(x), int(y)), (int(end_x), int(end_y))]

            # Create transparent line surface
            for i in range(len(points) - 1):
                pygame.draw.line(self.screen, (*color, 0), points[i], points[i+1], max(1, depth))

            # FLUFFY, SOFT lines
            if depth > 1:
                width = max(3, depth * 3)  # MUCH THICKER
            else:
                width = 3

            # Draw organically curved line with MORE segments for ultra-smoothness
            num_segments = 10  # Increased for fluffy smoothness
            for i in range(num_segments):
                t = i / num_segments
                # Organic curve using sine
                curve_offset_x = math.sin(self.time + t * 3) * 10 * intensity
                curve_offset_y = math.cos(self.time * 1.2 + t * 3) * 10 * intensity

                seg_x = x + (end_x - x) * t + curve_offset_x
                seg_y = y + (end_y - y) * t + curve_offset_y

                if i > 0:
                    pygame.draw.line(self.screen, color,
                                   (int(prev_x), int(prev_y)),
                                   (int(seg_x), int(seg_y)), width)
                prev_x, prev_y = seg_x, seg_y

            # Branch recursively - creates fractal pattern
            if depth > 1:
                # Left branch
                branch_angle_left = angle + 0.4 + math.sin(self.time) * 0.2
                self.draw_fractal_tendril(end_x, end_y, branch_angle_left,
                                        length * 0.65, intensity, depth - 1, hue_offset + 20)

                # Right branch
                branch_angle_right = angle - 0.4 - math.sin(self.time) * 0.2
                self.draw_fractal_tendril(end_x, end_y, branch_angle_right,
                                        length * 0.65, intensity, depth - 1, hue_offset - 20)
        except:
            pass

    def draw_funky_waveforms(self, freq_data, bass, mid, treble, average):
        """Draw subtle, transparent waveforms that span across all monitors"""

        # 1. SUBTLE HORIZONTAL WAVEFORM - transparent and gentle
        points_top = []
        points_bottom = []
        step = max(1, self.width // 200)
        for x in range(0, self.width, step):
            idx = int((x / self.width) * len(freq_data)) % len(freq_data)
            intensity = freq_data[idx] / 255

            # Gentler waveform
            wave_height = intensity * 150 + bass / 255 * 50  # Reduced from 300/100
            y_top = self.height // 4 + math.sin(x * 0.01 + self.time * 3) * wave_height
            y_bottom = 3 * self.height // 4 - math.sin(x * 0.01 + self.time * 3) * wave_height

            points_top.append((x, int(y_top)))
            points_bottom.append((x, int(y_bottom)))

        if len(points_top) > 2:
            hue = (self.time * 80) % 360
            color = self.hsv_to_rgb(hue, 0.6, 0.4)  # Slightly brighter
            # FLUFFY, THICK lines
            pygame.draw.lines(self.screen, color, False, points_top, 3)
            pygame.draw.lines(self.screen, color, False, points_bottom, 3)

        # 2. ORGANIC FLOWING WAVEFORM - gentle sine curves across width
        points = []
        num_points = 300
        for i in range(num_points):
            progress = i / num_points
            x = progress * self.width

            freq_idx = int(progress * len(freq_data)) % len(freq_data)
            intensity = freq_data[freq_idx] / 255

            # Organic flowing curves - more subtle
            y = self.height / 2
            y += math.sin(progress * math.pi * 8 + self.time * 2) * (30 + intensity * 80)  # Reduced
            y += math.cos(progress * math.pi * 12 + self.time * 3) * (20 + intensity * 50)  # Reduced
            y += math.sin(progress * math.pi * 20 - self.time * 5) * (10 + bass / 255 * 40)  # Reduced

            points.append((int(x), int(y)))

        if len(points) > 2:
            # Fluffy gradient
            for i in range(len(points) - 1):
                hue = (i / len(points) * 360 + self.time * 120) % 360
                color = self.hsv_to_rgb(hue, 0.5, 0.3)  # Slightly brighter
                pygame.draw.line(self.screen, color, points[i], points[i + 1], 3)  # FLUFFY

        # 3. FLUFFY EDGE TENDRILS - soft organic wisps from edges
        num_tendrils = 16
        for i in range(num_tendrils):
            angle = (i / num_tendrils) * 2 * math.pi

            freq_idx = int(i / num_tendrils * len(freq_data)) % len(freq_data)
            intensity = freq_data[freq_idx] / 255

            # Soft wisps
            length = intensity * 200 + bass / 255 * 100
            x1, y1 = 0, self.height / 2
            x2 = length * math.cos(angle)
            y2 = self.height / 2 + length * math.sin(angle)

            hue = (i / num_tendrils * 360 + self.time * 90) % 360
            color = self.hsv_to_rgb(hue, 0.4, 0.3 + intensity * 0.2)  # Softer
            pygame.draw.line(self.screen, color, (int(x1), int(y1)), (int(x2), int(y2)), 3)  # FLUFFY

            # Right edge tendrils
            x1 = self.width
            x2 = self.width - length * math.cos(angle)
            pygame.draw.line(self.screen, color, (int(x1), int(y1)), (int(x2), int(y2)), 3)

    def draw_high_note_effects(self, freq_data, bass, mid, treble, average):
        """Glowing orbs for high notes and beat pulsing effects"""

        # Beat pulse intensity
        beat_pulse = 1 + (bass / 255) * 0.4

        # 1. FLOATING GLOWING ORBS for high notes
        if treble > 100:
            intensity = (treble - 100) / 155
            num_orbs = int(intensity * 40) + 15  # 15-55 orbs

            for i in range(num_orbs):
                # Position with organic movement
                base_x = (i * 137.5) % self.width  # Golden ratio distribution
                base_y = (i * 79.3) % self.height

                # Floating motion
                float_x = base_x + math.sin(self.time * 2 + i * 0.5) * 100
                float_y = base_y + math.cos(self.time * 1.5 + i * 0.3) * 80

                x = int(float_x) % self.width
                y = int(float_y) % self.height

                # Orb size pulses with beat
                base_size = 8 + intensity * 25
                orb_size = int(base_size * beat_pulse)

                # Bright, ethereal colors
                hue = (self.time * 150 + i * 20 + treble) % 360
                color = self.hsv_to_rgb(hue, 0.7, 0.6 + intensity * 0.3)

                # Draw layered glowing orb
                glow_surf = pygame.Surface((orb_size * 6, orb_size * 6), pygame.SRCALPHA)

                # Outer glow
                outer_color = (*color, int(30 + intensity * 50))
                pygame.draw.circle(glow_surf, outer_color,
                                 (orb_size * 3, orb_size * 3), orb_size * 2)

                # Middle glow
                mid_color = (*color, int(80 + intensity * 100))
                pygame.draw.circle(glow_surf, mid_color,
                                 (orb_size * 3, orb_size * 3), int(orb_size * 1.2))

                # Core
                core_color = (*color, int(150 + intensity * 105))
                pygame.draw.circle(glow_surf, core_color,
                                 (orb_size * 3, orb_size * 3), orb_size)

                self.screen.blit(glow_surf, (x - orb_size * 3, y - orb_size * 3))

        # 2. PULSING ENERGY RINGS on the beat
        if bass > 150:
            intensity = (bass - 150) / 105
            num_rings = int(intensity * 5) + 3

            for i in range(num_rings):
                # Rings emanate from monitor centers
                monitor = i % self.num_monitors
                cx = monitor * self.monitor_width + self.monitor_width // 2
                cy = self.height // 2

                # Expanding pulse
                phase = (self.time * 3 + i * 0.5) % 1
                radius = int(phase * 600 * beat_pulse)

                hue = (self.time * 100 + i * 40) % 360
                alpha = int((1 - phase) * (100 + intensity * 100))
                color = self.hsv_to_rgb(hue, 0.6, 0.5 + intensity * 0.3)

                # Draw pulsing ring with transparency
                ring_surf = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
                ring_color = (*color, alpha)
                pygame.draw.circle(ring_surf, ring_color, (radius + 5, radius + 5),
                                 radius, max(2, int(3 * beat_pulse)))

                self.screen.blit(ring_surf, (cx - radius - 5, cy - radius - 5))

        # 3. BEAT IMPACT ORBS - spawn on strong beats
        if bass > 200:
            intensity = (bass - 200) / 55
            num_impact = int(intensity * 8) + 4

            for i in range(num_impact):
                # Random positions
                x = np.random.randint(0, self.width)
                y = np.random.randint(0, self.height)

                # Large pulsing orbs
                size = int((15 + intensity * 40) * beat_pulse)

                # Bright impact colors
                hue = (self.time * 200 + i * 45) % 360
                color = self.hsv_to_rgb(hue, 0.8, 0.7 + intensity * 0.3)

                # Multi-layer impact orb
                glow_surf = pygame.Surface((size * 5, size * 5), pygame.SRCALPHA)

                # Outer explosion
                pygame.draw.circle(glow_surf, (*color, 40), (size * 2.5, size * 2.5), size * 2)
                # Middle ring
                pygame.draw.circle(glow_surf, (*color, 120), (size * 2.5, size * 2.5), int(size * 1.3))
                # Bright core
                pygame.draw.circle(glow_surf, (*color, 200), (size * 2.5, size * 2.5), size)

                self.screen.blit(glow_surf, (int(x - size * 2.5), int(y - size * 2.5)))

        # 4. SCREEN PULSE GLOW on beat
        if bass > 180:
            intensity = (bass - 180) / 75
            pulse_surf = pygame.Surface((self.width, self.height))

            # Warm pulsing glow
            hue = (self.time * 80) % 360
            glow_color = self.hsv_to_rgb(hue, 0.4, 0.3)
            pulse_surf.fill(glow_color)
            pulse_surf.set_alpha(int(intensity * 40 * beat_pulse))
            self.screen.blit(pulse_surf, (0, 0))

    def run(self):
        """Main loop"""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key in (K_ESCAPE, K_q):
                        running = False

            # Get audio data
            freq_data = self.get_audio_data()

            # Calculate frequency bands (matching HTML)
            third = len(freq_data) // 3
            bass = np.mean(freq_data[:third])
            mid = np.mean(freq_data[third:2*third])
            treble = np.mean(freq_data[2*third:])
            average = np.mean(freq_data)

            # Trailing effect (matching HTML)
            fade_amount = 0.15 - (bass / 255) * 0.1
            fade_alpha = int(fade_amount * 255)
            self.trail_surface.fill((0, 0, 0))
            self.trail_surface.set_alpha(fade_alpha)
            self.screen.blit(self.trail_surface, (0, 0))

            # Flash white on massive beats (matching HTML)
            if bass > 230:
                flash = pygame.Surface((self.width, self.height))
                flash.fill((255, 255, 255))
                flash.set_alpha(int((bass - 230) / 255 * 76))
                self.screen.blit(flash, (0, 0))

            # Update rotation speeds (matching HTML)
            self.target_rotation_speed = 0.02 + (bass / 255) * 0.3
            self.current_rotation_speed += (self.target_rotation_speed - self.current_rotation_speed) * 0.15

            self.rotation += self.current_rotation_speed
            self.rotation2 += self.current_rotation_speed * 0.7 + math.sin(self.time * 0.5) * 0.01
            self.rotation3 += self.current_rotation_speed * 1.3 + math.cos(self.time * 0.3) * 0.01
            self.time += 0.03

            # Draw on each monitor
            for monitor in range(self.num_monitors):
                self.draw_on_monitor(monitor, freq_data, bass, mid, treble, average)

            # Draw funky waveforms that span across ALL monitors
            self.draw_funky_waveforms(freq_data, bass, mid, treble, average)

            # Draw explosive high note effects
            self.draw_high_note_effects(freq_data, bass, mid, treble, average)

            pygame.display.flip()
            self.clock.tick(60)

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
        print("Starting FLUFFY triple monitor light show...")
        print("Ultra-smooth, cloud-like visuals - no harsh edges!")
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
