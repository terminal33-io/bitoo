from typing import Union, Dict, Any, Optional

from langchain.chains.sql_database.prompt import SQL_PROMPTS
from langchain_community.utilities import SQLDatabase
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, Runnable
from core.chains.sql.callback import SqlCallbackHandler
from core.chains.sql.prompt import PROMPT
from core.chains.sql.utils import extract_sql_query, get_db
from core.utils import get_llm
from langchain.chains.sql_database.query import SQLInputWithTables, SQLInput


# TODO:
# - Add tool to execute query
# - Add query checker and results checker
# - Agent based query chain - Discuss with #exhale
def get_query_chain():
    include_tables = {"rpt_customer_profile", "rpt_order_details_report"}
    db = get_db(include_tables)
    # callbacks = [SqlCallbackHandler(chat_id, message_id)]
    llm = get_llm()
    prompt = PROMPT
    return create_sql_query_chain(llm, db, prompt, k=20)


# overriden default langchain function
def create_sql_query_chain(
    llm: BaseLanguageModel,
    db: SQLDatabase,
    prompt: Optional[BasePromptTemplate] = None,
    k: int = 5,
) -> Runnable[Union[SQLInput, SQLInputWithTables, Dict[str, Any]], str]:
    if prompt is not None:
        prompt_to_use = prompt
    elif db.dialect in SQL_PROMPTS:
        prompt_to_use = SQL_PROMPTS[db.dialect]
    else:
        prompt_to_use = PROMPT
    if {"input", "top_k", "table_info"}.difference(
        prompt_to_use.input_variables + list(prompt_to_use.partial_variables)
    ):
        raise ValueError(
            f"Prompt must have input variables: 'input', 'top_k', "
            f"'table_info'. Received prompt with input variables: "
            f"{prompt_to_use.input_variables}. Full prompt:\n\n{prompt_to_use}"
        )
    if "dialect" in prompt_to_use.input_variables:
        prompt_to_use = prompt_to_use.partial(dialect=db.dialect)

    inputs = {
        "input": lambda x: x["question"] + "\nSQLQuery: ",
        "table_info": lambda x: db.get_table_info(
            table_names=x.get("table_names_to_use")
        ),
    }
    return (
        RunnablePassthrough.assign(**inputs)  # type: ignore
        | (
            lambda x: {
                k: v
                for k, v in x.items()
                if k not in ("question", "table_names_to_use")
            }
        )
        | prompt_to_use.partial(top_k=str(k))
        | llm.bind(stop=["\nSQLResult:"])
        | extract_sql_query
    )
