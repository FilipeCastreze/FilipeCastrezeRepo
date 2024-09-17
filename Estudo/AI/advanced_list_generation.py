import openai
import re
import getpass
import json

openai.api_key = getpass.getpass("Please enter your OpenAI Key:")

def complete(prompt):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
            "role": "user",
            "content": prompt
            }
        ],
    )
    return response.choices[0].message.content

complete("is this working?")