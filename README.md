# GlobiCLI

Ever wanted to see the world spinning in your terminal? Well, here it is (it's open source, btw).

## What is this!

<img width="1366" height="768" alt="screenshot-2026-07-28_23-14-38" src="https://github.com/user-attachments/assets/bca4cff2-1f76-47e5-a06d-c048b1dc409a" />


GlobiCLI is a little side project that turns your terminal into a spinning 3D globe — no GUI, no game engine, no fancy renderer. Just Python, NumPy doing the math, and a bunch of ANSI escape codes tricking your terminal into drawing something that looks way cooler than it has any right to.

It's not trying to be geographically perfect or scientifically accurate. It's the kind of thing you run just to watch for a minute, maybe leave open in a spare terminal pane while you work, and go "huh, neat" every time you glance at it.

## How it actually works

<img width="5000" height="1451" alt="python" src="https://github.com/user-attachments/assets/823ad038-c58d-4344-856f-7f88dc19c4bd" />

Under the hood there's a real sphere being projected in camera space every single frame — rays get cast, hit points get calculated, a rotation matrix spins the whole thing, and a simple directional light figures out which side should look brighter and which side should fade toward the terminator. All of that runs as vectorized NumPy operations instead of a slow pixel-by-pixel loop, which is the only reason it stays smooth at 24 FPS instead of chugging along like a slideshow.

The land itself comes from real country polygon data — longitude/latitude points traced out by hand off a low-res map, so don't expect perfectly accurate borders. A few disputed or tricky territories got merged into their neighbors rather than split out properly. It's ASCII art, not a GIS tool — nobody's plotting a shipping route with this thing.

About 70 countries get labeled too, each with a little dotted line pointing from its spot on the globe out to its name at the edge of the terminal — kind of like those infographic world maps you see in magazines, except yours is spinning and made entirely of text characters.

And because a perfectly clean render felt a little too sterile, there's an occasional cosmetic glitch built in — every so often a handful of characters on screen flash into static-looking symbols in random bright colors for a single frame, like a satellite feed cutting out for a split second. It doesn't touch anything underneath, it's just there to make the whole thing feel a little less like a polished demo and a little more alive.

## Requirements

- Python 3
- NumPy
- A real POSIX terminal — Linux or macOS. It leans on `termios`/`tty` for raw keyboard input, so Windows users will need WSL or something similar.

## Running it

```bash
pip install numpy
python3 GlobiCLI.py
```

That's it. No config files, no setup wizard, no accounts. Just run it and the globe shows up.

## Controls

| Key | What it does |
|-----|---------------|
| `+` / `-` | Speed the rotation up or slow it down |
| `space` | Pause / resume |
| `r` | Reset back to default speed and position |
| `q` | Quit and hand your terminal back |

It also just handles resizing your terminal window mid-run — the globe redraws itself to fit, no restart needed.

## A few honest caveats

- Border accuracy is "good enough to look right at a glance," not survey-grade.
- This was built for fun, not for production anything. Treat it accordingly.

