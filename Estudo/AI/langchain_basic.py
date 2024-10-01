from langchain_openai.chat_models import ChatOpenAI

chat = ChatOpenAI(openai_api_key="...")

print(chat.invoke("Hello, how are you?"))