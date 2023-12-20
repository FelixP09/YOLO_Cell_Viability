# YOLO Detection model for Cell Viability

## Introduction
Detection models are able both to find objects coordinates on images and classifiate them. Unlike classification models, detection models are able to predict severale objects with different classes on the same image, making it a powerful tool for cellular images and especialy for cell viability analysis.

## Dataset
The Dataset is composed of 480 images (X10) of U2OS cell line treated with diffenrent confidential compounds. These are hight resolution grayscale images (2048,2048,1).
All images were acquired in three channels :
  - Transmitted light : the model  input
  - FITC : a DIOC staining used for cell localization (x/y coordinates calculation) for the labelling
  - DAPI : a DAPI stainning used for cell classification (Alive/Dead) for the labelling

Input images were normalized by quantiles (0.0005,0.9995) and saved in png format. The dataset were splitted in train and val parts (0.8/0.2).

## Model trainning
We trainned a YOLOv8n dection model, developped by Ultralytics package (https://docs.ultralytics.com/). The model is trainned from a pre-trained model to which new classes will be added.
YOLO trainning needs a yaml file containing the dataset pathway and the new classes IDs.
Model trainning is performed with a maximum of 300 epoch and two losses calculation for localization (box_loss) and classifiction (cls_loss).
At the end of the trainning, plots are automaticaly generated :
  - the confusion matrix
  - the F1-score in function of confidence vlaue (the probability that a box contains an object)
  - the different losses / metrics along epochs
