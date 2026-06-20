eal-Time 3D Terminal Globe
I wanted to see if I could build a real-time, rotating 3D world globe that renders completely inside a terminal window without lagging, so I put this script together. It works by using matrix math to map a flat world outline onto a virtual sphere, and then throws a moving sun vector into the equation to calculate dynamic shadows, day/night cycles, and twilight blending on the fly.

(This project documentation was generated with the help of an AI to break down the features and technical requirements).

Features
Retro Terminal Visuals: Combines high-density Unicode shading blocks (▓, ▒, ░) for continents and ocean characters (~, ≈, ·) to give a stylized ASCII-art aesthetic.

Ambient Shading & Atmospheric Glow: Features real-time shading based on a simulated sun source, along with a soft blue-purple atmospheric gradient at the sphere's edge.

Procedural Starfield: Generates a randomized background starfield using brightness-scaled markers (· and *) that update naturally when resizing the screen.

High Performance (30 FPS): Leverages NumPy vectors to calculate full-frame strings in memory, jumping the terminal cursor (\x1b[H) to eliminate screen flickering.
