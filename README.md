# YOLO Detection model for Cell Viability

## Introduction
Detection models are able both to find objects coordinates on images and classify them. Unlike classification models, detection models are able to predict several objects with different classes on the same image, making it a powerful tool for cellular images and especially for cell viability analysis.

## Dataset
The Dataset is composed of 480 images (X10) of U2OS cell line treated with different confidential compounds. These are high resolution grayscale images (2048,2048,1).
All images were acquired in three channels :
  - Transmitted light : the model  input
  - FITC : a DIOC staining used for cell localization (x/y coordinates calculation) for the labeling
  - DAPI : a DAPI staining used for cell classification (Alive/Dead) for the labeling

Input images were normalized by quantiles (0.0005,0.9995) and saved in png format. The dataset were divided in training and validation parts (0.8/0.2).

Download link : https://www.kaggle.com/datasets/felixp09/cell-viability-detection/data

## Model training
We trained a YOLOv8n detection model, developed by Ultralytics package (https://docs.ultralytics.com/). The model is trained from a pre-trained model, to which new classes will be added.
YOLO training needs a yaml file containing the dataset pathway and the new classes IDs.
Model training is performed with a maximum of 300 epochs and two losses calculation for localization (box_loss) and classification (cls_loss).
At the end of the training, plots are automatically generated :
  - the confusion matrix
  - the F1-score in function of confidence value (the probability that a box contains an object)
  - the different losses / metrics along epochs

![res_plot](plots/results.png)
![f1_plot](plots/F1_curve.png)
![val_plot](plots/val_bath0_pred.jpg)
