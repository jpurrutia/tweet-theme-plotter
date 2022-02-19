FROM python:3.9.1

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /mydata

COPY tweet_scraper.py tweet_scraper.py
COPY my_stop_words.py ./
COPY config.py ./

EXPOSE 8050

VOLUME ["/mydata"]

ENTRYPOINT ["python", "tweet_scraper.py"]

CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8050", "app:server"]
