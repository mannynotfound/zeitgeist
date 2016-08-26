import firebase
import argparse

def check_count(data):
    print(len(data))


def show_newest(data, show):
    print(data[0:show])

def show_oldest(data, show):
    start = len(data) - show
    end = len(data)
    print(data[start:end])


if __name__ == '__main__':
    # parse cli arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--term', help = 'term to test for')
    ap.add_argument('-c', '--count', help = 'count amount of tweets', action="store_true")
    ap.add_argument('-n', '--newest', help = 'get newest posts', action="store_true")
    ap.add_argument('-o', '--oldest', help = 'get oldest posts', action="store_true")
    ap.add_argument('-s', '--show', help = 'amount of tweets to show', type=int, default=1)
    args = vars(ap.parse_args())

    if args['term'] is None:
        print('please provide a term to look up')
        sys.exit(1)

    fb = firebase.create_firebase()
    db_tweets = fb.database().child('tweets').child(args['term']).get().val()

    if db_tweets is None:
        print('no data found here')
        sys.exit(0)

    if args['count']:
        check_count(db_tweets)

    if args['newest']:
        show_newest(db_tweets, args['show'])

    if args['oldest']:
        show_oldest(db_tweets, args['show'])

