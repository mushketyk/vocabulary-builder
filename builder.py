#!/usr/bin/python2.7
from BeautifulSoup import BeautifulSoup

import urllib2
import logging
import config

from urlparse import urlparse

def create_readable_links(scheme, netloc, links):
    readable_links = []

    for link in links:
        parse_result = urlparse(link)

        link_scheme = scheme
        link_netloc = netloc
        link_path = parse_result.path

        if parse_result.scheme:
            link_scheme = parse_result.scheme

        if parse_result.netloc:
            link_netloc = parse_result.netloc

        result_link = link_scheme + "://" + link_netloc + link_path
        readable_links.append(result_link)

    return readable_links

def get_most_used_words(found_words):
    sorted_words = sorted(found_words.keys(), key = lambda k: found_words[k], reverse=True)

    return sorted_words[:config.num_of_words_to_return]

def enumerate_words(html, words):
    striped_text = ''.join(BeautifulSoup(html).findAll(text=True))

    #print striped_text

    for line in striped_text.splitlines():
        for word in line.split():
            #print word
            words[word] = words.get(word, 0) + 1


if __name__ == "__main__":
    if config.log_filename is not None:
        logging.basicConfig(level=config.log_level)
    else:
        logging.basicConfig(filename=config.log_filename, level=config.log_level)
    logging.info("Vocabulary builder started")

    visited_urls = set()
    urls_to_visit = [config.start_url]
    num_of_visited_urls = 0
    found_words = dict()

    while len(urls_to_visit) or num_of_visited_urls < config.max_number_of_urls_to_visit:

        url = urls_to_visit.pop()

        req = urllib2.Request(url, None, config.headers)
        response = urllib2.urlopen(req)
        html = response.read()

        soup = BeautifulSoup(html)

        a_tags = soup.findAll('a')
        print str(len(a_tags))

        links = set()
        for tag in a_tags:

            if 'href' in tag.attrs[0]:
                print tag['href']

                links.add(tag['href'])

        parse_result = urlparse(url)
        links = create_readable_links(parse_result.scheme, parse_result.netloc, links)

        for link in links:
            print link

        visited_urls.add(url)

        enumerate_words(html, found_words)

        num_of_visited_urls += 1

    print found_words
    words = get_most_used_words(found_words)

    for word in words:
        print word