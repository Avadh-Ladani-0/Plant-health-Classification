# Plant Health Classification

This repository contains a notebook-first plant health classification workflow built around two data sources:

- spectrometer readings
- plant images

The repo supports three experiment styles:

- classical machine learning on spectra
- image-only deep learning
- multimodal fusion using spectra + images

The project has already been reorganized so that data, notebooks, scripts, and generated outputs live in predictable folders. This README is meant to help you use the repo efficiently without having to reverse-engineer the pipeline each time.

## Dataset Availability

The full `data/` folder is not stored in this Git repository.

The dataset is provided externally as a `.rar` archive on Google Drive:

- https://drive.google.com/drive/folders/1oe0ny592vZWtkdVWrjlIzYZmeV-e5nTl?usp=sharing

Download and extract that archive if the local `data/` directory is incomplete or missing.

After extraction, place the restored contents into this repository's `data/` folder so that paths such as `data/raw/imgs/`, `data/interim/`, and `data/processed/` match the notebook and script expectations.

## Repository Structure

```text
Plant Health Classifiacation/
  data/
    raw/
      imgs/                  # Canonical image directory used by the current notebooks
      aug/                   # Optional/archive augmented images, not the main training source
      spectra/
        before_espectro_18.csv
      misc/                  # Loose images not part of the main current pipeline
    interim/
      img_data.csv           # Image metadata extracted from raw images
      spectro_18.csv         # Preprocessed spectral data
    processed/
      plant_spectro_image_without_aug.csv
      aug_final_dataset.csv
    external/
      tvisha/                # External dataset archive, not used by the current notebook flow
  notebooks/
    metadata_extraction.ipynb
    spectro_preprocessing.ipynb
    Map.ipynb
    ML_spectro.ipynb
    classification.ipynb
    image_cnn.ipynb
    classification_2.ipynb
  scripts/
    augmenatation.py
    new_to_std_csv.py
    multimodalv2_epoch_wise_plot.py
  outputs/
    figures/
    metrics/
    predictions/
    reports/
  requirements.txt
  readme.md
```

## What Each Main Folder Is For

### `data/`

This is the working data area for the project.

- `data/raw/imgs/` is the main image source used by the current notebooks.
- the complete `data/` folder can be restored locally from the Google Drive archive linked above
- `data/raw/spectra/before_espectro_18.csv` is the raw spectral source file currently stored in the repo.
- `data/interim/` holds intermediate CSVs created during metadata extraction and spectrum preprocessing.
- `data/processed/` holds model-ready datasets.
- `data/external/tvisha/` is kept as external/archive data and is not used by the current notebook pipeline.

### `notebooks/`

These are the main entry points for data prep, analysis, training, and evaluation.

### `scripts/`

These are reusable utilities for:

- augmentation
- CSV normalization/conversion
- training curve plotting

### `outputs/`

All generated artifacts should go here:

- figures
- metrics CSVs
- prediction CSVs
- reports

## Core Datasets You Should Know

If you understand these files, the repo becomes much easier to work with:

- `data/interim/img_data.csv`
  Image metadata extracted from files in `data/raw/imgs/`.

- `data/interim/spectro_18.csv`
  Preprocessed spectral data used during dataset merging.

- `data/processed/plant_spectro_image_without_aug.csv`
  The main merged image + spectra dataset before augmentation.

- `data/processed/aug_final_dataset.csv`
  The augmented processed dataset used by the image and multimodal notebooks.

In practice:

- use `plant_spectro_image_without_aug.csv` for non-augmented experiments
- use `aug_final_dataset.csv` for augmented image-based and multimodal runs

## Environment Setup

The repo is easiest to use from the project root.

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start Jupyter or use VS Code notebooks

```powershell
jupyter lab
```

`requirements.txt` includes the packages needed by the current notebooks and scripts, including `tensorflow`, `torch`, `torchvision`, `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `Pillow`, and `pillow-heif`.

`pillow-heif` matters because the dataset includes `.heic` images.

## Fastest Way To Start

If you do not need to rebuild the data pipeline from scratch, start with the already prepared processed CSVs:

1. Install dependencies.
2. Open the repo in VS Code or Jupyter.
3. Run one of the model notebooks directly:
   - `notebooks/ML_spectro.ipynb`
   - `notebooks/classification.ipynb`
   - `notebooks/image_cnn.ipynb`
   - `notebooks/classification_2.ipynb`
4. Check generated artifacts under `outputs/`.

This is the most efficient path if your goal is to reproduce or iterate on model experiments rather than regenerate metadata and merged datasets.

## Full Pipeline Order

Use this order if you want to understand or rebuild the full project workflow.

### Step 1. Extract image metadata

Run:

- `notebooks/metadata_extraction.ipynb`

Purpose:

- reads images from `data/raw/imgs/`
- extracts metadata from `.jpg` and `.heic` files
- writes `data/interim/img_data.csv`

### Step 2. Prepare spectral data

Run:

- `notebooks/spectro_preprocessing.ipynb`

Purpose:

- reads `data/interim/img_data.csv`
- works with spectral CSV data
- updates or rewrites `data/interim/spectro_18.csv`

### Step 3. Merge image and spectral data

Run:

- `notebooks/Map.ipynb`

Purpose:

- combines image metadata and spectral features
- produces `data/processed/plant_spectro_image_without_aug.csv`

### Step 4. Optionally augment the dataset

Run:

- `scripts/augmenatation.py`

Purpose:

- expands the image set by generating augmented copies
- writes a larger CSV such as `data/processed/aug_final_dataset.csv`

### Step 5. Train and evaluate models

Use one or more of the following notebooks:

- `notebooks/ML_spectro.ipynb` for classical ML on spectra
- `notebooks/classification.ipynb` for multimodal training on the non-augmented dataset
- `notebooks/image_cnn.ipynb` for image-only deep learning
- `notebooks/classification_2.ipynb` for augmented multimodal experiments

## Notebook Guide

| Notebook | Main Input | Main Output | Use It When |
| --- | --- | --- | --- |
| `metadata_extraction.ipynb` | `data/raw/imgs/` | `data/interim/img_data.csv` | You want to rebuild image metadata from raw images |
| `spectro_preprocessing.ipynb` | `data/interim/img_data.csv`, spectral CSVs | `data/interim/spectro_18.csv` | You want to clean or align spectral readings |
| `Map.ipynb` | `data/interim/img_data.csv`, `data/interim/spectro_18.csv` | `data/processed/plant_spectro_image_without_aug.csv` | You want the merged non-augmented dataset |
| `ML_spectro.ipynb` | `data/processed/plant_spectro_image_without_aug.csv` | prediction CSVs in `outputs/predictions/` | You want tabular ML baselines using spectra only |
| `classification.ipynb` | `data/processed/plant_spectro_image_without_aug.csv`, `data/raw/imgs/` | training/evaluation artifacts | You want multimodal training without augmentation |
| `image_cnn.ipynb` | `data/processed/aug_final_dataset.csv`, `data/raw/imgs/` | prediction CSVs in `outputs/predictions/` | You want image-only CNN experiments |
| `classification_2.ipynb` | `data/processed/aug_final_dataset.csv`, `data/raw/imgs/` | prediction CSVs in `outputs/predictions/` | You want augmented multimodal experiments |

## Script Guide

### `scripts/new_to_std_csv.py`

Use this when you have a raw spectral CSV in another layout and want to convert it into the standardized schema used by this project.

Example:

```powershell
python scripts\new_to_std_csv.py input.csv output.csv --records-prefix rec --image-template "IMG_{num}.jpg" --folder-base dataset
```

What it does:

- auto-detects label and image-number columns unless you override them
- keeps numeric spectral band columns
- writes a standardized CSV with columns such as:
  - `Records`
  - `class_s`
  - spectral columns like `410`, `435`, ...
  - `image_name`
  - `folder`
  - `class(h,u)`

### `scripts/augmenatation.py`

Use this when you want to generate augmented image samples and an expanded training CSV.

Example:

```powershell
python scripts\augmenatation.py `
  --csv data\processed\plant_spectro_image_without_aug.csv `
  --images_root data\raw\imgs `
  --out_images_root data\raw\imgs `
  --out_csv data\processed\aug_final_dataset.csv `
  --target_count 500 `
  --seed 42
```

Important:

- the current notebooks load images from `data/raw/imgs/`
- if you save augmented images somewhere else, you must also make sure the CSV paths still match where the notebooks expect the files to be

### `scripts/multimodalv2_epoch_wise_plot.py`

Use this after you have an epoch-wise metrics CSV.

Example:

```powershell
python scripts\multimodalv2_epoch_wise_plot.py
```

Expected input:

- `outputs/metrics/epoch_wise_stats.csv`

Generated outputs:

- `outputs/figures/accuracy_smooth.png`
- `outputs/figures/loss_smooth.png`

## Outputs

The repo already separates generated artifacts from source files.

### `outputs/predictions/`

Example files:

- `decision_tree_predictions.csv`
- `fusionmodel_predictions.csv`
- `fusionmodel_preds_min.csv`
- `vgglite_predictions.csv`
- `vgglite_preds_min.csv`

### `outputs/metrics/`

Example file:

- `epoch_wise_stats.csv`

### `outputs/figures/`

Contains plots and comparison figures such as smoothed training curves and model comparison charts.

### `outputs/reports/`

Contains report files generated or collected for the project.

## Efficient Working Tips

- Work from the repository root whenever possible.
- Use the processed CSVs first if your goal is model development, evaluation, or reporting.
- Treat `outputs/` as regenerable artifacts unless you specifically want to preserve experiment history.
- Use `data/raw/imgs/` as the canonical image location for the current notebooks.
- Keep `data/external/tvisha/` separate in your mental model; it is not part of the current core pipeline.

## Important Notes And Caveats

- The notebook source paths were updated to match the reorganized structure.
- Some notebooks still contain old saved output cells from before the reorganization. If you see printed paths like old `RAW/...` locations inside notebook outputs, that is stale output text, not the current source code.
- `metadata_extraction.ipynb` and `spectro_preprocessing.ipynb` use `../data/...` style paths. If either notebook throws a path error in your environment, run it in a notebook session whose working directory matches the `notebooks/` folder structure.
- `data/raw/aug/` exists, but the current training notebooks primarily use image paths under `data/raw/imgs/`.
- `data/external/tvisha/` is preserved as external/archive data and is not part of the current main experiment flow.
- Scratch files such as `ex.ipynb` and `ex.py` are still in the repo root and can be cleaned up later.

## Suggested Usage Patterns

### If you want the quickest usable result

1. Install dependencies.
2. Open `notebooks/image_cnn.ipynb` or `notebooks/classification_2.ipynb`.
3. Use `data/processed/aug_final_dataset.csv`.
4. Inspect outputs in `outputs/predictions/` and `outputs/figures/`.

### If you want a clean end-to-end rerun

1. Run `metadata_extraction.ipynb`.
2. Run `spectro_preprocessing.ipynb`.
3. Run `Map.ipynb`.
4. Optionally run `scripts/augmenatation.py`.
5. Run the modeling notebooks.

### If you want only a tabular spectral baseline

1. Use `data/processed/plant_spectro_image_without_aug.csv`.
2. Run `notebooks/ML_spectro.ipynb`.
3. Read prediction outputs from `outputs/predictions/`.

## Summary

The most important idea in this repo is:

- `data/raw/` stores sources
- `data/interim/` stores intermediate tables
- `data/processed/` stores model-ready CSVs
- `notebooks/` runs the workflow
- `scripts/` provides reusable utilities
- `outputs/` stores generated results

If you are unsure where to begin, start with `data/processed/aug_final_dataset.csv` plus `notebooks/image_cnn.ipynb` or `notebooks/classification_2.ipynb`.
