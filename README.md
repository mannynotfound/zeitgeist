# zeitgeist

Utility library for scraping real time event data without the use of official APIs.

# credits

The search code is from [TwitterWebsiteSearch](https://github.com/dtuit/TwitterWebsiteSearch)

# data format
Tweets extracted, are formatted similarly to the official API, detailed [here](https://dev.twitter.com/overview/api/tweets)

each tweet is a python dict with the following structure.
```
{
	'created_at' : UTC-datetime format '%Y-%m-%d %H:%M:%S' ,
	'id_str' : "",
	'text' : "",
	'entities': {
		'hashtags': [],
		'symbols':[],
		'user_mentions':[],
		'urls':[],
		'media'[] optional
		},
	'user' : {
		'id_str' : "",
		'name' : "",
		'screen_name': "",
		'profile_image_url': "",
		'verified': bool
		},
	'retweet_count' : 0,
	'favorite_count' : 0,
	'is_quote_status' : False,
	'in_reply_to_user_id': None,
	'in_reply_to_screen_name' : None,
	'contains_photo': False,
	'contains_video': False
}
```
# usage

## terminator
scrapes twitter search for a certain search term

```bash
./src/py/terminator.py -t [search term] -l [optional limit]
```

eg:

```bash
./src/py/terminator.py -t python
```

## sentiment analyzer

analyzes the positive/negative language of a dump of tweets

```bash
./src/py/sentiment/analyze.py -f [filepath] -l [optional limit]
```

eg:

```bash
./src/py/sentiment/analyze.py -f ~/Sites/zeitgeist/src/py/dump/my_tweets.json
```

## Dependencies 

* [python3](http://docs.python.org/3/)
* [requests](http://docs.python-requests.org)
* [lxml](http://lxml.de/index.html)
* [cssselect](https://pythonhosted.org/cssselect/)

note. using lmxl directly instead of BeautifulSoup as BS was too slow.
