from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    PromptTemplate,
)

from core.constants import ChatMessage
from core.utils import get_llm

# TODO: Modify prompt for better answer, to show trends and analysis
_template = """Given the following user question, corresponding SQL query, SQL result provide a concise and to the point answer 
to the user's question.
Question: {question}
SQL Query: {query}
SQL Result: {result}

If Sql Result is None or empty, provide a response that "{SQL_RESULT_ERROR}"
"""
ANSWER_PROMPT = PromptTemplate(
    template=_template,
    input_variables=["question", "query", "result"],
    partial_variables={'SQL_RESULT_ERROR': ChatMessage.SQL_RESULT_ERROR}
)


def get_answer_chain():
    chain = ANSWER_PROMPT | get_llm() | StrOutputParser()
    return chain
