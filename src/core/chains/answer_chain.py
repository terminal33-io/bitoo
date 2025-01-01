from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    PromptTemplate,
)

from core.constants import ChatMessage
from core.utils import get_llm

_template = """You are an AI trained in Retail Store Data. Given the following user question, corresponding SQL query, SQL result provide a concise answer 
to the user's question.
Question: {question}
SQL Query: {query}
SQL Result: {result}

Use the following guidelines to answer the question:
- Keep the tone conversational and friendly.
- Format numbers into readable currency format as per Indian Rupees. Ceil the numbers to the nearest integer. Use crores and lakhs for large numbers.
- Format dates into readable format as per Indian Standard Time.
- Analyse the result data and try to provide a trend or analysis if possible.
- Provide suggestions on similar questoions related to the question asked.
- If Sql Result is None or empty, provide a response that "{SQL_RESULT_ERROR}"
"""
ANSWER_PROMPT = PromptTemplate(
    template=_template,
    input_variables=["question", "query", "result"],
    partial_variables={'SQL_RESULT_ERROR': ChatMessage.SQL_RESULT_ERROR}
)


def get_answer_chain():
    chain = ANSWER_PROMPT | get_llm() | StrOutputParser()
    return chain
