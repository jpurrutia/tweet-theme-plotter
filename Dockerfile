FROM python:3.9.1

COPY . ./

WORKDIR ./

RUN pip install -r ./requirements.txt

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
