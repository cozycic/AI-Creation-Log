import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.responses.create(
    model="deepseek-v4-flash",
    input="请用一句话告诉我，什么是AI创业？"
)

print(response.output_text)