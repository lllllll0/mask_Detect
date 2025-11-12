# 口罩检测工具：基于YOLO的智能检测应用
基于YOLO模型开发的口罩检测工具，支持图片/视频上传检测，部署后快速使用。
(该项目目的是为学习、研究,模型训练以及检测结果若有瑕疵和问题,请多多包容)


## 🌟 核心功能
- **可视化界面**：通过Streamlit提供直观的Web交互界面，支持图片/视频上传检测；

- **高效推理**：基于ONNX Runtime优化模型推理速度；

- **开放API**：FastAPI提供检测接口，支持二次开发与集成。


## 🚀 快速启动（Docker Compose）

### 前提条件
- 安装 Python 3.9+


### 部署步骤
1. **克隆仓库**
   ```bash
   git clone https://github.com/lllllll0/mask_Detect.git
   cd mask_Detect
   
2. **安装依赖**
    ```bash
   pip install -r requirements.txt

3. **启动服务**
   注意:先启动后端,再运行前端
   ```bash
   uvicorn code.deployment_code.fastapi_server:app --host 0.0.0.0 --port 8000
   streamlit run code.deployment_code.streamlit_mask_detect.py

4. **访问服务**
   
    前端界面（上传检测）：http://localhost:8501
   
    后端 API 文档（调试接口）：http://localhost:8000/docs

5. **停止服务**
   在同一个终端窗口中,按下
    ```txt
    Ctrl + C

## 🛠️技术栈

**后端**：FastAPI + ONNX Runtime + YOLO

**前端**：Streamlit

**模型**：YOLO 系列（默认提供yolo11n.pt预训练模型，可替换为自定义模型）


## ❗ 常见问题
### 端口占用：
若 8000 端口被占用，找出被占用端口然后关闭或者修改启动命令,例如(--port 8001)，再重新启动。

### 模型加载失败：
确认code/目录下存在best.onnx和yolo11n.pt，另外,该项目**有使用相对路径**,请注意不要随意移动文件位置
若缺失，参考 “模型替换” 说明。

### 检测无结果：
检查图片格式或视频编码（仅支持 MP4）以及文件大小(需要小于200MB)，确保文件无损坏。


## 📄 模型替换（自定义训练）

若需替换为自己训练的模型，按以下步骤操作：

1. 将新训练的best.pt放入code/目录；

2. 执行模型转换脚本生成best.onnx并替换原来的onnx模型（或者找到该文件直接运行）:
   ```bash
   python code/deployment_code/export_onnx.py
   
3. 重启服务
    

## 📢 素材声明

数据集过大,并未上传,在results目录中有给出一些该模型检测的示例以及训练日志
本项目中使用的人脸相关素材（包括示例图片、测试数据集等）来源于 GitHub 开源项目：  
[virus-mask-dataset]（链接：https://github.com/hikariming/virus-mask-dataset  ）

**使用说明**：  
1. 上述人脸素材仅用于本项目的 **学习、研究及功能测试**，未进行任何商业用途,原数据集采用  MIT License 开源；  
2. 素材的版权归原项目作者所有，如需将其用于其他场景，请遵守原项目的许可证；  
3. 本项目仅对素材进行了必要的标注扩展，未修改其核心内容。







