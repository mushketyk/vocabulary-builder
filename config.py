# To set logging level in config
import logging

##### Crawling #####
# Set of URLs that are used to start crawling
start_urls = ("http://en.wikipedia.org",)
# User agent that will be set in all HTTP requests
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# Some sites blocks robots, to avoid this, we pretend as a broswer
headers = { 'User-Agent' : user_agent }
#
max_number_of_urls_to_visit = 200
# Only those URLs that match any of this regexps will be visited
netlocs_of_interest = ('en\\.wikipedia\\.org.*',)
# List MIME types of crawled documents
text_mime_types = ('text',)

##### Words #####
# Size of collected dictionary
num_of_words_to_return = 10000
# Symbols that should be striped from the beginning and end of each word, found in a document. This helps to
# recognize words as '(programming', 'Python,' etc.
symbols_to_strip = " '.,;[](){}-_1234567890:!\|/&#$%=\""

###### Dictionary #####
# File to output the most popular words that are used on the crawled web pages
dictionary_output_file = "dictionary"
# The same as a previous one, but also output number of occurrence of words
dictionary_with_usage_file = "ext_dictionary"

##### Logger #####
# Level of logging
log_level = logging.DEBUG
# File to output log to
log_filename = None