# Plant-Health-Classification

This repository contains a Jupyter Notebook-based project focused on plant health classification using a combination of spectrometer data, images, and computer vision techniques.  The goal is to develop a robust model capable of accurately identifying healthy and unhealthy plants based on spectral signatures and visual characteristics.

## Project Overview

Plant health is crucial for agriculture and environmental monitoring. Traditional methods of assessing plant health are often time-consuming and labor-intensive. This project explores the use of hyperspectral imaging and computer vision to provide a more efficient and accurate alternative. By analyzing both spectral data obtained from a spectrometer and visual information from images, we aim to create a classification model that can identify various plant health conditions. Data Augumentation Techniques were also used in order to avoid overfitting of the results.

## Technologies Used

* **Python:** The primary programming language.
* **Jupyter Notebook:**  Used for development, documentation, and reproducibility.
* **Pandas:** For data manipulation and analysis.
* **Pillow (PIL):** For image processing.
* **pillow_heif:** For handling HEIC image files.


## Repository Structure

The repository is organized as follows:

* **`.gitignore`:** Specifies files and directories to be excluded from version control (e.g., temporary files, virtual environments).  See contents below.
* **`Map.ipynb`:** The main Jupyter Notebook containing the core data processing and analysis logic.  This notebook merges spectrometer and image data, preprocesses the data, and prepares it for model training (see example contents below).
* **`before_espectro_18.csv`:** Raw spectrometer data before preprocessing.
* **`metadata_extraction.ipynb`:** A Jupyter Notebook dedicated to extracting metadata (e.g., date, time, camera information) from image files. This notebook handles both JPG and HEIC formats and generates a CSV file containing the extracted metadata (see example contents below).
* **`plant_spectro_image_processed.csv`:** The final processed dataset combining spectrometer data and image metadata, ready for model training.
* **`requirements.txt`:** Lists all project dependencies, making it easy to recreate the development environment.
* **`spectro_18.csv`:** Processed spectrometer data after preprocessing steps.
* **`spectro_preprocessing.ipynb`:** A Jupyter Notebook detailing the preprocessing steps applied to the raw spectrometer data (see example contents below).


### .gitignore contents:

```
ex.ipynb
ex.py
.venv
RAW
img_data.csv
repo.txt
```

### Map.ipynb (Excerpt):

This notebook demonstrates merging spectrometric and image data.  It shows example data cleaning and preparation steps.

```python
import pandas as pd

sp=pd.read_csv('spectro_18.csv')
id=pd.read_csv('img_data.csv')

# ... (Further code for data cleaning and merging) ...
```


### metadata_extraction.ipynb (Excerpt):

This notebook shows how image metadata is extracted.

```python
import pandas as pd
import os
from PIL import Image
from pillow_heif import register_heif_opener
register_heif_opener()

# ... (Code to iterate through images, extract metadata, and create img_data.csv) ...
```

### spectro_preprocessing.ipynb (Excerpt):

This notebook demonstrates preprocessing steps for the spectroscopic data.

```python
import pandas as pd

# ... (Code to load raw spectro data, clean it, and save to spectro_18.csv) ...
```


## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your_username>/Plant-health-Classification.git
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Jupyter Notebooks:** Open `Map.ipynb`, `metadata_extraction.ipynb`, and `spectro_preprocessing.ipynb` in Jupyter Notebook and execute the cells sequentially.  Ensure the `RAW` directory containing the image data is present and correctly referenced within `metadata_extraction.ipynb`.


## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

[Specify your license here, e.g., MIT License]
