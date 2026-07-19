#!/usr/bin/env python3
"""
Reorganize the CompCars dataset into a car_type/make/model/year folder tree.

This script reads the raw CompCars "make/model/year" image folders together with
the provided .mat metadata files, and copies the images into a clean, human-readable
hierarchy:

    <DST_ROOT>/<car_type>/<make>/<model>/<year>/*.jpg

Only model/year folders that contain at least MIN_IMAGES images are kept.

Requirements:
    pip install scipy

CompCars dataset (non-commercial research use only):
    https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/
"""

import os
import shutil
import scipy.io

# ======================
# PATH SETTINGS  (edit these)
# ======================
SRC_ROOT = "./CompCars/dataset_images_60plus"          # raw make/model/year folders
DST_ROOT = "./CompCars_structured"                     # output (MUST be outside SRC_ROOT)
MAKE_MODEL_MAT = "./CompCars/misc/make_model_name.mat"
CAR_TYPE_MAT = "./CompCars/misc/car_type.mat"

MIN_IMAGES = 60

# CompCars car-type ids -> readable names
CAR_TYPE_MAP = {
    1: "sedan",
    2: "suv",
    3: "hatchback",
    4: "coupe",
    5: "wagon",
}


# ======================
# Load .mat metadata
# ======================
mm = scipy.io.loadmat(MAKE_MODEL_MAT)
ct = scipy.io.loadmat(CAR_TYPE_MAT)

model_names = mm["model_names"].squeeze()
car_types = ct["types"].squeeze()


def mat_str(x):
    """Recursively unwrap a MATLAB string cell into a plain Python str."""
    if isinstance(x, str):
        return x
    if hasattr(x, "__len__"):
        return mat_str(x[0])
    return str(x)


# ======================
# Main loop
# ======================
def main():
    for make_model_id in os.listdir(SRC_ROOT):
        # only numeric folders
        if not make_model_id.isdigit():
            continue

        mm_path = os.path.join(SRC_ROOT, make_model_id)
        if not os.path.isdir(mm_path):
            continue

        idx = int(make_model_id) - 1
        # bounds check
        if idx < 0 or idx >= len(model_names):
            continue

        full_name = mat_str(model_names[idx]).strip()
        parts = full_name.split(" ", 1)
        make = parts[0]
        model = parts[1] if len(parts) > 1 else "UnknownModel"

        car_type_id = int(car_types[idx])
        car_type = CAR_TYPE_MAP.get(car_type_id, "unknown")

        for year_folder in os.listdir(mm_path):
            year_path = os.path.join(mm_path, year_folder)
            if not os.path.isdir(year_path):
                continue

            images = [
                f for f in os.listdir(year_path)
                if f.lower().endswith(".jpg")
            ]
            if len(images) < MIN_IMAGES:
                continue

            dst_dir = os.path.join(DST_ROOT, car_type, make, model, year_folder)
            os.makedirs(dst_dir, exist_ok=True)

            for img in images:
                src_img = os.path.join(year_path, img)
                dst_img = os.path.join(dst_dir, img)
                if not os.path.exists(dst_img):
                    shutil.copy2(src_img, dst_img)

        print(f"OK  {car_type}/{make}/{model}")

    print("Done. Dataset reorganization complete.")


if __name__ == "__main__":
    main()
