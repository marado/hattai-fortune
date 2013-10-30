#!/usr/bin/env python

# hattai-fortune
#
# Original author: Mindbooster Noori
# Author of python version: Nuno Nunes <nuno@nunonunes.org>


import sys
sys.path.append("./feedparser")
import feedparser
import pickle
import traceback

# Configuration
#
feed_url = "http://feeds.feedburner.com/publicoRSS"
title_file_name = "title"
link_file_name = "link"
memory_file_name = "memory"
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

try:
    memory_file = open(memory_file_name, "rb")
    memory = pickle.load(memory_file)
    memory_file.close()
except:
    memory = []

feed = feedparser.parse(feed_url)
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
    memory.append( {"title": post.title, "link": post.link} )

try:
    title_file = open( title_file_name, "w" )
    link_file  = open( link_file_name, "w" )
    memory_file = open( memory_file_name, "wb" )
    title_file.write( memory[0]["title"] )
    link_file.write( memory[0]["link"] )
    pickle.dump( memory, memory_file )
    title_file.close()
    link_file.close()
    memory_file.close()
    print memory[0]["title"]
except:
    print "BORK! : " + traceback.format_exc()
