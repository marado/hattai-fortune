#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# hattai-fortune
#
# Original author: Marcos Marado <mindboosternoori@gmail.com>
# Author of python version: Nuno Nunes <nuno@nunonunes.org>


import sys
import getopt
sys.path.append("./feedparser")
import feedparser
import pickle
import traceback
from html.parser import HTMLParser
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='debug.log')

# Configuration
#
debug = False
feed_url = \
    "https://news.google.com/news?pz=1&cf=all&ned=pt-PT_pt&hl=pt-PT&output=rss"
title_file_name = "title"
link_file_name = "link"
memory_file_name = "memory"
desc_file_name = "desc"
max_memory_size = 72
bad_words = ["olhanense", "psilon", "benfic", "assinant", "sporting",
             "chelsea", "arsenal", "derby", "golo", "djokovic", "jogo",
             "ronaldo", "Brasil"]
substitute_chars = {'“': '"', '”': '"'}
#
################


# Global variables
#
memory = []
logger = logging.getLogger(__name__)
#
################


# Functions
#
def getNewNews():
    """Read the RSS feed and fetch new articles."""

    global memory

    seen_titles = [article["title"] for article in memory]

    logger.debug("===> Parsing feed")
    new_memories = []
    feed = feedparser.parse(feed_url)
    for post in feed.entries:
        post.title = post.title.encode("utf-8")
        post.link = post.link.encode("utf-8")
        post.description = post.description.encode("utf-8")
        logger.debug("\"%s\"" % post.title)

        if post.title in seen_titles:
            logger.debug("Already seen this title, ignoring")
            continue
        if post.title == "":
            logger.debug("Empty title, ignoring")
            continue
        has_bad_words = False
        for bad_word in bad_words:
            if bad_word.encode('utf-8') in post.title.lower():
                has_bad_words = True
                logger.debug("Title has bad word \""+bad_word+"\" ignoring")
                continue
        if has_bad_words:
            continue

        new_memories.append({"title": post.title,
                             "link": post.link,
                             "description": post.description,
                             "published": post.published,
                             "used": 0})

    memory = new_memories + memory
    memory = memory[:max_memory_size]

    if logger.getEffectiveLevel() <= logging.DEBUG:
        __dump_memory__()


def chooseArticle():
    """Chooses an article from our memory, as fresh as possible, and returns
    it's index in memory."""

    best_used = 999999
    best_index = None
    i = 0

    logger.debug("===> Choosing the best article")
    logger.debug("Memory has " + str(len(memory)) + " articles")

    for article in memory:
        logger.debug("Analizyng article \"%s\" (%s)" % (article["title"],
                                                        str(article["used"])))
        if article["used"] < best_used:
            best_used = article["used"]
            best_index = i
            logger.debug("Best so far")

        i += 1

        if logger.getEffectiveLevel() <= logging.DEBUG:
            __dump_memory__()

    return best_index


def initializeStuff():
    """Read state from files (memory)."""

    global memory

    try:
        memory_file = open(memory_file_name, "rb")
        memory = pickle.load(memory_file)
        memory_file.close()
    except:
        memory = []

    logger.debug("===> Initializing")
    logger.debug("Found " + str(len(memory)) + " articles on disk:")

    if logger.getEffectiveLevel() <= logging.DEBUG:
        __dump_memory__()


def closeUpShop(chosen_article_index):
    """Commit memory to file, write title and link to files and reply with
    the chosen title."""

    logger.debug("===> Writing results and saving state")

    try:
        title_file = open(title_file_name, "w")
        link_file = open(link_file_name, "w")
        memory_file = open(memory_file_name, "wb")
        desc_file = open(desc_file_name, "w")
        title = memory[chosen_article_index]["title"].decode('utf-8')
        title = clean_string(title)
        title_file.write(title)
        link_file.write(memory[chosen_article_index]["link"].decode('utf-8'))
        desc_file.write(memory[chosen_article_index]["description"].decode('utf-8'))
        print(title)
        memory[chosen_article_index]["used"] += 1
        pickle.dump(memory, memory_file)
        title_file.close()
        link_file.close()
        memory_file.close()
    except:
        logger.error("BORK! : " + traceback.format_exc())

    logger.debug("Stored memory with " + str(len(memory)) + " articles")


def clean_string(text):
    clean_text = __strip_tags__(text)
    clean_text = __substitute_weird_chars__(clean_text)
    return clean_text


def __strip_tags__(html):
    s = MLStripper()
    logger.debug("__strip_tags__(html), htmlk is " + str(html));
    s.feed(str(html))
    return s.get_data()


def __substitute_weird_chars__(string):
    clean_string = string
    for char, subst in substitute_chars.items():
        clean_string = clean_string.replace(char, subst)

    return clean_string


def __dump_memory__():
    """Print the memory contents in a pretty way."""

    logger.debug("Memory contents:")
    for article in memory:
        logger.debug("---------- (%s) Title: \"%s\"" % (
            article["used"], article["title"]))
        logger.debug("Link: \"%s\"" % article["link"])
        logger.debug("Published: %s" % article["published"])
    logger.debug("EOM")


def handleOptions():
    global debug
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d", ["debug"])
    except:
        return

    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            debug = True

    if debug:
        logger.setLevel(logging.DEBUG)

#
################


# Class to strip HTML clean
#
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
#
################

if __name__ == "__main__":
    handleOptions()

    logger.debug("===> In the beginning...")

    initializeStuff()
    getNewNews()
    article_index = chooseArticle()
    closeUpShop(article_index)

    logger.debug("===> All done!")
