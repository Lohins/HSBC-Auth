# 加注释
FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app

EXPOSE 5050

ENV FLASK_APP app 

# Run app.py when the container launches
CMD ["python", "app.py"]