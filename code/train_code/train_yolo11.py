from ultralytics import YOLO

model=YOLO('../yolo11n.pt')
results=model.train(data='../../dataset/data.yaml',
                    epochs=30,
                    batch=4,
                    device='cpu',
                    pretrained=True,
                    optimizer='Adam',
                    lr0=0.001,
                    augment=True)