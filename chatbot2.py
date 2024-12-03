from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
#from langchain_core.messages import AIMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
model = ChatOpenAI(model="gpt-4o-mini")

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


# Define the function that calls the model
def call_model(state: MessagesState):
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# config a session/thread id
config = {"configurable": {"thread_id": "abc1"}}
config2 = {"configurable": {"thread_id": "abc2"}}

def query(text,config):
  input_messages = [HumanMessage(text)]
  output = app.invoke({"messages": input_messages}, config)
  return output

output = query("Hi! I'm Bob.",config)
output["messages"][-1].pretty_print()  # output contains all messages in state

output = query("What's my name?",config)
output["messages"][-1].pretty_print()