"""Download and split the official PlantVillage color image dataset."""

import importlib.util
import os
import subprocess
import sys
import zipfile

import splitfolders


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_ROOT = os.path.join(PROJECT_ROOT, "data", "raw", "PlantVillage")
COLOR_DATA_DIR = os.path.join(RAW_ROOT, "color")
SPLIT_DATA_DIR = os.path.join(
    PROJECT_ROOT, "data", "processed", "PlantVillage_Official_Split"
)
KAGGLE_DATASET = "abdallahalidev/plantvillage-dataset"
EXPECTED_CLASS_COUNT = 38


def _existing_color_directory():
    candidates = [
        COLOR_DATA_DIR,
        os.path.join(RAW_ROOT, "plantvillage dataset", "color"),
        os.path.join(
            PROJECT_ROOT,
            "data",
            "raw",
            "temp_plantvillage-dataset",
            "plantvillage dataset",
            "color",
        ),
    ]
    for candidate in candidates:
        if os.path.isdir(candidate) and len(
            [name for name in os.listdir(candidate) if os.path.isdir(os.path.join(candidate, name))]
        ) == EXPECTED_CLASS_COUNT:
            return candidate
    return None


def ensure_dataset():
    source = _existing_color_directory()
    if source:
        return source

    if importlib.util.find_spec("kaggle") is None:
        raise RuntimeError(
            "Install the Kaggle CLI (`pip install kaggle`) and configure Kaggle API credentials."
        )

    os.makedirs(RAW_ROOT, exist_ok=True)
    subprocess.check_call([
        sys.executable,
        "-m",
        "kaggle",
        "datasets",
        "download",
        "-d",
        KAGGLE_DATASET,
        "-p",
        RAW_ROOT,
    ])

    archives = [
        os.path.join(RAW_ROOT, name)
        for name in os.listdir(RAW_ROOT)
        if name.endswith(".zip")
    ]
    if not archives:
        raise FileNotFoundError("Kaggle download completed without a PlantVillage zip file.")

    for archive in archives:
        with zipfile.ZipFile(archive) as dataset_zip:
            dataset_zip.extractall(RAW_ROOT)

    source = _existing_color_directory()
    if not source:
        raise FileNotFoundError(
            "The downloaded archive did not contain the expected 38 PlantVillage color classes."
        )
    return source


def split_dataset(source):
    if os.path.exists(SPLIT_DATA_DIR):
        existing_train = os.path.join(SPLIT_DATA_DIR, "train")
        existing_classes = (
            len([name for name in os.listdir(existing_train)
                 if os.path.isdir(os.path.join(existing_train, name))])
            if os.path.isdir(existing_train)
            else 0
        )
        if existing_classes == EXPECTED_CLASS_COUNT:
            print(f"PlantVillage split already exists at {SPLIT_DATA_DIR}.")
            return
        raise FileExistsError(
            f"{SPLIT_DATA_DIR} exists but is not a 38-class PlantVillage split. "
            "Move or rename that directory before creating the official split."
        )

    splitfolders.ratio(
        source,
        output=SPLIT_DATA_DIR,
        seed=42,
        ratio=(0.8, 0.2),
        group_prefix=None,
        move=False,
    )
    print(f"Created train/validation split at {SPLIT_DATA_DIR}.")


if __name__ == "__main__":
    dataset_dir = ensure_dataset()
    split_dataset(dataset_dir)
