import cv2
from ultralytics import YOLO
import time
#检测视频的帧率/单帧均耗时
model=YOLO('../best.onnx',task='detect')
cap=cv2.VideoCapture(0)
total=0
cnt=0
while(True):
    ret,frame=cap.read()
    frame=cv2.flip(frame,1) #水平翻转摄像头
    if ret:
        sta_=time.time()
        res=model.predict(frame)
        if cnt>5:
            total+=(time.time()-sta_)
        cnt+=1
        for r in res:
            for box in r.boxes:
                x1,y1,x2,y2=map(int,box.xyxy[0])
                cls=int(box.cls[0])
                conf=float(box.conf[0])
                cls_name=model.names[cls]

                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                text=f'{cls_name}{conf:.2f}'
                cv2.putText(frame,text,(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)


        cv2.imshow('frame',frame)
        if cv2.waitKey(10)&0xFF==ord('q'):
            #当用户在图像显示窗口中按下键盘上的q键时，退出当前的循环
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
avg=total/(cnt-5)*1000#s->ms 是*1000
fps=1000/avg
print(f"平均FPS：{fps:.2f} | 单帧平均耗时：{avg:.2f} ms")
