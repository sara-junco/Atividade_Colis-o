from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="data.yaml",
    epochs=50,
    imgsz=640,
)


from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

results = model("teste.jpg", show=True)