#!/usr/bin/env python

# hattai-fortune
#
# Original author: Mindbooster Noori
# Author of python version: Nuno Nunes <nuno@nunonunes.org>


import sys
sys.path.append("./feedparser")
import feedparser

# Configuration
#
feed_url = "http://feeds.feedburner.com/publicoRSS"
title_file_name = "title"
link_file_name = "link"
#
################

bad_words = [
    "olhanense",
    "psilon",
    "benfic",
    "assinant",
    "sporting",
    "chelsea",
    "arsenal",
    "derby",
    "golo",
    "djokovic",
    "jogo",
    "ronaldo",
    "lt;",]

try:
    title_file = open(title_file_name, "r")
    previous_title = title_file.readline()
    title_file.close()
except:
    previous_title = ""


feed = feedparser.parse(feed_url)
articles = []
for post in feed.entries:
    post.title = post.title.encode("utf-8")
    post.link  = post.link.encode("utf-8")
    if post.title == previous_title:
        continue
    if post.title == "":
        continue
    if '"' in post.title:
        continue
    has_bad_words = False
    for bad_word in bad_words:
        if bad_word in post.title.lower():
            has_bad_words = True
            continue
    if has_bad_words:
        continue
    articles.append( [post.title,post.link] )

try:
    title_file = open( title_file_name, "w" )
    link_file  = open( link_file_name, "w" )
    title_file.write( articles[0][0] )
    link_file.write( articles[0][1] )
    title_file.close()
    link_file.close()
    print articles[0][0]
except:
    print "BORK! : " + sys.exc_info()[0]
