from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from core.chains.sql.callback import SqlCallbackHandler
from core.chains.sql.prompt import PROMPT
from core.chains.sql.utils import get_table_schema, extract_sql_query
from core.utils import get_llm


# TODO:
# - Add tool to execute query
# - Add query checker and results checker
# - Agent based query chain - Discuss with #exhale
def get_query_chain(chat_id: str, message_id: str):
    inputs = {
        "input": lambda x: x["question"] + "\nSQLQuery: ",
        "table_info": lambda x: get_table_schema(),
    }
    sql_llm = get_llm(callbacks=[SqlCallbackHandler(chat_id, message_id)])

    query_chain = (
            RunnablePassthrough.assign(**inputs)
            | PROMPT.partial(top_k=str(20))
            | sql_llm.bind(stop=["\nSQLResult:"])
            | extract_sql_query
    )

    return query_chain


