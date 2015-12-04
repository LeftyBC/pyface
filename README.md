# pyface
Simple script for doing face detection.  Writes a state file to `/tmp/facestatus.dat` when faces are detected on a webcam.

## Setup
```
sudo pip install -r requirements.txt
python main.py
```

## Caveats
- Probably not very efficient, as it polls the webcam every 100ms.
- Some detection parameters may need to be tweaked, and could probably be
  converted to command-line args.

