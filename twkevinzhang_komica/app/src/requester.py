import asyncio
import aiohttp


class Result:
    def __init__(self, key, url, html, error: Exception | None = None):
        self.key = key
        self.url = url
        self.html = html
        self.error = error

    def is_failed(self):
        return self.error is not None


class Requester:
    def __init__(self):
        pass

    async def __fetch(self, session, key, url) -> Result:
        # 取得 url 的 response，失敗則在 max_tries 內持續嘗試
        try:
            response = await session.get(url)
            response.raise_for_status()
            html = await response.text()
            await response.release()
            return Result(key, url, html)
        except Exception as e:
            return Result(key, url, None, e)

    async def crawl(
            self,
            urls: dict[str, str], # key -> url
    ) -> list[Result]:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            tasks = [self.__fetch(session, key, url) for key, url in urls.items()]
            return await asyncio.gather(*tasks)

    async def single_crawl(self, url) -> Result:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            return await self.__fetch(session, url, url)
