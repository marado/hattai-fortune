#!/usr/bin/env python
 # -*- coding: utf-8 -*-

# hattai-fortune
#
# Original author: Mindbooster Noori
# Author of python version: Nuno Nunes <nuno@nunonunes.org>


import sys
sys.path.append("./feedparser")
import feedparser
import pickle
import traceback
from HTMLParser import HTMLParser

# Configuration
#
debug            = False
feed_url         = "http://feeds.feedburner.com/publicoRSS"
title_file_name  = "title"
link_file_name   = "link"
memory_file_name = "memory"
max_memory_size  = 20
bad_words        = [ "olhanense", "psilon", "benfic", "assinant", "sporting",
                     "chelsea", "arsenal", "derby", "golo", "djokovic", "jogo",
                     "ronaldo" ]
substitute_chars = { '“': '"', '”': '"' }
#
################


# Global variables
#
memory         = []
#
################


# Functions
#
def getNewNews():
    """Read the RSS feed and fetch new articles."""

    global memory

    seen_titles = [ article["title"] for article in memory ]

    if debug:
        print "===> Parsing feed"
    new_memories = []
    feed = feedparser.parse(feed_url)
    for post in feed.entries:
        post.title = post.title.encode("utf-8")
        post.link  = post.link.encode("utf-8")
        if debug:
            print "\"" + post.title + "\""
        if post.title in seen_titles:
            if debug:
                print "Already seen this title, ignoring"
            continue
        if post.title == "":
            if debug:
                print "Empty title, ignoring"
            continue
        has_bad_words = False
        for bad_word in bad_words:
            if bad_word in post.title.lower():
                has_bad_words = True
                if debug:
                    print "Title has bad word \"" + bad_word + "\" ignoring"
                continue
        if has_bad_words:
            continue

        new_memories.append( { "title": post.title, "link": post.link, "published": post.published, "used": 0 } )

    memory = new_memories + memory
    memory = memory[:max_memory_size]

    if debug:
        print "Memory contents:"
        __dump_memory__()
        print


def chooseArticle():
    """Chooses an article from our memory, as fresh as possible, and returns
    it's index in memory."""

    best_used  = 999999
    best_index = None
    i          = 0
    if debug:
        print "===> Choosing the best article"
        print "Memory has " + str(len(memory)) + " articles"
    for article in memory:
        if debug:
            print "Analizyng article \"" + article["title"] + "\" (" \
                  + str(article["used"]) + ")"
        if article["used"] < best_used:
            best_used  = article["used"]
            best_index = i
            if debug:
                print "Best so far"
        i += 1

    if debug:
        print "Memory contents:"
        __dump_memory__()
        print

    return best_index


def initializeStuff():
    """Read state from files (memory)."""

    global memory

    try:
        memory_file = open(memory_file_name, "rb")
        memory      = pickle.load(memory_file)
        memory_file.close()
    except:
        memory = []

    if debug:
        print "===> Initializing"
        print "Found " + str(len(memory)) + " articles on disk:"
        __dump_memory__()
        print


def closeUpShop( chosen_article_index ):
    """Commit memory to file, write title and link to files and reply with
    the chosen title."""

    if debug:
        print "===> Writing results and saving state"

    try:
        title_file  = open( title_file_name, "w" )
        link_file   = open( link_file_name, "w" )
        memory_file = open( memory_file_name, "wb" )
        title = memory[chosen_article_index]["title"]
        title = clean_string( title )
        title_file.write( title )
        link_file.write( memory[chosen_article_index]["link"] )
        print title
        memory[chosen_article_index]["used"] += 1
        pickle.dump( memory, memory_file )
        title_file.close()
        link_file.close()
        memory_file.close()
    except:
        print "BORK! : " + traceback.format_exc()

    if debug:
        print "Stored memory with " + str(len(memory)) + " articles"


def clean_string( text ):
    clean_text = __strip_tags__( text )
    clean_text = __substitute_weird_chars__( clean_text )
    return clean_text


def __strip_tags__( html ):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def __substitute_weird_chars__( string ):
    clean_string = string
    for char, subst in substitute_chars.iteritems():
        clean_string = clean_string.replace( char, subst )

    return clean_string


def __dump_memory__():
    """Print the memory contents in a pretty way."""

    for article in memory:
        print "---------- (" + str(article["used"]) + ") Title: \"" + article["title"] + "\""
        print "Link: \"" + article["link"] + "\""
        print "Published: " + article["published"]
#
################


# Class to strip HTML clean
#
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
#
################



if __name__ == "__main__":
    if debug:
        print "===> In the beginning..."
    initializeStuff()
    getNewNews()
    article_index = chooseArticle()
    closeUpShop( article_index )
    if debug:
        print "===> All done!"
