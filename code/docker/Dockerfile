# 基础镜像：Python 3.11 轻量版（减少镜像体积）
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# -------------- 关键优化1：调整镜像源配置顺序（先换源再更新）--------------
# 配置阿里云 Debian 13（trixie）镜像源（解决官方源访问慢问题）
RUN echo "" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ trixie main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ trixie main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security/ trixie-security main" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian-security/ trixie-security main" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ trixie-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ trixie-updates main non-free contrib" >> /etc/apt/sources.list

# -------------- 关键优化2：合并系统依赖安装（减少分层，缩小镜像体积）--------------
# 安装系统依赖：binutils（含execstack）+ 图像处理相关库 + 清理缓存
RUN apt-get update && apt-get install -y \
    binutils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*  # 清理apt缓存，减少镜像体积

# -------------- 关键优化3：统一pip镜像源（避免重复配置）--------------
# 配置pip阿里云镜像源（全局生效，加速Python依赖安装）
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.trusted-host mirrors.aliyun.com

# -------------- 应用部署步骤 --------------
# 1. 复制依赖清单（优先复制requirements.txt，利用Docker缓存机制）
COPY code/docker/requirements.txt .

# 2. 安装Python依赖（升级pip + 无缓存安装 + 兼容国内网络）
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 3. 复制核心代码和模型文件（代码变更频率高，放在后面减少缓存失效）
COPY code/deployment_code/fastapi_server.py /app/fastapi_server.py
COPY code/best.onnx /app/best.onnx

# -------------- 关键修复：ONNX Runtime动态库权限配置 --------------
# 为所有ONNX Runtime的.so文件设置可执行栈权限（解决"无法启用可执行栈"错误）
# 适配Python 3.11的site-packages路径，使用find确保遍历所有子目录
RUN find /usr/local/lib/python3.11/site-packages/onnxruntime -name "*.so" -type f -exec execstack -s {} \;

# 暴露应用端口（与FastAPI启动端口一致）
EXPOSE 8000

# 启动命令（使用exec格式，确保容器信号转发正常）
CMD ["uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
