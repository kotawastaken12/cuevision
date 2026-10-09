"""
CUE - Phase 1 prototype loop.

Ties together camera capture, preprocessing, and quality diagnostics
into a live, on-screen demo. This is the Phase 1 milestone from the
proposal's six-phase roadmap: local video capture + OpenCV preprocessing,
running and visible end to end.

Controls:
  q - quit
  c - toggle CLAHE on/off
  b - toggle bilateral filtering on/off
"""

import cv2

from capture import Camera
from preprocessing import apply_clahe, apply_bilateral
from diagnostics import assess_frame


def draw_overlay(frame, quality, clahe_on, bilateral_on):
    color = (0, 200, 0) if quality.is_usable else (0, 0, 220)
    lines = [
        f"blur: {quality.blur_score:6.1f}   brightness: {quality.brightness:5.1f}",
        f"status: {quality.reason}",
        f"CLAHE [{'ON' if clahe_on else 'off'}] (c)   Bilateral [{'ON' if bilateral_on else 'off'}] (b)   Quit (q)",
    ]
    for i, line in enumerate(lines):
        cv2.putText(frame, line, (10, 25 + i * 25), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, color, 2, cv2.LINE_AA)
    return frame


def main():
    clahe_on = True
    bilateral_on = False

    with Camera(index=0) as cam:
        print("CUE Phase 1 prototype running. Press 'q' in the video window to quit.")
        while True:
            frame = cam.read()
            if frame is None:
                print("Camera read failed - stopping.")
                break

            processed = frame.copy()
            if clahe_on:
                processed = apply_clahe(processed)
            if bilateral_on:
                processed = apply_bilateral(processed)

            quality = assess_frame(processed)
            display = draw_overlay(processed.copy(), quality, clahe_on, bilateral_on)

            cv2.imshow("CUE - raw", frame)
            cv2.imshow("CUE - processed", display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                clahe_on = not clahe_on
            elif key == ord('b'):
                bilateral_on = not bilateral_on

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
