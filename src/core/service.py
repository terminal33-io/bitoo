from operator import itemgetter

from langchain_community.tools import QuerySQLDataBaseTool
from langchain_core.runnables import RunnablePassthrough

from core.chains.answer_chain import get_answer_chain
from core.chains.sql.sql_chain import get_query_chain
from core.chains.sql.utils import get_db, extract_sql_query


async def answer_question(question: str):
    # invoke only query chain to see the query
    # both full chain with answer and query covered
    # depends on the UI needs if we need to stream query from intermediate chain

    # Tables to be included for query generation
    include_tables = {"rpt_customer_profile", "rpt_order_details_report"}
    db = get_db(include_tables)
    query_chain = get_query_chain(db)
    answer_chain = get_answer_chain()

    full_chain = (RunnablePassthrough.assign(
        query_chain=query_chain
    ) | RunnablePassthrough.assign(
        query=lambda x: extract_sql_query(itemgetter("query_chain")(x))
    ) | RunnablePassthrough.assign(
        result=itemgetter("query") | QuerySQLDataBaseTool(db=db)
    ) | answer_chain)

    stream = full_chain.astream({"question": question})
    async for s in stream:
        yield s
