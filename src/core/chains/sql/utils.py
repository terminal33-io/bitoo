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


# TODO: Override SQLDatabase class to handle column exclusion and comments via code
def get_db(include_tables: set[str]) -> SQLDatabase:
    encoded_password = urllib.parse.quote_plus(database.db_password)
    mysql_uri = f"mysql+pymysql://{database.db_user}:{encoded_password}@{database.db_host}:{database.db_port}/{database.db_database}"
    return SQLDatabase.from_uri(mysql_uri, {}, include_tables=include_tables)


class SQLDatabaseWrapper(SQLDatabase):
    def __init__(self):
        super().__init__()

    def get_table_info(self, table_names: Optional[List[str]] = None,
                       include_columns: Optional[List[str]] = None) -> str:
        """Get information about specified tables.

               Follows best practices as specified in: Rajkumar et al., 2022
               (https://arxiv.org/abs/2204.00498)

               If `sample_rows_in_table_info`, the specified number of sample rows will be
               appended to each table description. This can increase performance as
               demonstrated in the paper.
               """
        all_table_names = self.get_usable_table_names()
        if table_names is not None:
            missing_tables = set(table_names).difference(all_table_names)
            if missing_tables:
                raise ValueError(f"table_names {missing_tables} not found in database")
            all_table_names = table_names

        metadata_table_names = [tbl.name for tbl in self._metadata.sorted_tables]
        to_reflect = set(all_table_names) - set(metadata_table_names)
        if to_reflect:
            self._metadata.reflect(
                views=self._view_support,
                bind=self._engine,
                only=list(to_reflect),
                schema=self._schema,
            )

        meta_tables = [
            tbl
            for tbl in self._metadata.sorted_tables
            if tbl.name in set(all_table_names)
               and not (self.dialect == "sqlite" and tbl.name.startswith("sqlite_"))
        ]

        tables = []
        for table in meta_tables:
            if self._custom_table_info and table.name in self._custom_table_info:
                tables.append(self._custom_table_info[table.name])
                continue

            # Ignore JSON datatyped columns
            for k, v in table.columns.items():  # AttributeError: items in sqlalchemy v1
                if type(v.type) is NullType:
                    table._columns.remove(v)

            # Modify to include comments
            create_table = str(CreateTable(table).compile(self._engine))
            table_info = f"{create_table.rstrip()}"
            has_extra_info = (
                    self._indexes_in_table_info or self._sample_rows_in_table_info
            )
            if has_extra_info:
                table_info += "\n\n/*"
            if self._indexes_in_table_info:
                table_info += f"\n{self._get_table_indexes(table)}\n"
            if self._sample_rows_in_table_info:
                table_info += f"\n{self._get_sample_rows(table)}\n"
            if has_extra_info:
                table_info += "*/"
            tables.append(table_info)

        # check if comments need to be added to the tables, call generate schema
        tables.sort()
        final_str = "\n\n".join(tables)
        return final_str


# def run_query(db: SQLDatabase, query: str, ):
#     if query is not None:
#         return QuerySQLDataBaseTool(db=db)
#     return None
#
#
# def extract_sql_query(
#         message: AIMessage,
# ) -> str | None:
#     """Parse the AI message."""
#     regex_pattern = r"SELECT.*(?:&#39;|')?.*;"
#     match = re.search(regex_pattern, message.content, re.DOTALL)
#     return match.group(0) if match else None
