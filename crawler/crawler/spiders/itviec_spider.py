import scrapy

from crawler.items import JobItem


class ItviecSpider(scrapy.Spider):
    name = 'itviec'
    allowed_domains = ['itviec.com']

    def start_requests(self):
        start_url = 'https://itviec.com/it-jobs'
        cookies = {
            "_ITViec_session": "6713ds9XqKZhQtzTxJxhG0h%2BfSLmGKfvU9drjgq9%2Faaty%2B7axAqafMx%2FAKmOpGsyjIn%2B5wixE50NYvX5Ykn3p%2F6SXjw99bNF6QfDs%2F4rol5Ei4RxXhOztwpa4h%2FDU045y6jamiy657vpx0biCd68875aSmxJHFqvkslJN7QzRnw%2BdfqbLxTWLCqF5rbgARUZTczbtKddYv8zwVLifObDTkSTLzSzN4C3WP9hrnWMKiqHdOJ%2BiOTe8PYexT82RueHT9JRBKW3R5m0fa3jebNJWvzx3sM0yI7cvX%2Bzun03izpL90FWFr5%2BXoqb85y1Vnzdsuo0MWiTFyIXuVbvVbaWSc81Jr%2B5CUHvrEHUdcF%2F%2BenIDjMhBC3IbVPDfaLYWrWPrlL37LVg%2BslHq0OC%2F2TPrXTAWAfjuq0detlk%2FfL64B3osfq0avGzE2zi2zAGZ%2Bsm4vS8eH9O%2F%2Fg5oYUNnYj%2FRNZcVRPcaRZGzNKbLwkNjuCFPQ%2FVvz7fyBmBwx5%2F5fsDqXoj3x6IaE2v%2FNsTH5so2zeIjctnBNwZf0l%2FFbAqImwyZFTSWJZVRMbHKuH6iCoFNSY%2FaA4KVi57EazgXpCTmtPOuNkzL5uQC2Ddaz20WmYCQ9xzIGklg%2B2QxMVbJvR5Gmbka21HQlnVkdeWYOWWMKdOldjxWmGz2R8dnH3pbSM9JOPefZy%2BHh8kCCCJ1p5Bp45Gdw0Eg%2F%2BFLOZUucFcyz5JNFttCxArvSGZobKhizAQE0QvAYbtBFK6Z2%2F3StHwMsncewxit8lsUZBANSsQ0iRfZklJw88XvXNluoBaedEAGhQuLtsglu55LF37BNM%2Fe%2Blw4UiFC%2F%2Bg%2B6IR5bASYaG4b%2FOG0ivbV4FNJsbkfbSjMVb3gfyVRznXqmv81kJJVBuLOtNmzH16SENZIu79wao2fYgE--a5wBGPLpXcNeHUhR--WimBtJxZWw43f%2FFD2cmfnA%3D%3D",
            "auth_token": "sgD8ERdALBsUJVJxzCRe1lJyfRhRh3kZkqmA8sCQmm%2B%2BB4jRB6w%2BuzZF39cEI4PieDCPCoTidlUJRBO1%2BhTjLkvXAB%2Brc38gSaqLj8GAdOOHwaL2HZ7DWS59hpWEZLX0HUVeI6TJmiCLmTqNPyzXCoitYTS1wVJL09so91nCcgThYqT2c4eeFbgymBmfhUAtuXZNeU%2Ff0eQCQu4Ej8UuemxGSsE%2FaLZKllYmtGO1ay41HOa23boZySnx94k%2FW8kQr6wGBaFcC6I2dfAQl3padHeOJExEqfiiTtVqC2%2BdDdh68NNvVbZ1xRggZnIRINxjow%2FSdM%2BoUHK1I6LIBAdycGO9C8I%3D--XiNkmhjB9t7KOMwG--7mqaSXEjo6zboW%2B8ndLP6w%3D%3D",
            "cf_clearance": "3raIm65bGoj3Jh19gRSl6FW9iHR2dm0UGFXRz3ERCJk-1771918850-1.2.1.1-L4AbbBSOaaDjUv2yzAMelVQWhPN21M6qvJ2.amXB04RvnS3fAleqmUhoDVfXNI5wJ3yShGx4l5FnYABVs.B327H66dSFQR5dtFRmBfCsvJEoDXWNURvQXzl1IgO9aACPduAgJ2noKf2q0wkSupAHX82RKPn.vDCkS7P3xgVHQwLq6n14YK5Qsg5HX542z.OLA_Tw6lFD7dnQzsVlsbuPPRW6bgC72mSyg0DyYzZWfgE"
        }

        yield scrapy.Request(
            url=start_url,
            cookies=cookies,
            callback=self.parse
        )

    def parse(self, response):
        for job in response.css("div.job-card"):
            detail_url = job.css("h3::attr(data-url)").get()

            if detail_url:
                yield response.follow(
                    detail_url,
                    callback = self.parse_detail
                )

        next_page = response.css("a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback = self.parse)

    def parse_detail(self, response):
        job_item = JobItem()
        job_item['title'] = response.css("h1::text").get()
        job_item['company'] = response.css("div.employer-name::text").get()
        job_item['salary'] = response.css("div.salary span::text").get()
        job_item['url'] = response.url

        lines = response.css(
            "div.imb-3 > div.d-flex > div.d-inline-block span.normal-text::text"
        ).getall()

        keywords = ['accepted', 'at office','hybrid','remote', 'posted']
        locations = [
            line.strip()
            for line in lines
            if line.strip() and not any(k in line.lower() for k in keywords)
        ]

        job_item['locations'] = locations

        skills = response.xpath(
            "//h2[contains(text(), 'Your skills and experience')]/parent::div//text()"
        ).getall()

        skills = " ".join([t.strip() for t in skills if t.strip()])

        job_item['skills'] = skills

        yield job_item