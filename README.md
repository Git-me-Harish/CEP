# WBC Type Prediction and Blood Cell Detection

This project aims to develop a high-performance machine learning model that can recognize White Blood Cell (WBC) types and detect blood cell components (WBC, RBC, and Platelets) from microscopic images.

## Table of Contents

- [Introduction](#introduction)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Models](#models)
  - [WBC Classification](#wbc-classification)
  - [Blood Cell Detection](#blood-cell-detection)
- [Results](#results)
- [Discussion](#discussion)
- [Contributing](#contributing)

## Introduction

Accurate determination of WBC types and blood cell counts is crucial in clinical medical diagnostics. This project employs various Convolutional Neural Network (CNN) models, including the Inception model, ResNet50, a custom CNN implementation, and YOLOv5 for object detection. The goal is to automate the process of blood cell counting and WBC classification, potentially helping healthcare professionals make better prognoses and life-saving decisions.

## Dataset

The project utilizes the BCCD (Blood Cell Count and Detection) Dataset, which is a small-scale dataset for blood cells detection licensed under MIT. The dataset consists of two sub-datasets:

1. `dataset2-master`: Contains 12,500 augmented images of blood cells for WBC classification, along with a CSV file containing the corresponding image number and type.
2. `dataset-master`: Contains approximately 410 pre-augmentation images of blood cells and their bounding box annotations in XML format.

## Installation

1. Clone the repository: `git clone https://github.com/shreyas1104/White-Blood-Cells-Image-Classification.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Download the dataset from `https://www.kaggle.com/datasets/paultimothymooney/blood-cells/discussion/63703` and extract it to the `data/` directory.

## Usage

1. For WBC classification, run: `wbc-classification.ipynb`
2. For blood cell detection, run: `YOLOv5_BCCD.ipynb`

## Models

### WBC Classification

Three CNN models were implemented for WBC classification:

1. **Inception Model**: With 571,460 trainable parameters, this model achieved an accuracy of 99.15% on the validation set.
2. **ResNet50**: This pre-trained model has 16,060,228 parameters and achieved an accuracy of 97.74% on the validation set.
3. **Custom CNN**: A custom CNN architecture with 142,980 parameters, achieving an accuracy of 98.34% on the validation set.

### Blood Cell Detection

The YOLOv5 model was used for detecting and classifying blood cell components (WBC, RBC, and Platelets). It achieved a mean Average Precision (mAP) of 92.86% on the test set.

## Results

The Inception model performed the best for WBC classification, with an accuracy of 99.15%. The custom CNN model, despite having fewer parameters, achieved a relatively high accuracy of 98.34%. For blood cell detection, the YOLOv5 model performed well, with a mAP of 92.86%.

## Discussion

The custom CNN model proved to be the most efficient, with fewer parameters and comparable accuracy to the Inception model. Increasing the training epochs could potentially improve its performance further. The YOLOv5 model effectively detected blood cell components, with WBCs having the highest detection accuracy (98.3%) and RBCs the lowest (88.3%), likely due to the dense and overlapping nature of RBCs in the dataset.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request
"# CEP" 
