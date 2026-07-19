# Multi-Stage 3D Vehicle Reconstruction Pipeline

🌐 **[Project Page](https://ardasdasdas.github.io/vehicle-3dgs/)** &nbsp;|&nbsp; 📄 [Paper](https://doi.org/10.65520/erciyesfen.1918173) &nbsp;|&nbsp; 🤗 [Dataset](https://huggingface.co/datasets/muzafferardauslu/vehicle-3dgs)

Code for the paper **"A Multi-Stage Pipeline for 3D Reconstruction of Vehicles from
Heterogeneous Multi-View Images"** (Uslu & Kaplan Berkaya, 2026). DOI: https://doi.org/10.65520/erciyesfen.1918173

The pipeline turns heterogeneous, multi-source vehicle images into 3D Gaussian Splatting
reconstructions through three stages:

1. **Preprocessing** — background removal (rembg) + adaptive histogram equalization (CLAHE)
   to isolate the vehicle and normalize illumination.
2. **Orientation classification** — an EfficientNet-B0 model sorts each image into one of eight
   directional views (front, front-left, left, rear-left, rear, rear-right, right, front-right).
3. **Sparse reconstruction** — hierarchical localization (HLOC) with SuperPoint + SuperGlue and a
   neighbor-based image-pairing strategy, followed by COLMAP reconstruction.

## Repository contents

| File | Description |
|------|-------------|
| `vehicle_reconstruction_pipeline.ipynb` | End-to-end batch pipeline (Google Colab / Drive). Preprocessing → classification → HLOC + COLMAP → per-vehicle `.zip` export. |
| `organize_compcars.py` | Reorganizes the raw CompCars dataset into a `car_type/make/model/year` folder tree used as input to the pipeline. |
| `model_best.pth` | Trained EfficientNet-B0 orientation classifier weights. *(add this file to the repo)* |
| `requirements.txt` | Python dependencies. |

## Quick start

### 1. Prepare the dataset
Download CompCars (non-commercial research use only) and reorganize it:

```bash
pip install scipy
# edit the PATH SETTINGS at the top of organize_compcars.py first
python organize_compcars.py
```

This produces:

```
CompCars_structured/
└── sedan/
    └── Audi/
        └── A3/
            └── 2013/*.jpg
```

### 2. Run the pipeline
Open `vehicle_reconstruction_pipeline.ipynb` in Google Colab (GPU runtime recommended):

1. Mount Google Drive and place the organized dataset + `model_best.pth` where the **SETTINGS**
   cell points.
2. Run the installation cells (HLOC, COLMAP, and the core libraries), then restart the runtime
   when prompted.
3. Run the pipeline cells. Each vehicle is exported as `{make}_{model}_{year}.zip` containing the
   reconstruction.

## Dataset

The resulting 3D Gaussian Splatting models (114 vehicle classes) are available on Hugging Face:

**https://huggingface.co/datasets/muzafferardauslu/vehicle-3dgs**

They are derived from CompCars and released for **non-commercial research** with the permission of
the CompCars authors.

## Citation

If you use this code or the dataset, please cite both papers:

```bibtex
@article{uslu2026multistage,
  title   = {A Multi-Stage Pipeline for 3D Reconstruction of Vehicles from Heterogeneous Multi-View Images},
  author  = {Uslu, Muzaffer Arda and Kaplan Berkaya, Selcan},
  journal = {Erciyes {\"U}niversitesi Fen Bilimleri Enstit{\"u}s{\"u} Fen Bilimleri Dergisi},
  volume  = {42},
  number  = {2},
  year    = {2026},
  doi     = {10.65520/erciyesfen.1918173},
  url     = {https://doi.org/10.65520/erciyesfen.1918173}
}

@inproceedings{yang2015compcars,
  title     = {A Large-Scale Car Dataset for Fine-Grained Categorization and Verification},
  author    = {Yang, Linjie and Luo, Ping and Loy, Chen Change and Tang, Xiaoou},
  booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2015}
}
```

## Acknowledgements

This work was supported by the Eskişehir Technical University Scientific Research Projects
Commission under grant no. 25LÖT108.

Built on [Hierarchical-Localization (HLOC)](https://github.com/cvg/Hierarchical-Localization),
[COLMAP](https://colmap.github.io/), and [rembg](https://github.com/danielgatis/rembg).

## License

Code in this repository is released under the MIT License (see `LICENSE`).
The **dataset** and the CompCars source data are governed by their own non-commercial terms —
see the Hugging Face dataset card.
