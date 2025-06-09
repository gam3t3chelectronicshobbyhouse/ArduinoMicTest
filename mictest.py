#!/usr/bin/env python3
"""
Microphone Visualizer V1.0
To use with Arduino Microphone checker you may need to adjust the COM port or other info
in the configuration below.

Make sure to install the following dependencies:
pip install pyserial numpy matplotlib

Gam3t3ch Electronics
http://Gam3t3ch.com
gam3t3ch@gmail.com
https://github.com/gam3t3chelectronicshobbyhouse
"""

import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# CONFIGURATION
PORT      = "COM10"       # your Arduino port
BAUD      = 230400         # must match Arduino Serial.begin rate
WINDOW    = 512            # number of samples in the rolling buffer
INTERVAL  = 20             # ms between frames (~50 FPS)
MIDLINE   = 512            # ADC midpoint for 10-bit Arduino
MARGIN    = 20             # margin around min/max for zoom

# Initialize serial connection
try:
    ser = serial.Serial(PORT, BAUD, timeout=0.01)
except Exception as e:
    print(f"Error opening port {PORT}: {e}")
    exit(1)

# Pre-fill buffer
data = np.full(WINDOW, MIDLINE, dtype=int)

# Set up plot
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 4), facecolor='#0A0A0A')
ax.set_facecolor('#0A0A0A')
line, = ax.plot(data, color='#00FFCC', lw=1)

# Clean UI (no axes or ticks)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Initial view limits
ax.set_xlim(0, WINDOW)
ax.set_ylim(MIDLINE - MARGIN, MIDLINE + MARGIN)
plt.tight_layout()

# Update function for animation
def update(frame):
    global data
    # Read all available samples from serial
    while ser.in_waiting:
        try:
            val = int(ser.readline().decode('utf-8', errors='ignore').strip())
        except:
            continue
        # Shift buffer left and append new sample
        data = np.roll(data, -1)
        data[-1] = val
    # Update the line
    line.set_ydata(data)
    # Dynamic zoom: compute min/max of buffer and adjust y-limits
    min_val = data.min()
    max_val = data.max()
    ax.set_ylim(min_val - MARGIN, max_val + MARGIN)
    return (line,)

# Start animation (cache_frame_data=False suppresses frame warning)
ani = FuncAnimation(
    fig, update,
    interval=INTERVAL,
    blit=True,
    cache_frame_data=False
)

plt.show()

# Clean up
ser.close()