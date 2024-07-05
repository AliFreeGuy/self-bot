# Dockerfile
# استفاده از یک تصویر پایه از پایتون
FROM python:3.9-slim

# کپی کردن فایل پایتون به داخل کانتینر
COPY self.py /self-source/self.py

# تنظیم دایرکتوری کاری
WORKDIR /self-source

RUN apt-get update && apt-get install -y procps
RUN pip install pyrogram
RUN pip install redis
RUN pip install python-dotenv
RUN pip install jdatetime
RUN pip install pytz

# تنظیم ENTRYPOINT برای اجرای اسکریپت شل
ENTRYPOINT ["python", "self.py"]
