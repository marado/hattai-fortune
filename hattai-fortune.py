import sys

sys.path.append('./feedparser')

import feedparser


feed = feedparser.parse('http://feeds.feedburner.com/publicoRSS')
print "Got " + str(len(feed.entries)) + " entries in the feed"

for post in feed.entries:
    print post.title
    print post.link
    print

