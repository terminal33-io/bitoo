from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    PromptTemplate,
)

from src.core.constants import ChatMessage
from src.core.utils import get_llm


_template = """You are an AI trained in Retail Store Data.

Given the following user question, SQL query, and SQL results, 
1. Keep the tone conversational and friendly.
2. Format currency values into Indian currency format.
3. Format dates into readable format as per Indian Standard Time.
4. Analyse the result data and try to provide a trend or analysis if possible.
5. Provide suggestions on similar questions related to the question asked.
6. If Sql Result is None or empty, provide a response that "{SQL_RESULT_ERROR}"

Question: {question}
SQL Query: {query}
SQL Result: {result}

"""
ANSWER_PROMPT = PromptTemplate(
    template=_template,
    input_variables=["question", "query", "result"],
    partial_variables={'SQL_RESULT_ERROR': ChatMessage.SQL_RESULT_ERROR}
)


def get_answer_chain():
    llm = get_llm()
    chain = ANSWER_PROMPT | llm | StrOutputParser()
    return chain
