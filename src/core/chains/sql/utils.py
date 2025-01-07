import re
import urllib
from typing import Optional, List, Any

from dotenv import load_dotenv
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage
from sqlalchemy.sql.ddl import CreateTable
from sqlalchemy.sql.sqltypes import NullType

from app.config import database
import datetime


# TODO: Override SQLDatabase class to handle column exclusion and column specific comments via code
def get_db(include_tables: set[str]) -> SQLDatabase:
    encoded_password = urllib.parse.quote_plus(database.db_password)
    mysql_uri = f"mysql+pymysql://{database.db_user}:{encoded_password}@{database.db_host}:{database.db_port}/{database.db_database}"
    return SQLDatabase.from_uri(mysql_uri, {}, include_tables=include_tables)


def extract_sql_query(
        message: str,
) -> str | None:
    regex_pattern = r"SELECT.*(?:&#39;|')?.*;"
    match = re.search(regex_pattern, message, re.DOTALL)
    return match.group(0) if match else None



def get_current_financial_year():
    today = datetime.date.today()
    # Indian financial year runs from 1st April (month = 4) to 31st March (next year)
    if today.month >= 4:
        # From April (4) to December (12), the financial year starts this year and ends next year
        return f"{today.year}-{str(today.year + 1)[2:]}"
    else:
        # From January (1) to March (3), the financial year started last year and ends this year
        return f"{today.year - 1}-{str(today.year)[2:]}"
