import aiohttp

SUMMARY_SERVER = "http://127.0.0.1:8000/summarize"  # replace with your IP:PORT


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
