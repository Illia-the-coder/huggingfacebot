import scrapy
import requests

class HfSpiderSpider(scrapy.Spider):
    name = "hf_spider"
    allowed_domains = ["huggingface.co"]
    start_urls = ["https://huggingface.co"]

    def start_requests(self):
        # URL to the text file containing profile URLs
        # url = 'https://raw.githubusercontent.com/Illia-the-coder/huggingfacebot/master/huggingface/spiders/hf_profiles_urls.txt'
        url = 'https://content.freelancehunt.com/message/eb213/f9180/4066542/hf_profiles_1k.txt'
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        urls = page.text.splitlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_with_xpath(query):
            return response.xpath(query).get(default='').strip()

        def extract_with_xpath_length(query):
            return len(response.xpath(query).getall())
        
        followers_count = extract_with_xpath('/html/body/div/main/div/div/section[1]/div[4]/button[1]/text()').split('\n')[0]
        followers_count = 0 if len(followers_count) == 0 else int(followers_count)
        following_count = extract_with_xpath('/html/body/div/main/div/div/section[1]/div[4]/button[2]/text()').split(' ')[0]
        following_count = 0 if len(following_count) == 0 else int(following_count)
        
        Blocks = response.xpath('/html/body/div/main/div/div/section[2]/div/div/h3/div[1]/span[1]/text()').getall()
        Values = response.xpath('/html/body/div/main/div/div/section[2]/div/div/h3/div[1]').getall()
        blocksDict =  dict(zip(Blocks, Values)) 
        if 'Papers' in blocksDict.keys():
            papers_count = int(response.xpath(f'/html/body/div/main/div/div/section[2]/div/div[{Blocks.index("Papers")+1}]/h3/div[1]/span[2]/text()').get())
        else:
            papers_count = 0
        
        yield {
            'username': extract_with_xpath('/html/body/div/main/div/div/section[1]/h1/span/text()'),
            'nickname': extract_with_css('div.mb-4.inline-block.rounded::text'),
            'twitter_link': extract_with_css('a[href*="twitter.com"]::attr(href)'),
            'github_link': extract_with_css('a[href*="github.com"]::attr(href)'),
            'linkedin_link': extract_with_css('a[href*="linkedin.com"]::attr(href)'),
            'website_link': extract_with_xpath('/html/body/div/main/div/div/section[1]/div[5]/div/a/@href'),
            'interests': extract_with_xpath('/html/body/div/main/div/div/section[1]/div[6]/text()'),
            'articles_count': extract_with_xpath_length('/html/body/div/main/div/div/section[1]/div[7]/div/div[1]/div'),
            'papers_count': papers_count,
            'models_count': int(extract_with_xpath('//*[@id="models"]/h3/div[1]/span[2]/text()') or 0),
            'spaces_count': int(extract_with_xpath('//*[@id="spaces"]/h3/div[1]/span[2]/text()') or 0),
            'datasets_count': int(extract_with_xpath('//*[@id="datasets"]/h3/div[1]/span[2]/text()') or 0),
            'organizations_count': extract_with_xpath_length('/html/body/div/main/div/div/section[1]/div/a/img[@class="h-10 w-10 rounded"]'),
            'followers_count': followers_count,
            'following_count': following_count,
        }
