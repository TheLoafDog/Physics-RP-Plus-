# Physics-RP-Plus-
FinCode Hacks Hackathon submission. Graph visualisation for A-level physics students.

## What it does
Pick one of the A-level required practicals (RP1–RP12) from the sidebar, type in your
readings, and the app plots the (linearised) graph with a best-fit line. It shows the
gradient and y-intercept alongside the original and linearised equations for that practical.

## Requirements
- Python 3 with Tkinter (included with the python.org installers on Windows/macOS;
  on Debian/Ubuntu run `sudo apt install python3-tk`)
- matplotlib and numpy

## Install and run
```
pip install -r requirements.txt
python3 Main.py
```
Run it from the repository folder, since it reads `RP info.txt` by relative path.

## How to use
1. Click a practical in the sidebar.
2. Type an x and y reading into the two boxes and press the green button to add the point.
   Where the practical needs it, the app transforms your readings automatically
   (for example 1/L for RP1, ln(V) for RP9, cos θ for RP11).
3. Add more points: from two points onwards, the best-fit line, gradient and y-intercept appear.
4. To remove a point, press the red button next to it.
