# langchain03chatbot
This is to generate XSLT to transfrom source XML to expected target XML.

A chatbot with:
- LangChain 03
- LangGraph
- GUI with Chainlit

### Install
python3 -m venv .venv\
source .venv/bin/activate\
pip install -r requirements.txt

#### OpenAI Key
create an file .env
```
OPENAI_API_KEY='your key here'
```
### Run
chainlit run chatbot2_chainlit.py -w

### Try prompts
. Show me the source XML.\
. Show me the target XML.\
. get the xpath of agency and then generate xslt to transform it from the source to the target field, xslt is for only agency and no other fields.\
. get the xpath of order number and then generate xslt to transform it from the source to the target field, xslt is for only agency and no other fields.\
. how many xslt did we generated?\
[
 .user: get the xpath of sales order and then generate xslt to transform it from the source xml to the target xml. 
 .AI: provide your xpath of "Sales Order"
 .user: provide any xpath.
 .user: show me the xpath of sales order.
]\
. generate xsl to transfrom the source xml to the target xml.\
. write a python script to test the xslt and the source xml, and execute it then show me the output.