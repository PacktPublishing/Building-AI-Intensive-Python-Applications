# pip3 install --upgrade openai==1.41.0

# Include your OpenAI API key
# export OPENAI_API_KEY='your-api-key-here'

# Create an openai-test.py file and insert this
from openai import OpenAI

client = OpenAI()
completion = client.chat.completions.create(model="gpt-4o-mini", messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
])
print(completion.choices[0].message)