import logging

# Crawling
start_url = "http://python.org"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
max_number_of_urls_to_visit = 1

# Words
num_of_words_to_return = 5000

# Logger
log_level = logging.DEBUG
log_filename = None