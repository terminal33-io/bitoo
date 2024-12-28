from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# Improve prompt for Time Constraint
# Escape Special Characters: Escape ' with &#39; for values in the generated query.
# Some important facts related to query generation:

_mysql_prompt = """You are an AI trained in MySQL and Retail Store Data. Your role is to analyze user questions and create accurate, syntactically correct SQL queries to answer them. Follow these guidelines:

Analyze the Question: Understand the specific data the user is asking for.

Craft the SQL Query:
    - Result Limit: Default to a maximum of {top_k} results using the LIMIT clause, unless specified otherwise by the user.
    - Column Selection: Only include necessary columns in your query, using backticks () for each column name. Avoid using SELECT *`.
    - Table and Column Reference: Ensure accuracy in referencing columns and tables; only query existing columns and be mindful of their respective tables.
    - Current Date Queries: Use CURDATE() for queries involving today's date.

Focus on precision and efficiency in your query to ensure it meets the user's data retrieval needs. Do not explain your answer.
"""

# PROMPT_SUFFIX = """Only use the following tables:
# {table_info}
#
# Question: {input}
# """
#
# example_prompt = PromptTemplate.from_template(
#     "Below are a number of examples of questions and their corresponding SQL queries:\nUser input: {input}\nSQL query: {query}"
# )
# examples = [
# ]

MYSQL_PROMPT = PromptTemplate(
    # examples=examples,
    # example_prompt=example_prompt,
    prefix=_mysql_prompt,
    # suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k", "location_id"],
)
