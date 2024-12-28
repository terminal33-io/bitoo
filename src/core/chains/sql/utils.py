import re
import urllib
from dotenv import load_dotenv
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage

from app.config import database

def get_db() -> SQLDatabase:
    encoded_password = urllib.parse.quote_plus(database.db_password)
    mysql_uri = f"mysql+pymysql://{database.db_user}:{encoded_password}@{database.db_host}:{database.db_port}/{database.db_database}"

    return SQLDatabase.from_uri(mysql_uri)


def run_query(db: SQLDatabase, query: str, ):
    if query is not None:
        return QuerySQLDataBaseTool(db=db)
    return None

def extract_sql_query(
        message: AIMessage,
) -> str | None:
    """Parse the AI message."""
    regex_pattern = r"SELECT.*(?:&#39;|')?.*;"
    match = re.search(regex_pattern, message.content, re.DOTALL)
    return match.group(0) if match else None


# Returns table schema with examples
def generate_schema(table_name: list, skip_columns: list, column_comments: dict, examples_count: int = 3) -> str:
    pass

# Returns schema for all tables
def get_table_schema():
    pass

