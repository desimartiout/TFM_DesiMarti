import openai


#pip install --upgrade openai

from openai import OpenAI
client = OpenAI()

#model="gpt-4o",
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Eres un asistente útil."},
        {
            "role": "user",
            "content": "¿Cuál es la capital de Francia?"
        }
    ]
)

print(completion.choices[0].message)