import io
import streamlit as st
import requests #用于发送http请求,调用后端接口
from PIL import Image
import tempfile
import os
import time #用于视频轮询
from urllib.parse import urljoin  #拼接接口地址


# ---------------------- 配置项（与后端严格匹配，需根据实际部署调整） ----------------------
#后端服务地址,本地测试用localhost，部署后需要替换
BACKEND_URL="http://backend:8000"  #本地"http://localhost:8000"
image_types=['png','jpg','jpeg']
video_types=['mp4']
max_limit_mb=200
#视频检测轮询间隔,最大等待时间
video_per_time=10
max_wait_time=20*60

# ---------------------- 页面基础配置（设置页面标题、图标、布局） ----------------------
st.set_page_config(
    page_title='口罩检测系统',
    page_icon='😷',
    layout='wide'#宽屏布局,适用左右分栏
)
st.title("😷 口罩检测系统")
st.markdown("支持图片/MP4视频上传，自动检测人脸口罩佩戴情况（CPU处理视频约1-5分钟）")
st.markdown(f"⚠️ 视频限制：仅支持 MP4 格式，最大 {max_limit_mb}MB")

col1,col2=st.columns(2)

# ---------------------- 工具函数定义（封装通用逻辑，便于复用和维护） ----------------------
def check_filesize(file,max_size):
    file_size=file.size/1024/1024
    if file_size>max_size:
        st.error(f"文件过大!最大支持{max_size}MB,当前文件{file_size:.2f}MB")
        return False
    return True

def upload_to_backend(endpoint: str, file, mime_type: str,conf:float):
    try:
        response = requests.post(
            url=urljoin(BACKEND_URL, endpoint),
            files={'file': (file.name, file.getvalue(), mime_type)},
            data={'conf':str(conf)},
            timeout=60
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {str(e)}")
        return None


def poll_video(result_query):#轮询后端视频查询接口
    try:
        response=requests.get(
            url=urljoin(BACKEND_URL,result_query),
            timeout=30
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        st.warning(f'查询失败,{video_per_time}秒后重试:{str(e)}')
        return None

# ---------------------- 主页面布局与交互逻辑 ----------------------
#左侧分栏
with col1:
    st.subheader("上传文件")
    upload_type=st.radio("选择文件类型",["图片","视频"])
    upload_file=None#初始化上传对象

    # 根据选择的类型，显示对应的文件上传组件
    if upload_type=='图片':
        upload_file=st.file_uploader(
            label="上传图片(png,jpg,jpeg)",
            type=image_types,
            accept_multiple_files=False # 不允许批量上传
        )
    else:
        upload_file=st.file_uploader(
            label=f"上传视频(仅 MP4,最大{max_limit_mb}MB)",
            type=video_types,
            accept_multiple_files=False
        )
    if upload_type in ['图片', '视频']:
        conf_threshold = st.slider(
            "置信度阈值 (Confidence Threshold)",
            min_value=0.0,
            max_value=1.0,
            value=0.3,  # 默认值，与你后端一致
            step=0.02,
            help="低于此置信度的目标将不会被显示"
        )

    detect_btn=st.button(
        label='🔍 开始检测',
        type="primary",# 高亮按钮样式
        #是否禁用
        disabled=not (upload_file and check_filesize(upload_file,max_limit_mb))
    )

with col2:
    st.subheader("检测结果")
    res_placeholder=st.empty()
    download_placeholder=st.empty()#占位符,动态更新显示

# ---------------------- 检测核心逻辑（点击检测按钮后执行） ----------------------

if detect_btn and upload_type=='图片' and upload_file:
    with st.spinner("图片加载中,请稍候..."):#显示动画
        img_data=upload_to_backend("/detect_image",upload_file,upload_file.type,conf_threshold)
        if img_data:
            # 将二进制流转为PIL图片对象（用于Streamlit展示）
            detect_image=Image.open(io.BytesIO(img_data.content))
            res_placeholder.image(detect_image,caption="口罩检测结果", use_container_width=True)

            download_placeholder.download_button(
                label='💾 下载检测结果',
                data=img_data.content,
                file_name=f'detected_{upload_file.name}',
                mime='image/jpeg'
            )

if detect_btn and upload_type=='视频' and upload_file:
    with st.spinner('提交视频中...'):
        submit_res=upload_to_backend("/detect_video",upload_file,"video/mp4",conf_threshold).json()
        if not submit_res:
            st.error("视频提交失败,请重试")
        else:
            st.info(f'{submit_res["message"]}')
            result_query=submit_res['result_query']
            video_ready=False#标记检测状态
            #轮询查询直到完成或超时
            with st.spinner("视频检测中,将持续查询结果(请勿关闭页面)..."):
                start_time=time.time()
                while time.time()-start_time < max_wait_time:
                    response=poll_video(result_query)
                    if response:
                        # 检查响应类型：若为视频流（Content-Type含video/mp4），说明处理完成
                        if "video/mp4" in response.headers.get('Content-Type',""):
                            temp_video=tempfile.NamedTemporaryFile(delete=False,suffix='.mp4')
                            temp_video.write(response.content)
                            temp_video.close()
                            #res_placeholder.video(data=temp_video.name,
                            #                 format='video/mp4')
                            res_placeholder.success("✅ 视频检测完成！请下载查看结果（部分浏览器不支持在线播放）")

                            download_placeholder.download_button(
                                label='💾 下载检测结果视频',
                                data=response.content,
                                file_name=f'detected_{upload_file.name}',
                                mime='video/mp4'
                            )
                            os.unlink(temp_video.name)
                            video_ready=True
                            break
                        else:
                            status_info=response.json()
                            st.warning(f'处理中:{status_info["message"]}')
                    time.sleep(video_per_time)

                if not video_ready:
                    res_placeholder.error(f"视频处理超时(已等待20分钟),请稍候重新上传检测")

# ---------------------- 页面底部说明文字 ----------------------
st.markdown("----")
st.markdown("###操作说明")
st.markdown(f"1. 图片处理：上传后即时返回结果，支持下载标注后的图片")
st.markdown(f"2. 视频处理：CPU环境下约需 1-5 分钟，期间请勿关闭页面，完成后可下载视频")
st.markdown(f"3. 常见问题：")
st.markdown(f"   - 检测失败请检查：后端服务是否启动、文件格式/大小是否合规、网络连接正常")
st.markdown(f"   - 视频查询超时可重新上传（建议控制视频时长在1分钟内，提升处理速度）")




