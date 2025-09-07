import aiohttp
from config import SUMMARY_SERVER, SEARCH_SERVER


async def summarize_text(text: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(SUMMARY_SERVER, json={"text": text}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("summary", "No summary found in response.")
                else:
                    return f"Error from summarizer: {resp.status}"
        except Exception as e:
            return f"Failed to contact summarizer: {e}"


async def search_text(text: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(SEARCH_SERVER, json={"text": text}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("web_search", "No search result found in response.")
                else:
                    return f"Error from searcher: {resp.status}"
        except Exception as e:
            return f"Failed to contact searcher: {e}"
