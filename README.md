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

Two realistic paths, in order of effort:

1. **Classical feature matching (ORB/SIFT)** against a reference photo of
   your *specific* earphones. No training data needed, fast to build, works
   well for one known object — but won't generalize to earphones in general,
   only that exact pair.
2. **A small trained detector** (e.g. YOLOv8n via the `ultralytics` package)
   fine-tuned on ~100–200 labeled photos of your desk with/without the
   earphones in different spots. More setup (need to shoot and label photos),
   but generalizes better and gives you real precision/recall numbers to
   report against the proposal's stated benchmarks (≥92% precision, ≥88%
   recall).

Given the competition timeline, option 1 gets an end-to-end demo working
fastest. Worth switching to option 2 once Phase 3 (lighting robustness) and
Phase 4 (spatial audio) are wired up, since detection is the piece most
likely to need iteration and real data.
