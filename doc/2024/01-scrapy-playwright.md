1.为什么使用框架：
框架的使用就是为了让我们的开发更大项目的时候更加容易，小的爬虫我觉得不需要；
但是学习框架确实没那么容易，为了能搞出更大的事情，只能是坚持下去，自己选择的路跪着也要走完呀


- https://www.xiegerts.com/post/infinite-scroll-scrapy-playwright/ 对了


参考资料：
- https://github.com/scrapy-plugins/scrapy-playwright
- https://www.zenrows.com/blog/scrapy-playwright#why-use-playwright-with-scrapy
- https://scrapeops.io/python-scrapy-playbook/scrapy-playwright/
- https://www.youtube.com/watch?v=EijzO7n2-dg&ab_channel=ScrapeOps
- https://scrapy-chs.readthedocs.io/zh-cn/0.24/topics/architecture.html
-  https://qixinbo.info/2023/01/25/web-crawler-9/ 52讲轻松搞定网络爬虫笔记9
- https://github.com/Python3WebSpider/ScrapyTutorial

-  How To Scroll Infinite Pages in Python

When web scraping, infinite scrollers can present some major challenges. Scraping is the easiest when we're dealing with static content. 
One of the best ways to deal with an infinite scroller is by using a headless browser such as Selenium, Playwright or Puppeteer.


How does that work?
When you visit a site and scroll to the bottom, the webpage automatically sends a request via JavaScript for more content.


- https://github.com/jonwoong/Scrapy-Samples/tree/master/Books

简而言之，
Playwright 是一个强大的浏览器自动化工具，
而 scrapy-playwright 是 Scrapy 的一个扩展，使得用户可以在 Scrapy 项目中使用 
Playwright 的功能。这种结合使得在处理现代网页时，Scrapy 的爬虫能够更有效地抓取和解析数据。


## 操作步骤

### Installation
pip install scrapy-playwright
playwright install

scrapy startproject myspider
You can start your first spider with:
    cd playwright_scraper
    scrapy genspider zhsxq https://wx.zsxq.com/group/88885284844882

        Initialize a Scrapy spider for the target page:
        为目标页面初始化一个Scrapy蜘蛛：




scrapy crawl zhsxq

scrapy crawl quotes
https://github.com/python-scrapy-playbook/quotes-js-project


class Request(
    url: str,
    callback: ((...) -> Any) | None = None,
    method: str = "GET",
    headers: dict | None = None,
    body: bytes | str | None = None,
    cookies: dict | List[dict] | None = None,
    meta: dict | None = None,
    encoding: str = "utf-8",
    priority: int = 0,


playwright_include_page 这个参数做作用是什么




`playwright_include_page` 参数在 Scrapy 与 Playwright 集成时起到了关键的作用。以下是关于这个参数作用的详细解释：

1. **传递页面对象**：
   当在 Scrapy 请求中设置 `playwright=True` 时，Scrapy 会使用 Playwright 来处理该请求，允许对 JavaScript 渲染的页面进行抓取。`playwright_include_page` 参数则进一步指示 Scrapy 在处理响应时是否将 Playwright 的 `Page` 对象包含在内。如果设置为 `True`，则可以在 Scrapy 的回调函数（如 `parse` 方法）中访问到这个 `Page` 对象。

2. **扩展页面交互**：
   通过包含 `Page` 对象，开发者可以在 Scrapy 回调函数中利用 Playwright 提供的丰富 API 进行页面交互，如点击元素、填写表单、等待特定事件等。这使得 Scrapy 能够处理更复杂的抓取场景，尤其是那些需要模拟用户行为或处理动态加载内容的页面。

3. **整合两个工具的优势**：
   Scrapy 本身是一个强大的网页抓取框架，擅长处理静态页面和高并发的抓取任务。而 Playwright 则专注于浏览器自动化，能够处理 JavaScript 渲染和动态内容。通过 `playwright_include_page` 参数，Scrapy 和 Playwright 可以无缝集成，充分发挥各自的优势，从而更高效地抓取和处理现代网页。

综上所述，`playwright_include_page` 参数在 Scrapy 与 Playwright 的集成中起到了桥梁的作用，它使得开发者能够在 Scrapy 的回调函数中访问和操作 Playwright 的 `Page` 对象，从而扩展了 Scrapy 的功能，使其能够应对更复杂的网页抓取需求。

https://www.xiegerts.com/post/infinite-scroll-scrapy-playwright/


def scroll_to_bottom(self, page):
        # 滚动页面并等待新内容加载
        prev_height = 0
        while True:
            # 执行滚动
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            # 等待加载
            page.wait_for_timeout(1000)  # 等待 1 秒
            # 获取当前高度
            new_height = page.evaluate("document.body.scrollHeight")
            # 如果没有新的内容加载，则停止
            if new_height == prev_height:
                break
            prev_height = new_height