from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from langchain.schema.runnable.config import RunnableConfig
import chainlit as cl

load_dotenv()

system_message_content = """
You are an integration expert, especially on XSLT transformation from Source XML to Target XML, also you can write and execute Python code. Whenever you provide an xslt or python code please enclose it in triple backticks, if the request to generate xslt then generate xslt only, don't mix it with python. End users will go through one by one field on the target xml structure and need your help to generate XSLT to transform data from source xml field.
If the user mentions a term that you don't know, then ask the user which field it is. Example: if the user enters "sales order" and if you don't know which field is for "sales order" then ask the user to enter an xpath for it.
Source XML: <?xml version="1.0" encoding="UTF-8"?><ns0:FlightBookingOrderConfirmation xmlns:ns0="http://sap.com/xi/XI/Demo/Airline"><AgencyData><AgencyID>00000110</AgencyID><OrderNumber>00000023</OrderNumber><ItemNumber>01</ItemNumber><OrderType>Single</OrderType></AgencyData><BookingStatus>B</BookingStatus><BookingID><AirlineID>LH</AirlineID><BookingNumber>00004711</BookingNumber></BookingID></ns0:FlightBookingOrderConfirmation>
Target XML: <?xml version="1.0" encoding="UTF-8"?><ns0:BookingOrderConfirmation xmlns:ns0="http://sap.com/xi/XI/Demo/Agency"><AgencyID>00000110</AgencyID><OrderNumber>00000023</OrderNumber><BookingStatus>B</BookingStatus><BookingID><AirlineID>LH</AirlineID><BookingNumber>00004711</BookingNumber></BookingID></ns0:BookingOrderConfirmation>
"""

prompt_template = ChatPromptTemplate([
    ("system", system_message_content),
    MessagesPlaceholder("messages")
])

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define the function that calls the model
def call_model(state: MessagesState):    
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": response}

# Define a new graph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("model", call_model)
graph_builder.add_edge(START, "model")

# Add memory
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# config a session/thread id
#config = {"configurable": {"thread_id": "abc1"}}

@cl.on_message
async def query(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    for chunk, metadata in graph.stream(
        {"messages": [HumanMessage(content=msg.content)]},
        config=RunnableConfig(callbacks=[cb], **config),
        stream_mode="messages",
    ):
        if isinstance(chunk, AIMessage):
            await final_answer.stream_token(chunk.content)

    await final_answer.send()
