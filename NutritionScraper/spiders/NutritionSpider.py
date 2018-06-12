import scrapy


class NutritionSpider(scrapy.Spider):
    name = "nutrition"

    def getPages(self):
        base = "https://www.iherb.com/c/Grocery?p="
        pages = []
        for i in range(1, 2):
            pages.append(base + str(i))

        return pages

    def start_requests(self):
        pages = self.getPages()
        print(pages)

        for page in pages:
            yield scrapy.Request(url=page, callback=self.parse)

    def parse(self, response):
        page_type = response.url.split("/")[3]
        print(page_type)

        if page_type == "c":
            items = []

            for div in response.css('div.product-inner'):
                items.append(div.css('a::attr(href)').extract_first())

            for item in items:
                yield scrapy.Request(url=item, callback=self.parse)

        elif page_type == "pr":
            name = response.url.split("/")[4] + ".txt"
            div = response.css('div.supplement-facts-container table').extract_first()

            with open(name, 'wb') as f:
                f.write(div.encode())
            print("saved file in ", name)