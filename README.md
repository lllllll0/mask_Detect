# 口罩检测工具：基于YOLO的智能检测应用
基于YOLO模型开发的口罩检测工具，支持图片/视频上传检测，容器化一键部署,快速使用。


## 🌟 核心功能
- **可视化界面**：通过Streamlit提供直观的Web交互界面，支持图片/视频上传检测；

- **高效推理**：基于ONNX Runtime优化模型推理速度；

- **容器化部署**：Docker Compose一键启动，无需配置复杂环境；

- **开放API**：FastAPI提供检测接口，支持二次开发与集成。


## 🚀 快速启动（Docker Compose）

### 前提条件
- 安装 [Docker](https://www.docker.com/get-docker) 和 [Docker Compose](https://docs.docker.com/compose/install/)（Windows/Mac可直接安装Docker Desktop，内置Compose）；
- 验证安装：在终端执行 `docker --version` 和 `docker compose version`（或 `docker-compose --version`），显示版本号即成功。


### 部署步骤
1. **克隆仓库**
   ```bash
   git clone https://github.com/[你的GitHub用户名]/[你的仓库名].git
   cd [你的仓库名]
   
2. **一键启动所有服务**
    ```bash
   docker-compose up -d

3. **访问服务**
   
    前端界面（上传检测）：http://localhost:8501
   
    后端 API 文档（调试接口）：http://localhost:8000/docs

4. **停止服务**
    ```bash
    docker-compose down

## 🛠️技术栈

**后端**：FastAPI + ONNX Runtime + YOLO

**前端**：Streamlit

**容器化**：Docker + Docker Compose

**模型**：YOLO 系列（默认提供yolo11n.pt预训练模型，可替换为自定义模型）


## ❗ 常见问题
### 端口占用：
若 8000/8501 端口被占用，修改docker-compose.yml中ports映射（如8001:8000、8502:8501），再重新启动。

### 模型加载失败：
确认code/目录下存在best.onnx和yolo11n.pt，若缺失，参考 “模型替换” 说明。

### 检测无结果：
检查图片格式或视频编码（仅支持 MP4）以及文件大小(需要小于200MB)，确保文件无损坏。


## 📄 模型替换（自定义训练）

若需替换为自己训练的模型，按以下步骤操作：

1. 将新训练的best.pt放入code/目录；

2. 执行模型转换脚本生成best.onnx（或者找到该文件直接运行）:
   ```bash
   python code/deployment_code/export_onnx.py
   
3. 重启服务
    ```bash
    python code/deployment_code/export_onnx.py

## 📢 素材声明
本项目中使用的人脸相关素材（包括示例图片、测试数据集等）来源于 GitHub 开源项目：  
[项目名称]（链接：https://github.com/原作者用户名/项目仓库名）

**使用说明**：  
1. 上述人脸素材仅用于本项目的 **学习、研究及功能测试**，未进行任何商业用途；  
2. 素材的版权归原项目作者所有，如需将其用于其他场景，请遵守原项目的许可证（如 MIT、GPL 等）并联系原作者授权；  
3. 本项目仅对素材进行了必要的格式转换或裁剪，未修改其核心内容。







