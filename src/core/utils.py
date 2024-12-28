
from langchain_openai import ChatOpenAI

# Returns LLM Instance
def get_llm(callbacks=None, model_name=None):
    if callbacks is None:
        callbacks = []
    if model_name is None:
        model_name = "gpt-4o"

    return ChatOpenAI(
        temperature=0,
        model_name=model_name,
        callbacks=callbacks,
        verbose=True,
        model_kwargs={"seed": 1, "frequency_penalty": 0, "presence_penalty": 0},
    )
