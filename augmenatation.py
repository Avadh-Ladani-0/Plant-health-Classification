import os
import argparse
import random
import math
import uuid
from pathlib import Path
from pillow_heif import register_heif_opener

register_heif_opener()

import pandas as pd
from PIL import Image, ImageOps

def safe_join(root, subfolder, filename):
    # Normalize weird // in folder column like "ad1//u"
    subfolder = subfolder.replace("\\", os.sep).replace("//", os.sep)
    full = Path(root) / Path(subfolder) / filename
    return full

def ensure_dir_for_file(filepath: Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)

def augment_once(img: Image.Image):
    """
    Apply a random combination of flipping, rotation, and scaling,
    then return an image resized back to the original size.
    """
    w0, h0 = img.size
    out = img.copy()

    # --- Random flips ---
    if random.random() < 0.5:
        out = ImageOps.mirror(out)  # horizontal flip
    if random.random() < 0.2:
        out = ImageOps.flip(out)    # vertical flip (rarer)

    # --- Random rotation ---
    # Choose a small-to-moderate angle to avoid heavy cropping artifacts
    angle_choices = [-30, -20, -15, -10, -5, 5, 10, 15, 20, 30]
    angle = random.choice(angle_choices)
    # rotate with expansion then resize back
    out = out.rotate(angle, resample=Image.BICUBIC, expand=True)

    # --- Random scaling ---
    # Scale 0.85x–1.2x, then fit back to original canvas
    scale = random.uniform(0.85, 1.2)
    new_w = max(1, int(out.size[0] * scale))
    new_h = max(1, int(out.size[1] * scale))
    out = out.resize((new_w, new_h), resample=Image.BICUBIC)

    # --- Fit back to original size (center crop or pad) ---
    # 1) If larger than target, center-crop; if smaller, pad with edge pixels
    # Create a canvas and paste centered
    canvas = Image.new(mode=out.mode, size=(w0, h0))
    # If image smaller, first paste centered; if larger, crop
    if new_w >= w0 and new_h >= h0:
        # center-crop out to (w0,h0)
        left = (new_w - w0) // 2
        top = (new_h - h0) // 2
        out = out.crop((left, top, left + w0, top + h0))
        return out
    else:
        # paste centered; if one dimension larger, crop to fit after paste
        x = (w0 - new_w) // 2
        y = (h0 - new_h) // 2
        canvas.paste(out, (x, y))
        return canvas

def make_unique_name(base_name: str, suffix: str):
    stem = Path(base_name).stem
    ext = Path(base_name).suffix or ".jpg"
    return f"{stem}_{suffix}{ext}"

def main():
    parser = argparse.ArgumentParser(description="Augment images to reach target count while preserving spectral data in CSV.")
    parser.add_argument("--csv", required=True, help="Path to input CSV.")
    parser.add_argument("--images_root", required=True, help="Root directory where images are stored (folders in CSV are relative to this).")
    parser.add_argument("--out_images_root", required=True, help="Root directory where augmented images will be saved (mirrors folder structure).")
    parser.add_argument("--out_csv", required=True, help="Path to write the NEW CSV (original + augmented rows).")
    parser.add_argument("--target_count", type=int, default=500, help="Desired total image count (default: 500).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    args = parser.parse_args()

    random.seed(args.seed)

    df = pd.read_csv(args.csv)
    current_count = len(df)
    if current_count >= args.target_count:
        print(f"Already have {current_count} >= target {args.target_count}. Nothing to do.")
        df.to_csv(args.out_csv, index=False)
        return

    needed = args.target_count - current_count
    print(f"Current rows: {current_count}. Need to add: {needed}")

    # Sample rows WITH replacement for augmentation
    sample_idx = [random.randrange(0, current_count) for _ in range(needed)]

    # Column names to carry over (copy everything, then update name/records as needed)
    augmented_rows = []

    for i, idx in enumerate(sample_idx, start=1):
        row = df.iloc[idx]

        image_name = str(row["image_name"])
        folder = str(row["folder"])
        src_path = safe_join(args.images_root, folder, image_name)

        if not src_path.exists():
            print(f"[WARN] Source image not found, skipping: {src_path}")
            continue

        try:
            with Image.open(src_path) as im:
                im = im.convert("RGB")  # normalize
                aug_img = augment_once(im)
        except Exception as e:
            print(f"[ERROR] Failed to load/augment {src_path}: {e}")
            continue

        # New name & destination
        unique_suffix = f"aug{i:05d}"
        new_image_name = make_unique_name(image_name, unique_suffix)

        # Save to out_images_root / folder / new_image_name
        dst_path = safe_join(args.out_images_root, folder, new_image_name)
        ensure_dir_for_file(dst_path)

        try:
            # Quality=95 for JPEGs; if PNG, Pillow ignores quality
            aug_img.save(dst_path, quality=95)
        except Exception as e:
            print(f"[ERROR] Failed to save {dst_path}: {e}")
            continue

        # Build new CSV row: copy spectral data and labels exactly;
        # update image_name and (optionally) Records to reflect augmentation
        new_row = row.copy()
        new_row["image_name"] = new_image_name
        # Keep folder same as source; if you'd rather send augmented images to a specific subfolder,
        # you can change new_row["folder"] here.
        # new_row["folder"] = str(Path(folder) / "aug")  # <- optional alternative
        # Make a unique Records id if present
        if "Records" in df.columns:
            new_row["Records"] = f"{row['Records']}_{unique_suffix}"

        augmented_rows.append(new_row)

        if i % 25 == 0:
            print(f"Created {i}/{needed} augmented images...")

    if not augmented_rows:
        print("No augmented rows were created (check paths).")
        return

    df_aug = pd.DataFrame(augmented_rows)
    df_out = pd.concat([df, df_aug], ignore_index=True)

    print(f"Final count: {len(df_out)} rows (target {args.target_count}).")
    # If overshot the target due to missing images, we may still be below target.
    # Optional: top up again by re-running with a slightly larger 'needed' or check here.
    df_out.to_csv(args.out_csv, index=False)
    print(f"Wrote new CSV to: {args.out_csv}")

if __name__ == "__main__":
    main()
