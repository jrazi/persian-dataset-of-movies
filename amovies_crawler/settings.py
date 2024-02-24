# settings.py for amovies_crawler

# Scrapy settings for amovies_crawler project
BOT_NAME = 'amovies_crawler'

SPIDER_MODULES = ['amovies_crawler.spiders']
NEWSPIDER_MODULE = 'amovies_crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False 

# Configure a delay for requests for polite crawling
DOWNLOAD_DELAY = 0.5

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Enable or disable retrying
RETRY_ENABLED = True
RETRY_TIMES = 3

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 60  # Cache never expires, adjust if necessary
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []  # Caching responses with these codes
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60

# Enable and configure logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(levelname)s: %(message)s'
LOG_FILE = 'movie_detail_spider.log'

# Resume capability - setting separate job directories for each spider
JOBDIR = 'jobdir'  # Base directory for job state

ITEM_PIPELINES = {
    'amovies_crawler.pipelines.MovieValidationPipeline': 100,
    'amovies_crawler.pipelines.MovieDataPipeline': 200,
}

DOWNLOAD_TIMEOUT = 180

# Retry a failed request up to 5 times (default is 2)
RETRY_TIMES = 5

# Enable cookies for your spider
COOKIES_ENABLED = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
