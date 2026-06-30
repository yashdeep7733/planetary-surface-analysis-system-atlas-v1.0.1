from ultralytics import YOLO

model = YOLO("yolo11n.pt") # Loading the YOLO model from the specified path. This model will be used for crater detection in the images.

# Only run this file directly if you wish to train the model. If you want to use the model for inference, run app.py instead.

if __name__ == "__main__":
    model.train(
        data="dataset/craters/data.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        project="runs",
        name="crater_detector"
    )