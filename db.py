"""Acceso a la tabla items de Supabase."""
import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def listar_items(buscar: str | None = None) -> list[dict]:
    """Devuelve todos los items, opcionalmente filtrados por nombre."""
    consulta = supabase.table("items").select("*")
    if buscar:
        consulta = consulta.ilike("nombre", f"%{buscar}%")
    respuesta = consulta.order("id").execute()
    return respuesta.data


def buscar_item(item_id: int) -> dict | None:
    """Devuelve el item con ese id, o None si no existe."""
    respuesta = (
        supabase.table("items")
        .select("*")
        .eq("id", item_id)
        .limit(1)
        .execute()
    )
    return respuesta.data[0] if respuesta.data else None


def agregar_item(datos: dict) -> dict:
    """Inserta un item y devuelve la fila creada por Supabase."""
    respuesta = (
        supabase.table("items")
        .insert(datos)
        .select("*")
        .execute()
    )
    if not respuesta.data:
        raise RuntimeError("Supabase no devolvió el item insertado.")
    return respuesta.data[0]
