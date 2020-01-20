FROM python

LABEL Name=flask_app Version=1.0.0 Author=AlexanderCapitonenko

WORKDIR /flask_app
ADD app .
ADD requirements.txt .

RUN python3 -m pip install -r requirements.txt
CMD ["python3", "app.py"]