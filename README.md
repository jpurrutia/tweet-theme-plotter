# Tweet Theme Plotter

## Why I made this
I've been tweeting a lot about technology as a way to keep an online portfolio and build a network of engineers.

I'm producing some cool work from that content and in wanting to add to my resume, I wanted to see exactly what I've been working on.

So I built a scraper to look at my tweets, clean them, and get a count of the times they appear in my tweets. This might make me refine my writing so that I can add more concise tweets.

The goal is to build this and allow anyone to be able to use it and see what they mainly tweet about.

I'm a newbie to docker so any contribution is welcome!


## How to use

### Get Twitter API Credentials and Username

[Here](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)

## Change your username in the app.py file

`line 110`

Get credentials from:

```
CONSUMER_KEY=''
CONSUMER_SECRET=''
ACCESS_TOKEN=''
ACCESS_SECRET=''
```
Create a `config.py ` file and add those credentials to that file.
It will look just like the code block above and you are already importing into the  `tweet_scraper.py` file.

Make sure you DO NOT share those credentials with anyone.

[Install Docker](https://docs.docker.com/get-docker/)

### Build the Container
```
docker-compose build
```

### Run the Container
```
docker-compose up
```

You should see a populated output.csv locally. This is possible due to a Bind mounted volume at runtime. It maps a path in your host file system to a path in the Docker container's filesystem.

If everything is running correctly, go to your browser and type in:
`http://localhost:5000/`

You should see your most tweeted topics!
