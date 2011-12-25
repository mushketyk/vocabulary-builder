import logging

##### Crawling #####
start_url = "http://en.wikipedia.org"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
max_number_of_urls_to_visit = 200
netlocs_of_interest = ('en\\.wikipedia\\.org.*',)
text_mime_types = ('text',)

##### Words #####
num_of_words_to_return = 10000
symbols_to_strip = " '.,;[](){}-_1234567890:!\|/&#$%=\""

###### Dictionary #####
dictionary_output_file = "dictionary"
dictionary_with_usage_file = "ext_dictionary"

##### Logger #####
log_level = logging.DEBUG
log_filename = None