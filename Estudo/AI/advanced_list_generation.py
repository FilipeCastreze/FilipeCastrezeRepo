import openai
import re
import getpass
import json
import yaml

openai.api_key = getpass.getpass("Please enter your OpenAI Key:")

def complete(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": prompt
            }
        ],
    )
    return response.choices[0].message.content

complete("is this working?")

# Setup the article title
article = "What is data engineering?"
# Inject the article title into the base prompt
base_prompt = f'Write a numbered, hierarchical outline for an article on "{article}"\n\nHere is an example, of the structure:\n\n1. Introduction \n    a. Definition of digital marketing \n2. Types of Digital Marketing \n    a. Search Engine Optimization \n    b. Social Media Marketing \n    c. Content Marketing \n    d. Pay-Per-Click Advertising \n    e. Email Marketing \n3. Benefits of Digital Marketing \n    a. Cost-Effective \n    b. Targeted Audience \n    c. Measurable Results \n    d. Increased Reach \n\n----\n'

result = complete(base_prompt)

# Combine the two patterns so that we have a dictionary that looks like this:
# {
#     "1. Introduction": {"a.": "Definition of digital marketing"},
#     "2. Types of Digital Marketing": {
#         "a.": "Cost-Effective",
#         "b.": "Targeted Audience",
#         "c.": "Measurable Results",
#     },
# }

print(result)

# Extract main sections
main_sections = re.findall(r'\d+\..*?(?=^\d+|\Z)', result, re.MULTILINE | re.DOTALL)

# Extract sub-sections
sections = {}
for section in main_sections:
    section_title = re.search(r'\d+\..+', section).group(0)
    sub_sections = re.findall(r'\s+[a-z]\..+', section, re.MULTILINE)
    sections[section_title] = [heading.strip() for heading in  sub_sections]

print(sections)

prompt = "Produce an article outline for \"What is data engineering?\"\n\nHere is an example, of the structure. Always return valid JSON.\n\n{\n\"top_heading_one:\": [\"subheading_one\", \"subheading_two\"],\n\"top_heading_two:\": [\"subheading_one\", \"subheading_two\"],\n} \n\nRemember that the ouput must be like the above, and must be parsable JSON.\n\n----\n\n"
result = complete(prompt)
json.loads(result)

try:
  print(json.loads(result))
except Exception as e:
  # Re-running the gpt-4
  pass
  # Parsing the text and trying to extract the data from the string

prompt = "Produce an article outline in the format a .yml file for \"What is data engineering?\"\n\nAlways return valid YML.\n\nHere is an example:\n\n- name: Example YAML File\n  description: This is an example YAML file.\n  sections:\n    - title: Introduction\n      content: |\n        This is the introduction.\n    - title: Conclusion\n      content: |\n        This is the conclusion.\n\n----\n\n\n"
text = complete(prompt)
print(text)

data = yaml.load(text, Loader=yaml.FullLoader)
print(data)