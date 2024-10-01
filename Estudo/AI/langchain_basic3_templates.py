from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)

chat = ChatOpenAI(openai_api_key="")

template = "What would be a good company name for a {company_description}. List 3 company names that you like. Make sure that the list is a numbered list."

system_message_prompt = SystemMessagePromptTemplate.from_template(template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])

# Get a chat completion from the formatted messages
result = chat.invoke(
    chat_prompt.format_prompt(company_description="Data engineering").to_messages()
)

print(result.content)