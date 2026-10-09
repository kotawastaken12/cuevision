# CUE — Phase 1 Prototype

Local-first camera capture + OpenCV preprocessing + image-quality diagnostics.

This is **Phase 1** of the six-phase roadmap from the proposal: "CV Preprocess
(OpenCV 5 local)." It's a minimal, real, on-screen thing you can run today —
not a plan, an actual loop reading your webcam and showing you live
diagnostics on it.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
cd src
python main.py
```

Two windows will open: the raw feed, and the processed feed with a live
overlay showing blur score, brightness, and whether the frame currently
passes the quality check.

## Controls

- `q` — quit
- `c` — toggle CLAHE contrast correction on/off
- `b` — toggle bilateral filtering on/off

## What this demonstrates (mapped to the proposal)

- **Camera Input** → `capture.py` (`Camera` class)
- **OpenCV Preprocessing** → `preprocessing.py` (CLAHE, bilateral, Gaussian —
  Section 2.2)
- **Confidence Assessment** → `diagnostics.py` (blur via Laplacian variance,
  brightness via mean pixel intensity — flags frames too blurry/dark/bright
  to trust, per Section 2.2's "Image-Quality Diagnostics")

Toggle CLAHE on/off live and watch a dim or glare-y patch of your desk — that
side-by-side comparison is genuinely useful demo material for Act II of the
proposal's live demonstration playbook.

## Next: Phase 2 (object search — earphones)

Will figure out phase two