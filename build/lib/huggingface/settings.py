# Scrapy settings for hf_parser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "hf_parser"

SPIDER_MODULES = ["huggingface.spiders"]
NEWSPIDER_MODULE = "huggingface.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "hf_parser (+http://www.yourdomain.com)"

ROBOTSTXT_OBEY = True
HTTPCACHE_ENABLED = True
