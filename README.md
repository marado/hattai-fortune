hattai-fortune
==============

Hattai's Fortune: a script to be used by a bot, that gives news.

This script depends on feedparser, which should be installed on your system.

This script depends on python 3.2 or above.

## Script's behaviour

When run the script will:

1. Read the given (hardcoded) RSS feed:
   (at this moment, Google News' feed for in-Portuguese Portugal News)
2. Exclude the articles which contain any word from a given list of "bad words"
   (the match is case **insensitive**)
3. Exclude articles which have an empty title
4. Add new articles to the article list
5. Trim the article list up to a given maximum size
6. Pick the "best" article from the article list and:
    1. Store the title in a file called _title_
    2. Store the URL in a file called _link_
    2. Store the description in a file called _desc_
    3. Print out the title to STDOUT
7. Save the current article list for the next run


The way the "best article" is chosen is roughly like this:

- Look for the articles which have been used the least (ideally never)
- Pick the most recent one

We assume the feed delivers the articles ordered by date, so no check is done
on the script.
