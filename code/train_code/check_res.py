from ultralytics import YOLO
import cv2 as cv
#模型训练后,检测训练结果,图片保存至根目录/results/detect_examples
model=YOLO('../best.pt')

for i in range(17):
    result=model("C:\\Users\LLL\Downloads\check\\che ("+str(i+1)+").jpg")
    result=result[0].plot()
    cv.imwrite('../../results/detect_examples/check_'+str(i+1)+'.png',result)
