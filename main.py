#!/usr/bin/env python3
"""
globe.py — Real-time rotating 3D globe in the terminal.

Controls:
  q / Ctrl+C  — quit
  SPACE        — pause / resume rotation
  +  /  -      — speed up / slow down
  w / s        — tilt sun up / down (season simulation)
  a / d        — shift sun east / west
  r            — reset to defaults
"""

import sys, os, math, time, select, tty, termios, signal
import numpy as np

_MAP_W = 180
_MAP_H = 90
