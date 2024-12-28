from core.chains.sql.sql_chain import get_query_chain


async def answer_question(question: str):
    chain = get_query_chain()
    stream = chain.astream({"question": question})
    async for s in stream:
        yield s
