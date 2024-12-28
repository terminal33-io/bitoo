import re
from typing import Any

from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.outputs import LLMResult


class SqlCallbackHandler(AsyncCallbackHandler):
    def __init__(self):
        pass
        # self.chat_id = chat_id
        # self.message_id = message_id

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        generations = response.generations
        sql_query = None
        if generations and generations[0]:
            first_chunk = generations[0][0]
            text = first_chunk.text.strip()
            regex_pattern = r"SELECT.*?;"
            match = re.search(regex_pattern, text, re.DOTALL)
            if match:
                sql_query = match.group(0)

        # TODO: store the generated query