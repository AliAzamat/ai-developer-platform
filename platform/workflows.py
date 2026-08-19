from openai import OpenAI

client = OpenAI()

# The "product" the platform sells access to: an AI workflow. Keeping it a plain
# function means the platform layers (auth, limits, queue) wrap it without
# knowing what it does — swap this for any AI task and the platform is unchanged.
def summarize(text: str, model: str = "gpt-4o-mini") -> str:
    """One AI workflow: summarize text. The unit of work the platform exposes."""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize the user's text in two sentences."},
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content or ""
