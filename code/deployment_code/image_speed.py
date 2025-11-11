from ultralytics import YOLO
import time
#检测一张图片的平均耗时
model=YOLO('../best.onnx')
total_=0

#图片路径(根据本地路径直接复制进来即可)
img_path=""
#预热推理
for _ in range(2):
    model(img_path)

for _ in range(10):
    sta=time.time()
    res=model(img_path)
    total_+=(time.time()-sta)

avg_=total_/10
print(f'单张图片平均耗时:{avg_:.4f}')

