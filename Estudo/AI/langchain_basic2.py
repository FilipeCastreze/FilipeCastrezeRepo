from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

chat = ChatOpenAI(openai_api_key="")

text = "What would be a good company name for a company that makes colorful socks?"
messages = [HumanMessage(content=text)]
result = chat.invoke(messages)

print(result.content)

#Inserting the SystemMessage instead of a HumanMessage

messages = [SystemMessage(content=text)]
chat(messages)

print(result.content)