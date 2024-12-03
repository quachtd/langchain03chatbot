from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

#model.invoke([HumanMessage(content="Hi! I'm Bod")])
response = model.invoke(
  [
    HumanMessage(content="Hi! I'm Bod"),
    AIMessage(content="Hello Bob! How can I assist you today?"),
    HumanMessage(content="What's my name?")
  ]
)
print(response.content)