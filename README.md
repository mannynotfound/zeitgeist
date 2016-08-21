# zeitgeist

Utility library for scraping real time event data without the use of official APIs.

# usage

```bash
./src/py/terminator.py -t [search term]
```

eg:

```bash
./src/py/terminator.py -t python
```

## Dependencies 

* [python3](http://docs.python.org/3/)
* [requests](http://docs.python-requests.org)
* [lxml](http://lxml.de/index.html)
* [cssselect](https://pythonhosted.org/cssselect/)

note. using lmxl directly instead of BeautifulSoup as BS was too slow.
