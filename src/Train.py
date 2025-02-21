from ultralytics import YOLO

### This is the ultralytics pre-trained with common object classes (person, phone, car, dog ...etc)
model = YOLO('yolov8n.pt')

### Parameters
EPOCHS = 300 ### maximal epochs number for trainning
PATIENCE = 15 ### Number of epochs waited before stop the trainning when losses stop to decrease
IMGSZ = 2048 ### Input Images size for rescaling
BS = 1 ### Batch size
MAX_DET = 3000 ### Maximal number of object by image for the detection
WORKERS = 24 ### CPU count
DATA = "dataset.yaml" ### .yalm file containning images pathway, labels (.txt) pathway and classes IDs

### Model Fine-Tuning

if __name__ == '__main__': 
    results = model.train(data=DATA, epochs=EPOCHS, patience=PATIENCE, imgsz=IMGSZ, batch=BS, max_det=MAX_DET, workers=WORKERS )

