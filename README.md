# zeitgeist

Utility library for scraping real time event data without the use of official APIs.


## data format

## tweets

Tweets extracted, are formatted similarly to the official API, detailed [here](https://dev.twitter.com/overview/api/tweets)

each tweet is a python dict with the following structure.

```
{
  "created_at": "UTC-datetime format "%Y-%m-%d %H:%M:%S",
  "id_str": "",
  "text": "",
  "entities": {
    "hashtags": [],
    "symbols": [],
    "user_mentions": [],
    "urls": [],
    "media": [] // optional
    },
  "user": {
    "id_str": "",
    "name": "",
    "screen_name": "",
    "profile_image_url": "",
    "verified": bool
    },
  "retweet_count": 0,
  "favorite_count": 0,
  "is_quote_status": False,
  "in_reply_to_user_id": None,
  "in_reply_to_screen_name": None,
  "contains_photo": False,
  "contains_video": False
}
```

## stories

Stories are retrieved using [feedparser](https://pypi.python.org/pypi/feedparser)

each story is a python dict with the following structure.

```
{
  "headline": "Some headline",
  "summary": "Summary may contain <html>",
  "link": "http://linktostory.com/story.html",
  "published": "some timestamp",
  "unix_timestamp": 131323131, 
  "media": [
    {
      "height": "619",
      "medium": "image",
      "url": "http://linktomedia.com/media.jpg",
      "width": "1100"
    }, // etc
  ]
}
```

## usage

### firebase config:

include a `creds.json` with your project info, eg

```js
{
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com"
}
```

and a `service_account.json` for use with authing to server

```js
{
  "type": "service_account",
  "project_id": "projectId",
  "private_key_id": "privateKey",
  "private_key": "BEGIN PRIVATE KEY---",
  "client_email": "clientEmail",
  "client_id": "clientId",
  "auth_uri": "authUri",
  "token_uri": "tokenUri",
  "auth_provider_x509_cert_url": "authProvider",
  "client_x509_cert_url": "clientCert"
}
```

## twitter\_search
scrapes twitter search for a certain search term

```bash
./twitter_search.py -t [search term(s)] -f [optional firebase flag] -s [optional silent flag]
```

eg:

```bash
./twitter_search.py -t python -f
```

you can also pass multiple, comma seprated terms like so

```bash
./twitter_search.py -t "python, javascript, ruby" -f
```

## stories

scrapes RSS feeds described in `models/feeds.json`

```bash
./stories.py -f [optional firebase flag]
```

eg:

```bash
./stories.py -f
```

## all\_trends

uses all the trend collection scripts, merges them & launches a `forever` `twitter_search` process for each topic

```bash
./scripts/all_trends.py -l [optional limit, defaults to 10] -f [optional firebase flag]
```

eg:

```bash
./scripts/all_trends.py -l 20 -f
```

## google\_trends

scrapes google trends API for trending topics & launches a `forever` `twitter_search` process for each topic

```bash
./scripts/google_trends.py -l [optional limit, defaults to 10] -f [optional firebase flag]
```

eg:

```bash
./scripts/google_trends.py -l 20 -f
```

## twitter\_trends

scrapes a twitter trends website for trending topics & launches a `forever` `twitter_search` process for each topic

```bash
./scripts/twitter_trends.py -l [optional limit, defaults to 10] -f [optional firebase flag]
```

eg:

```bash
./scripts/twitter_trends.py -l 20 -f
```

## sentiment analyzer

analyzes the positive/negative language of a dump of tweets

```bash
./analyze.py -f [filepath] -l [optional limit]
```

eg:

```bash
./analyze.py -f ~/Sites/zeitgeist/dump/my_tweets.json
```

## splitter

just a fun applescript to auto create split panes in iTerm to run `twitter_search` processes

```bash
term_names=[comma seperated list] ./scripts/splitter.scpt
```

eg:

```bash
term_names="google,apple,uber" ./scripts/splitter.scpt
```

## log

the `twitter_search` writes all of its messages with context term to `.master.log`,
this is useful when running aggregate scripts to monitor all traffic

eg

```bash
./scripts/all_trends.py -f -l 20
tail -f .master.log
```

## dependencies 

* [python3](http://docs.python.org/3/)
* [feedparser](https://pypi.python.org/pypi/feedparser)
* [forever](https://github.com/foreverjs/forever)
* [pyrebase](https://github.com/thisbejim/Pyrebase)
* [requests](http://docs.python-requests.org)
* [lxml](http://lxml.de/index.html)
* [cssselect](https://pythonhosted.org/cssselect/)

## credits

The search code is from [TwitterWebsiteSearch](https://github.com/dtuit/TwitterWebsiteSearch)

sentiment analysis code from [sentiment](https://github.com/pthrasher/sentiment)
