import os
import numpy as np
from PIL import Image
from scipy.ndimage import binary_closing, binary_dilation

# ------------------------------
# Configuration
# ------------------------------
OUTPUT_WIDTH = 1024
OUTPUT_HEIGHT = 1536

MAX_CHAR_WIDTH = OUTPUT_WIDTH * 0.5     # 512 px
MAX_CHAR_HEIGHT = OUTPUT_HEIGHT * 0.5   # 768 px

PADDING = 10
UPWARD_SHIFT_RATIO = 0.07

INPUT_DIR = "input_pngs"
OUTPUT_DIR = os.path.expanduser("~/Desktop/retirees/resized/retry")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------
# Background Color Extraction
# ------------------------------
def detect_background_color(img):
    # Sample all 4 corners
    w, h = img.size
    samples = [
        img.getpixel((0, 0)),
        img.getpixel((w - 1, 0)),
        img.getpixel((0, h - 1)),
        img.getpixel((w - 1, h - 1)),
    ]

    # Convert to numpy for distance calculations
    samples_np = np.array([s[:3] for s in samples], dtype=np.int16)

    # Group colors by similarity (Manhattan distance)
    groups = []
    threshold = 12  # acceptable bg variation

    for color in samples_np:
        placed = False
        for g in groups:
            if np.abs(g[0] - color).sum() <= threshold:
                g.append(color)
                placed = True
                break
        if not placed:
            groups.append([color])

    # Choose the largest consensus group
    largest_group = max(groups, key=len)
    avg_color = np.mean(largest_group, axis=0).astype(np.int16)

    return avg_color

# ------------------------------
# Foreground Mask Creation
# ------------------------------
def build_foreground_mask(img, bg_color, threshold=10):
    rgb = np.array(img.convert("RGB"), dtype=np.int16)
    diff = np.abs(rgb - bg_color)

    # Use summed RGB difference so even small per-channel changes count
    dist = diff.sum(axis=2)
    mask = (dist > threshold).astype(np.uint8)
    return mask

# ------------------------------
# Clean mask with morphology
# ------------------------------
def clean_mask(mask):
    mask = binary_closing(mask, structure=np.ones((5,5))).astype(np.uint8)
    mask = binary_dilation(mask, structure=np.ones((5,5))).astype(np.uint8)
    return mask

# ------------------------------
# Mask -> bounding box
# ------------------------------
def mask_to_bbox(mask):
    coords = np.column_stack(np.where(mask > 0))
    if coords.size == 0:
        return None

    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    return (x_min, y_min, x_max, y_max)

# ------------------------------
# Scaling logic
# ------------------------------
def scale_factor(w, h):
    return min(MAX_CHAR_WIDTH / w, MAX_CHAR_HEIGHT / h)

# ------------------------------
# Main image logic
# ------------------------------
def resize_and_center(img_path):
    img = Image.open(img_path).convert("RGBA")
    filename = os.path.basename(img_path)

    # Detect solid background color
    bg_color = detect_background_color(img)

    # Build + clean mask
    raw_mask = build_foreground_mask(img, bg_color)
    mask = clean_mask(raw_mask)

    bbox = mask_to_bbox(mask)
    if bbox is None:
        print(f"No foreground found in {filename}")
        return

    x_min, y_min, x_max, y_max = bbox

    # Apply padding
    x_min = max(0, x_min - PADDING)
    y_min = max(0, y_min - PADDING)
    x_max = min(img.width, x_max + PADDING)
    y_max = min(img.height, y_max + PADDING)

    bbox_w = x_max - x_min
    bbox_h = y_max - y_min

    # Compute scale
    scale = scale_factor(bbox_w, bbox_h)

    # Crop character region
    crop = img.crop((x_min, y_min, x_max, y_max))
    new_w = int(bbox_w * scale)
    new_h = int(bbox_h * scale)
    resized_char = crop.resize((new_w, new_h), Image.LANCZOS)

    # Overwrite entire image with a solid background using detected bg_color
    background = Image.new(
        "RGBA",
        (OUTPUT_WIDTH, OUTPUT_HEIGHT),
        (int(bg_color[0]), int(bg_color[1]), int(bg_color[2]), 255),
    )

    # Composite character onto background
    canvas = background.copy()

    # Positioning
    x = (OUTPUT_WIDTH - new_w) // 2
    shift_y = int(OUTPUT_HEIGHT * UPWARD_SHIFT_RATIO)
    y = ((OUTPUT_HEIGHT - new_h) // 2) - shift_y

    canvas.paste(resized_char, (x, y), resized_char)

    out_path = os.path.join(OUTPUT_DIR, filename)
    canvas.save(out_path)
    print(f"Saved {out_path}")

# ------------------------------
# Runner
# ------------------------------
def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".png")]
    if not files:
        print(f"No PNGs found in {INPUT_DIR}/")
        return

    for f in files:
        resize_and_center(os.path.join(INPUT_DIR, f))

if __name__ == "__main__":
    main()