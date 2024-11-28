import openai
from config import openai_key

openai.api_key=openai_key


# プロンプトを基に出力
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
      {
        "role": "system",
        "content": "For the following task, respond in a way that matches this description:\n"
        "'I am introverted, antagonistic, conscientious, emotionally stable, and closed to experience.'"
      },
      {
        "role": "user",
        "content": "Please rate the following statement by selecting a number from 1 to 5, where:\n"
                   "1 = not applicable at all,\n"
                   "2 = not applicable,\n"
                   "3 = neutral,\n"
                   "4 = applicable,\n"
                   "5 = strongly applicable.\n\n"
                   "友達と話すのが好きだ。"
      },
    ],
    max_tokens=1,
)

print(response.choices[0].message.content)