FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY streamlit_mask_detect.py .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_mask_detect.py", "--server.port=8501", "--server.address=0.0.0.0"]

