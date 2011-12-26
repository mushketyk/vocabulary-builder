#!/usr/bin/python2.7

import urllib2
import logging
import config
import re
import codecs
import threading

from stemming.porter2 import stem
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse

compiled_netloc_regexps = []
compiled_path_regexps = []



def crawl_netlock(net_lock):
    global compiled_netloc_regexps
    for regexp in compiled_netloc_regexps:
        match = regexp.match(net_lock)
        if match and len(match.group()) == len(net_lock):
            return True
    return False

def crawl_path(path):
    global compiled_path_regexps
    for regexp in compiled_path_regexps:
        match = regexp.match(path)
        if match and len(match.group()) == len(path):
            return True
    return False
    

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

        if crawl_netlock(link_netloc) and crawl_path(link_path):
            result_link = link_scheme + "://" + link_netloc + link_path
            readable_links.append(result_link)

    return readable_links

def get_most_used_words(found_words):
    sorted_words = sorted(found_words.keys(), key = lambda k: found_words[k], reverse=True)

    return sorted_words[:config.num_of_words_to_return]

def enumerate_words(html, words):
    striped_text = ''.join(BeautifulSoup(html).findAll(text=True))

    for line in striped_text.splitlines():
        for word in line.split():
            word = word.strip(config.symbols_to_strip)
            if word:
                word = word.lower()

                try:                
                    word = stem(word)
                    if word.isalpha():
                        words[word] = words.get(word, 0) + 1
                except IndexError as inst:
                    logging.error("Possibly bug in stem function for word: " + word + "\n" + str(inst))
                
def configure_logger():
    if config.log_filename is None:
        logging.basicConfig(level=config.log_level)
    else:
        logging.basicConfig(filename=config.log_filename, level=config.log_level)

def compile_netloc_regexps():
    global compiled_netloc_regexps
    compiled_netloc_regexps = map(lambda reg_exp: re.compile(reg_exp), config.netlocs_of_interest)

def compile_path_regexps():
    global compiled_path_regexps
    compiled_path_regexps = map(lambda reg_exp: re.compile(reg_exp), config.paths_of_interest)

def get_linked_urls(html):
    soup = BeautifulSoup(html)
    a_tags = soup.findAll('a')

    links = set()
    for tag in a_tags:
        if len(tag.attrs) and 'href' in tag.attrs[0]:
            links.add(tag['href'])

    return links

def get_html(url):
    req = urllib2.Request(url, None, config.headers)
    response = urllib2.urlopen(req)
    logging.debug("Type = " + response.headers.getmaintype())

    if response.headers.getmaintype() in config.text_mime_types:
        return response.read()

def write_dictionary(words):
    f = codecs.open(config.dictionary_output_file, encoding='utf-8', mode='w+')

    for word in words:
        f.write(word + "\n" + config.line_end)

def write_dictionary_with_usage(words, found_words):
    f = codecs.open(config.dictionary_with_usage_file, encoding='utf-8', mode='w+')

    for word in words:
        f.write(word + " " + str(found_words[word]) + config.line_end)

def show_progress(num_of_visited_urls):
    print "Visiting URL: " + str(num_of_visited_urls) + "/" + str(config.max_number_of_urls_to_visit)

visited_urls = set()
urls_to_visit = []

found_words = dict()
num_lock = threading.Lock()
num_of_visited_urls = 0

class CrawlThread(threading.Thread):
    def run(self):
        global num_of_visited_urls
        global found_words
        global num_lock
        global visited_urls
        global urls_to_visit

        while len(urls_to_visit) > 0 and len(visited_urls) < config.max_number_of_urls_to_visit:
            url = urls_to_visit.pop(0)
            num_lock.acquire()
            num_of_visited_urls += 1
            thread_url_number = num_of_visited_urls
            num_lock.release()

            if url not in visited_urls:
                logging.info("Visited: " + url)

                try:
                    html = get_html(url)
                    if html:
                        show_progress(thread_url_number)
                        links = get_linked_urls(html)

                        parse_result = urlparse(url)
                        new_links = create_readable_links(parse_result.scheme, parse_result.netloc, links)
                        urls_to_visit.extend(new_links)
                        visited_urls.add(url)

                        enumerate_words(html, found_words)

                except urllib2.HTTPError as inst:
                    logging.info("HTTP error during reading" + url + ": " + str(inst))
                except urllib2.URLError as inst:
                    logging.info("HTTP error during reading" + url + ": " + str(inst))
                except UnicodeError as inst:
                    logging.error("Unicode error during reading " + url)


if __name__ == "__main__":
    configure_logger()
    compile_netloc_regexps()
    compile_path_regexps()
    logging.info("Vocabulary builder started")

    urls_to_visit.extend(config.start_urls)

    threads = set()

    for i in range(config.number_of_threads):
        crawl_thread = CrawlThread()
        crawl_thread.setDaemon(True)
        crawl_thread.start()
        threads.add(crawl_thread)

    for thread in threads:
        thread.join()

    words = get_most_used_words(found_words)

    write_dictionary(words)
    write_dictionary_with_usage(words, found_words)
    logging.info("Done.")

