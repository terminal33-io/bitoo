from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    PromptTemplate,
)

from src.core.constants import ChatMessage
from src.core.utils import get_llm

_template = """You are an AI trained in Retail Store Data. Given the following user question, corresponding SQL query, SQL result provide a concise answer 
to the user's question.
Question: {question}
SQL Query: {query}
SQL Result: {result}

Use the following guidelines to answer the question:
1. Keep the tone conversational and friendly.
2. **Format numbers into readable currency format** in Indian Rupees:
   - Use `ceil` to round up to the nearest integer.
   - Convert amounts ≥ 1,00,00,000 (1e7) to Crores and amounts ≥ 1,00,000 (1e5) but < 1,00,00,000 to Lakhs.
   - Otherwise, keep amounts in normal rupees format.
   - Donot make error in this conversion, this is very important.
3. Format dates into readable format as per Indian Standard Time.
4. Analyse the result data and try to provide a trend or analysis if possible.
5. Provide suggestions on similar questoions related to the question asked.
6. If Sql Result is None or empty, provide a response that "{SQL_RESULT_ERROR}"

To format numbers correctly, use the Indian numbering system:
- 1 Lakh = 1,00,000
- 1 Crore = 1,00,00,000

For example, if you have ₹73,45,600, convert it to "73.46 Lakhs" (using ceil or round as appropriate).
If you have ₹3,45,67,891, convert it to "3.46 Crores".

Finally, provide a concise and helpful answer.
"""
ANSWER_PROMPT = PromptTemplate(
    template=_template,
    input_variables=["question", "query", "result"],
    partial_variables={'SQL_RESULT_ERROR': ChatMessage.SQL_RESULT_ERROR}
)


def get_answer_chain():
    chain = ANSWER_PROMPT | get_llm() | StrOutputParser()
    return chain
