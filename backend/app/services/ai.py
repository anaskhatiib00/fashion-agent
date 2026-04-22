import json
from openai import OpenAI


def generate_caption(item):
    try:
        client = OpenAI()

        prompt = f"""
You are a fashion marketing expert.

Create:
- product title
- short description
- Instagram caption
- hashtags

Item details:
Title: {item["title"]}
Price: {item["price"]}
Quantity: {item["quantity"]}
Size: {item["size"]}
Color: {item["color"]}
Notes: {item["notes"]}

Return valid JSON only in this format:
{{
  "title": "...",
  "description": "...",
  "caption": "...",
  "hashtags": ["...", "..."]
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        content = response.choices[0].message.content
        return content if content else json.dumps({
            "title": item["title"],
            "description": "",
            "caption": "",
            "hashtags": []
        })
    except Exception as error:
        return f"AI generation failed: {str(error)}"