import scrapy

from crawler.items import JobItem


class ItviecSpider(scrapy.Spider):
    name = 'itviec'
    allowed_domains = ['itviec.com']

    def start_requests(self):
        start_url = 'https://itviec.com/it-jobs'
        cookies = {
            "_ITViec_session": "vISddNCOd70O%2F6Zr%2F9Ci5gnB6%2BVq42ZtWFCTuiVAczXwnVH5L3cj20pJiDdlx28kfvyi5QZeQD0Hje5CMcPRyR1j62yIsu2lVk1Ih1K48RianFf70VW5QNZrDlwPY14V3ZMM4inswonWPt0RLwtjK81UySxFgSE9KXl4UIz6JdEGo3T3lqZVGuYqvvcuPjDuqcsabe2xY43QtdWvSk48gAiMFTWW7CeE1Uha%2B096tAS2VNoae4FByG%2Fge7ANKRGHI8DM72pwhsernIDplrYxdNDt%2FbanKrWxxtbjgCroyFc5iqlepDwOobJxdcmy1I%2BL2kbfU60xfDVSANFnxodyFFNf8mE2cvznydc57hj8tWOIkVnXj9JdNFf1lgLdE0jUSVEmNDj97ZSeFhwRugkffMa5BuqUiWjdlD22XyT2otO%2FNHpi2d%2BhAIrm4n3WqwmE8eYiDci%2B8kg5YS8I%2F0M3vEp2biR0UOLvan2mcXxgaIw7%2BmEArR3mAXOdSJCy0EAEfSvytAarVcLyGLZpfM%2B5dSQkqSp%2BTR%2Bqcm%2BFM9eeiOam6VFt4VV1XhbwPm%2F%2Bdeq1VL5x2saRTOuehz0qWPBHU6PyX3V0sxUpTJXwfZe0w0%2BHHfaa%2FgnQtkgJH3k1zBjhcKnjw%2FdAQvXvWSsPFekQQopyaoiKevfUJqQ7a2sdNJihGSYh308pyzUtBXLTqYEoDM%2BZtK3gdmyngEczovbFBGDJIbzVYRm5Nf9fpohd93tBWwVTzO%2FQvJkYwHJpJQAN6Db5XeGdJFO%2FEWCt4SDso1i9HNTxwpvxu%2B0GW5UNIbVxcGFQhyBx1pfst3RMDIHtIWMP%2BcXNwx%2F%2FpegtueTM5UXgwldSoeg%2FuHiLkjzAtkXTKGwq1lu0uCMZVQCrXiOu5RhUQZPsi%2BFSYs08v2nRHCVm2ixpHF2Qj%2FFtr7k%3D--6xHtpjhHzgRNpgEs--Z%2BqgR5XapXX2VWgwuUmhPA%3D%3D",
            "auth_token": "vhExTBuWb%2FbUcXrKD4Z%2B7Yo4130cnO0gamf1HlLaRwTdpSZHqu861c3sGc7hCnbjGYwNEeDO%2BXRG4KcioOgGXJK3uTF9kU2IIRR%2BPNip%2BhDuDf9YDYHw%2FeVyCzclxqOhHIfE39CpwfD1l999DLfHR%2BMoRxLbrUsHmsoK9qHynIT4EuZC%2FC8pMM6kSpZTdtrE2yxClM0OT5p27Q%2FiqGRKEf%2F66E8ZvV9n02z1e4Vc%2F2r3em2YcgD5KNG3bj0ioVBrusiqVp%2BkeZ3%2Br%2FaEW1UNha8jgI4XUyAcivAvtmAWjeXAxVKaUukX6xZq3%2F17ropKIq4j0%2BkPA2zon6MgxnG5BTOvzEk%3D--4qd0l%2Btymqclv3zv--%2BpjA7RinLq7hDFury7rCaw%3D%3D",
            "cf_clearance": "JPm8R8OPtkAjlWu9_pXLj6qoxUXP4kYcUdg08nqc_sQ-1772537019-1.2.1.1-6n1TDVKbcOo7bc8g43UjsRXAbfXjLvzD5pAZepFkjcUaiCSwFc1FVfpruBVVPT7y8THm8ihb0G3SK6hWkHNXMovf4AatTAbPYKA2nRAknnfklBtQt3OuYLpW76iNrIbGgORSsGfzr0vLtdJVdHGSev_s7U6ussI8rbRZVHFFnkPv6aznM44Zo4buclRzN4bHZs6B8E.I5UyMamiD1qmAn9aJ9_yhOYE1dj4mm23QvHw"
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