import asyncio
import logging
import aiohttp

class Result:
    def __init__(self, url, html, error = None):
        self.url = url
        self.html = html
        self.error = error

    def is_failed(self):
        return self.error is not None


class Requester:
    def __init__(self):
        pass

    async def __fetch(self, session, url):
        # 取得 url 的 response，失敗則在 max_tries 內持續嘗試
        try:
            response = await session.get(url)
            response.raise_for_status()
            html = await response.text()
            await response.release()
            return Result(url, html)
        except Exception as e:
            return Result(url, None, e)

    async def crawl(self, urls) -> list[Result]:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            tasks = [self.__fetch(session, x) for x in urls]
            return await asyncio.gather(*tasks)

    async def single_crawl(self, url) -> Result:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            return await self.__fetch(session, url)
