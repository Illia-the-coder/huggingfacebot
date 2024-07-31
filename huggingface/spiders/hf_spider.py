import scrapy


class HfSpiderSpider(scrapy.Spider):
    name = "hf_spider"
    allowed_domains = ["huggingface.co"]
    start_urls = ["https://huggingface.co"]

    def start_requests(self):
        # Відкриваємо файл з URL профілів
        with open('https://raw.githubusercontent.com/Illia-the-coder/huggingfacebot/master/huggingface/spiders/hf_profiles_urls.txt', 'r') as file:
            urls = file.read().splitlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        def extract_with_xpath(query):
            return response.xpath(query).get(default='').strip()
        def extract_with_xpath_length(query):
            return len(response.xpath(query).getall())

        

        yield {
            'Ім\'я користувача': extract_with_xpath('/html/body/div/main/div/div/section[1]/h1/span/text()'),
            'Нікнейм': extract_with_css('div.mb-4.inline-block.rounded::text'),
            'Посилання на X': extract_with_css('a[href*="twitter.com"]::attr(href)'),
            'Посилання на GitHub': extract_with_css('a[href*="github.com"]::attr(href)'),
            'Посилання на LinkedIn': extract_with_css('a[href*="linkedin.com"]::attr(href)'),
            'Посилання на сайт': extract_with_xpath('/html/body/div/main/div/div/section[1]/div[5]/div/a/@href'),
            'Інтереси': extract_with_xpath('/html/body/div/main/div/div/section[1]/div[6]/text()') ,
            'Кількість статей': extract_with_xpath_length('/html/body/div/main/div/div/section[1]/div[7]/div/div[1]/div'),
            'Кількість моделей': int(extract_with_xpath('//*[@id="models"]/h3/div[1]/span[2]/text()') or 0),
            'Кількість спейсів': int(extract_with_xpath( '//*[@id="spaces"]/h3/div[1]/span[2]/text()') or 0),
            'Кількість датасетів': int(extract_with_xpath('///*[@id="datasets"]/h3/div[1]/span[2]/text()') or 0),
            'Кількість організацій': extract_with_xpath_length('/html/body/div/main/div/div/section[1]/div[8]/a'),
            'Кількість людей, які підписані': int(extract_with_xpath('/html/body/div/main/div/div/section[1]/div[4]/button[1]/text()').split('\n')[0]),
            'Кількість людей на яких підписаний': int(extract_with_xpath('/html/body/div/main/div/div/section[1]/div[4]/button[2]/text()').split(' ')[0]),
        }