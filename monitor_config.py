#!/usr/bin/env python3
"""
Monitor Configuration System
Auto-detects or manually configures monitor setup for light show
"""

import subprocess
import re
import json
import os
import sys

class MonitorConfig:
    """Detects and manages monitor configuration"""

    def __init__(self, config_file='monitor_config.json'):
        self.config_file = config_file
        self.monitors = []
        self.total_width = 0
        self.total_height = 0
        self.num_monitors = 0

    def auto_detect(self):
        """Auto-detect monitor setup using xrandr"""
        try:
            output = subprocess.check_output(['xrandr', '--query'], text=True)

            # Parse connected monitors with resolution and position
            # Format: "DP-2-2 connected 1920x1080+0+0"
            pattern = r'(\S+) connected (?:primary )?(\d+)x(\d+)\+(\d+)\+(\d+)'
            matches = re.findall(pattern, output)

            if not matches:
                print("Warning: No monitors detected via xrandr")
                return False

            self.monitors = []
            for name, width, height, x, y in matches:
                monitor = {
                    'name': name,
                    'width': int(width),
                    'height': int(height),
                    'x': int(x),
                    'y': int(y)
                }
                self.monitors.append(monitor)

            # Sort by x position (left to right)
            self.monitors.sort(key=lambda m: m['x'])

            # Calculate total dimensions
            self.num_monitors = len(self.monitors)

            # Find bounding box of all monitors
            if self.monitors:
                min_x = min(m['x'] for m in self.monitors)
                max_x = max(m['x'] + m['width'] for m in self.monitors)
                min_y = min(m['y'] for m in self.monitors)
                max_y = max(m['y'] + m['height'] for m in self.monitors)

                self.total_width = max_x - min_x
                self.total_height = max_y - min_y

            print(f"✓ Detected {self.num_monitors} monitor(s)")
            for i, m in enumerate(self.monitors):
                print(f"  Monitor {i+1}: {m['name']} - {m['width']}x{m['height']} at ({m['x']}, {m['y']})")
            print(f"✓ Total screen space: {self.total_width}x{self.total_height}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error running xrandr: {e}")
            return False
        except Exception as e:
            print(f"Error detecting monitors: {e}")
            return False

    def load_config(self):
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_file):
            return False

        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)

            self.monitors = data.get('monitors', [])
            self.total_width = data.get('total_width', 0)
            self.total_height = data.get('total_height', 0)
            self.num_monitors = len(self.monitors)

            print(f"✓ Loaded config from {self.config_file}")
            print(f"  {self.num_monitors} monitor(s), {self.total_width}x{self.total_height} total")
            return True

        except Exception as e:
            print(f"Error loading config: {e}")
            return False

    def save_config(self):
        """Save current configuration to JSON file"""
        try:
            data = {
                'monitors': self.monitors,
                'total_width': self.total_width,
                'total_height': self.total_height,
                'num_monitors': self.num_monitors
            }

            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"✓ Saved config to {self.config_file}")
            return True

        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def manual_config(self, num_monitors, width_per_monitor=1920, height_per_monitor=1080, layout='horizontal'):
        """Manually configure monitors"""
        self.num_monitors = num_monitors
        self.monitors = []

        if layout == 'horizontal':
            # Monitors side by side
            for i in range(num_monitors):
                monitor = {
                    'name': f'Monitor{i+1}',
                    'width': width_per_monitor,
                    'height': height_per_monitor,
                    'x': i * width_per_monitor,
                    'y': 0
                }
                self.monitors.append(monitor)

            self.total_width = num_monitors * width_per_monitor
            self.total_height = height_per_monitor

        elif layout == 'vertical':
            # Monitors stacked vertically
            for i in range(num_monitors):
                monitor = {
                    'name': f'Monitor{i+1}',
                    'width': width_per_monitor,
                    'height': height_per_monitor,
                    'x': 0,
                    'y': i * height_per_monitor
                }
                self.monitors.append(monitor)

            self.total_width = width_per_monitor
            self.total_height = num_monitors * height_per_monitor

        print(f"✓ Configured {self.num_monitors} monitor(s) in {layout} layout")
        print(f"  Total: {self.total_width}x{self.total_height}")

        return True

    def get_monitor_centers(self):
        """Get the center point of each monitor for visualization placement"""
        centers = []
        for m in self.monitors:
            center_x = m['x'] + m['width'] // 2
            center_y = m['y'] + m['height'] // 2
            centers.append((center_x, center_y))
        return centers

    def get_config_dict(self):
        """Return configuration as dictionary for easy access"""
        return {
            'num_monitors': self.num_monitors,
            'total_width': self.total_width,
            'total_height': self.total_height,
            'monitors': self.monitors,
            'monitor_centers': self.get_monitor_centers()
        }

def main():
    """Test/demo the monitor configuration"""
    print("Monitor Configuration Tool")
    print("=" * 50)

    config = MonitorConfig()

    # Try auto-detection first
    if config.auto_detect():
        print("\n✓ Auto-detection successful!")

        # Offer to save
        save = input("\nSave this configuration? (y/n): ").lower()
        if save == 'y':
            config.save_config()
    else:
        # Manual configuration
        print("\nAuto-detection failed. Let's configure manually.")

        try:
            num = int(input("Number of monitors: "))
            width = int(input("Width per monitor (default 1920): ") or "1920")
            height = int(input("Height per monitor (default 1080): ") or "1080")
            layout = input("Layout (horizontal/vertical, default horizontal): ") or "horizontal"

            config.manual_config(num, width, height, layout)

            save = input("\nSave this configuration? (y/n): ").lower()
            if save == 'y':
                config.save_config()
        except ValueError:
            print("Invalid input!")
            return 1

    # Display final config
    print("\n" + "=" * 50)
    print("Final Configuration:")
    print(json.dumps(config.get_config_dict(), indent=2))

    return 0

if __name__ == "__main__":
    sys.exit(main())
