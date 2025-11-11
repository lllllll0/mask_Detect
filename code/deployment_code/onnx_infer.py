import onnxruntime as ort
import cv2 as cv
import numpy as np


#配置cpu的多线程
options=ort.SessionOptions()
options.intra_op_num_threads=3 #单算子多线程
options.graph_optimization_level=ort.GraphOptimizationLevel.ORT_ENABLE_ALL #开启所有优化
#加载模型
session=ort.InferenceSession('../best.onnx',
                            sess_options=options,
                             providers=['CPUExecutionProvider']
                             )
#预处理
def preprocess(img,size=640):
    img=cv.resize(img,(size,size))
    img=img[:,:,::-1].transpose(2,0,1)#转格式  BGR→RGB，HWC→CHW
    img=np.ascontiguousarray(img,dtype=np.float32)/255.0
    #将数组转换为连续的内存布局，
    # 确保后续操作（如数值计算、跨框架传输）的效率和兼容性。
    #归一化操作
    img=np.expand_dims(img,axis=0)#加维度
    return img

#推理函数
def detect(img_path):
    img=cv.imread(img_path)
    in_img=preprocess(img)
    #名称
    in_name=session.get_inputs()[0].name
    outputs=session.run(None,{in_name:in_img})
    return outputs,img






