#!/usr/bin/env python3
import argparse
import pandas as pd
import re
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser(description="Convert plant spectra CSV to target format.")
    p.add_argument("input_csv", help="Path to input CSV")
    p.add_argument("output_csv", help="Path to write the converted CSV")
    # How to build new fields:
    p.add_argument("--records-prefix", default="rec",
                   help="Prefix for 'Records' column; final value = {prefix}_{Image_number}")
    p.add_argument("--image-template", default="IMG_{num}.jpg",
                   help="Template for image_name. Use {num} for Image_number (e.g., 'IMG_{num}.jpg')")
    p.add_argument("--folder-base", default="dataset",
                   help="Base folder name; final 'folder' value = {base}//{class_char}")
    p.add_argument("--label-col", default=None,
                   help="Exact name of the label column if it differs. If not set, script will detect it.")
    p.add_argument("--imagenum-col", default=None,
                   help="Exact name of the image number column if it differs. If not set, script will detect it.")
    return p.parse_args()

def detect_columns(df, label_col, imagenum_col):
    # Try to detect the label & image number columns
    if label_col is None:
        # Look for a column that contains "Label" (case-insensitive)
        cands = [c for c in df.columns if "label" in str(c).lower()]
        if not cands:
            # fall back to the first column
            label_col = df.columns[0]
        else:
            label_col = cands[0]
    if imagenum_col is None:
        # Look for a column containing "image" and maybe "number"
        cands = [c for c in df.columns if ("image" in str(c).lower() and "num" in str(c).lower())]
        if not cands:
            # fallback: try exact 'Image_number' or the second column
            imagenum_col = "Image_number" if "Image_number" in df.columns else df.columns[1]
        else:
            imagenum_col = cands[0]
    return label_col, imagenum_col

def class_from_label(label: str) -> str:
    """
    Map raw label text (e.g., 'healthy_404' or 'unhealty_517') -> 'h' or 'u'.
    Robust to typos/case like 'unhealty', 'unhealthy'.
    """
    s = str(label).lower().strip()
    if s.startswith("healthy"):
        return "h"
    # treat any non-healthy as unhealthy
    return "u"

def extract_num_from_label(label: str):
    """Optionally grab trailing digits from label like 'healthy_404' -> 404 (string)."""
    m = re.search(r"(\d+)$", str(label))
    return m.group(1) if m else None

def main():
    args = parse_args()
    df = pd.read_csv(args.input_csv)

    # Detect columns
    label_col, imagenum_col = detect_columns(df, args.label_col, args.imagenum_col)

    # Identify spectral columns: all numeric column headers (e.g., 410, 435, ..., 940)
    # Keep order as they appear.
    spectral_cols = []
    for c in df.columns:
        # skip the detected label/image columns
        if c == label_col or c == imagenum_col:
            continue
        try:
            # header may be numeric like 410, 435
            float(c)  # succeeds for '410' etc.
            spectral_cols.append(c)
        except Exception:
            # ignore non-numeric headers
            pass

    if not spectral_cols:
        raise ValueError("No spectral columns detected. Make sure the band headers are numeric like 410, 435, ...")

    # Build class char from label
    cls_char = df[label_col].apply(class_from_label)

    # Build Records
    # Use Image_number when present; fallback to number parsed from label; else row index.
    label_num = df[label_col].apply(extract_num_from_label)
    img_num_series = None
    if imagenum_col in df.columns:
        img_num_series = df[imagenum_col].astype(str)
    else:
        img_num_series = label_num.fillna(df.index.astype(str))

    records = args.records_prefix + "_" + img_num_series

    # class_s and class(h,u) are same short char
    class_s = cls_char
    class_hu = cls_char

    # image_name from template
    image_name = img_num_series.apply(lambda n: args.image_template.format(num=n))

    # folder base + // + class_char
    folder = cls_char.apply(lambda c: f"{args.folder_base}//{c}")

    # Reorder columns per spec:
    # Index column (blank name) will be the default pandas index; we won't name it.
    # Columns: Records, class_s, [spectral_cols in ascending numeric order], image_name, folder, class(h,u)
    # Sort spectral columns numerically based on header value
    spectral_cols_sorted = sorted(spectral_cols, key=lambda x: float(x))

    out = pd.DataFrame({
        "Records": records,
        "class_s": class_s
    })

    # Attach spectral columns in sorted order
    for c in spectral_cols_sorted:
        out[c] = df[c]

    out["image_name"] = image_name
    out["folder"] = folder
    out["class(h,u)"] = class_hu

    # Write CSV with a leading unnamed index (to mimic the sample with "0, ...")
    out.to_csv(args.output_csv, index=True, index_label="")

    print(f"✅ Wrote {len(out)} rows to {args.output_csv}")
    print(f"Columns: {', '.join(out.columns)}")

if __name__ == "__main__":
    main()
