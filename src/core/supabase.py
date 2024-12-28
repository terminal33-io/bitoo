import os
import uuid
from functools import lru_cache
from typing import List
from uuid import uuid4

from dotenv import load_dotenv
from httpx import Timeout
from postgrest.types import CountMethod
from supabase import Client, create_client
from supabase._async.client import (
    AsyncClient,
    create_client as create_async_client,
)
from supabase.lib.client_options import ClientOptions

@lru_cache()
def get_client():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    options = ClientOptions(postgrest_client_timeout=Timeout(60))

    supabase: Client = create_client(url, key, options)
    return supabase

async def get_async_client() -> AsyncClient:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return await create_async_client(url, key)

def get_all_from_table(table_name: str) -> List[str]:
    supabase_client = get_client()
    row = supabase_client.table(table_name).select("*").execute()
    return row.data


def get_total_count(table_name: str):
    supabase = get_client()
    response = (
        supabase.table(table_name)
        .select("*", count=CountMethod.exact)
        .execute()
    )
    return response.count

def insert_chat(messages):
    supabase_client = get_client()
    supabase_client.table("chats").insert(
        {
            "user_id": 1,
            "session_id": str(uuid.uuid4()),
            "messages": messages,
        }
    ).execute()

def get_user(username: str):
    supabase_client = get_client()
    try:
        row = (
            supabase_client.table("users")
            .select("*")
            .eq("username", username)
            .single()
            .execute()
        )
        return row.data
    except Exception as e:
        print(e)
        return None


def insert_user(user):
    supabase_client = get_client()
    row = supabase_client.table("users").insert(user).execute()
    return row.data[0]


def get_chats(chat_id):
    supabase = get_client()
    try:
        row = (
            supabase.table("chats")
            .select("*")
            .eq("id", chat_id)
            .single()
            .execute()
        )
        return row.data
    except Exception as e:
        return None

