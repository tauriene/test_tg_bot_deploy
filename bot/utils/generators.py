from openai import AsyncOpenAI
from bot.utils.config import settings


client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.ai_text_token.get_secret_value(),
)


async def genetate_text(req: str) -> dict[str, str]:
    try:
        completion = await client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[{"role": "user", "content": req}],
            max_tokens=500,
        )

        return {"ok": True, "text": completion.choices[0].message.content}
    except:
        return {"ok": False}
