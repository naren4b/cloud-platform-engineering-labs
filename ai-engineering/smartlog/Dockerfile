FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOME=/tmp
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py analyzer.py parsers.py guidance.py ./
COPY samples ./samples
COPY tests ./tests
COPY .streamlit ./.streamlit
EXPOSE 8501
USER 65532:65532
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
