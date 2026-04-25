import json

from openai import OpenAI


def generate_caption(item):
    try:
        client = OpenAI()

        prompt = f"""
You are a fashion marketing expert.

Create marketing content for this clothing item.

Item details:
- Title: {item["title"]}
- Price: {item["price"]}
- Quantity: {item["quantity"]}
- Size: {item["size"]}
- Color: {item["color"]}
- Notes: {item["notes"]}

Return valid JSON only in exactly this format:
{{
  "title": "short improved product title",
  "description": "short product description",
  "caption": "instagram-ready caption with price and quantity",
  "hashtags": ["#tag1", "#tag2", "#tag3"]
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        content = response.choices[0].message.content

        if not content:
            return json.dumps({
                "title": item["title"],
                "description": "",
                "caption": "",
                "hashtags": []
            })

        return content

    except Exception as error:
        return json.dumps({
            "title": item["title"],
            "description": "",
            "caption": f"AI generation failed: {str(error)}",
            "hashtags": []
        })