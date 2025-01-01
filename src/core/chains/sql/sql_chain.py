from src.core.chains.sql.callback import SqlCallbackHandler
from src.core.chains.sql.prompt import PROMPT
from src.core.utils import get_llm
from langchain.chains.sql_database.query import create_sql_query_chain


# TODO: change chain to langchain agent
def get_query_chain(db):
    callbacks = [SqlCallbackHandler()]
    llm = get_llm(callbacks=callbacks)
    return create_sql_query_chain(llm, db, PROMPT, k=20)
