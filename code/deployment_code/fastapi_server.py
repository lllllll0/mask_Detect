import shutil
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException,Form
from fastapi.responses import FileResponse #用于返回检测后的结果
import cv2 as cv
import numpy as np
import os
import uuid
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from ultralytics import YOLO

#创建实例
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法
    allow_headers=["*"]  # 允许所有请求头
)

model=YOLO('../best.onnx', task="detect")

output_dir="detect_results/"
os.makedirs(output_dir,exist_ok=True)
#定义路由
@app.post("/detect_image")
async def detect_image(file:UploadFile=File(...),
                       conf:float=Form(0.3)):
    img_bytes=await file.read()
    img=cv.imdecode(np.frombuffer(img_bytes,np.uint8),cv.IMREAD_COLOR)

    results=model.predict(img,device='cpu',conf=conf)
    result_img=results[0].plot()

    result_filename=f"{uuid.uuid4()}_detected.jpg"
    result_path=os.path.join(output_dir,result_filename)
    cv.imwrite(result_path,result_img)
    #返回结果图片,用户可下载或预览

    return FileResponse(result_path,filename=result_filename)

def process_video(video_path:str,result_path:str, conf: float = 0.3):
    cap=cv.VideoCapture(video_path)
    width=int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height=int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps=int(cap.get(cv.CAP_PROP_FPS))
    if fps<=0:
        fps=10

    fourcc=cv.VideoWriter_fourcc(*'mp4v')
    out=cv.VideoWriter(result_path,fourcc,min(fps,15),(width,height))

    while(True):
        ret,frame=cap.read()
        if ret:
            results=model.predict(frame,device='cpu',conf=conf)
            res=results[0].plot()
            out.write(res)
        else:
            break

    cap.release()
    out.release()
    os.remove(video_path)


max_size=200*1024*1024
@app.post("/detect_video")
async def detect_video(bt:BackgroundTasks,file:UploadFile=File(...,
                            description="上传MP4格式视频,文件超过200MB会被拒绝"),conf:float=Form(0.3)):
    try:
        temp_path=os.path.join(output_dir,f"{uuid.uuid4()}.mp4")
        with open(temp_path,"wb") as f:
            shutil.copyfileobj(file.file,f)
        await file.close()
        file_size=os.path.getsize(temp_path)
        if file_size>max_size:
            raise HTTPException(
            status_code=413,
            detail=f"文件过大！最大支持200MB，当前文件大小：{file_size/(1024*1024):.2f}MB"
        )

        result_path=os.path.join(output_dir,f"{uuid.uuid4()}_detected.mp4")

        bt.add_task(process_video,temp_path,result_path,conf=conf)

        return {"status":"processing",
                "message":"视频检测中(cpu约需1-5分钟)",
                "result_query":f"/get_video?path={result_path}"}
    except Exception as e:
        return JSONResponse(status_code=500,
                        content={'status':"error","message":str(e)})

@app.get("/get_video")
async def get_video(path:str):
    if os.path.exists(path) and os.path.getsize(path)>0:
        return FileResponse(path,media_type="video/mp4",filename='detected_video.mp4')
    else:
        return {"status":"waiting",
                "message":"请1分钟后再试"}


