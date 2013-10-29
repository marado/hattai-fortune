hattai-fortune
==============

Hattai's Fortune: a script to be used by a bot, that gives news (from Público)

## Script's behaviour

This is the behaviour of the script, as extracted from the previous implementation.

When run the script will:

1. Read the RSS feed of the Público newspaper
   (http://http://feeds.feedburner.com/publicoRSS)
2. Exclude the article with the same title as the one from the previous run
3. Exclude the articles which contain any word from a given list of "bad words"
   (the match is case **insensitive**)
4. Exclude articles which have an empty title
5. Exclude articles which have the character '"' in the title
6. Pick off the first article from the remaining articles list and:
    1. Store the title in a file called _title_
    2. Store the URL in a file called _link_
    3. Print out the title to STDOUT
