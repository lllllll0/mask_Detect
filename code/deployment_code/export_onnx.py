from ultralytics import YOLO
model=YOLO('../best.pt')
model.export(
    format='onnx',
    simplify=True,  # 简化网络结构（删除冗余节点）
    opset=16,
    dynamic=True,
    device='cpu'    # 确保在CPU环境导出
)



