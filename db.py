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


def listar_libros(titulo: str | None = None) -> list[dict]:
    """Devuelve todos los libros, opcionalmente filtrados por titulo."""
    consulta = supabase.table("libros_tp").select("*")
    if titulo:
        consulta = consulta.ilike("titulo", f"%{titulo}%")
    respuesta = consulta.order("id_libro").execute()
    return respuesta.data


def buscar_libros(libro_id: int) -> dict | None:
    """Devuelve el item con ese id, o None si no existe."""
    respuesta = (
        supabase.table("libros_tp")
        .select("*")
        .eq("id", libro_id)
        .limit(1)
        .execute()
    )
    return respuesta.data[0] if respuesta.data else None


def agregar_libros(datos: dict) -> dict:
    """Inserta un libro y devuelve la fila creada por Supabase."""
    respuesta = (
        supabase.table("libros_tp")
        .insert(datos)
        .select("*")
        .execute()
    )
    if not respuesta.data:
        raise RuntimeError("Supabase no devolvió el libro insertado.")
    return respuesta.data[0]


def actualizar_libros(item_id: int, datos: dict) -> dict | None:
    """Reemplaza los datos enviados del libro y devuelve la fila, o None si no existe."""
    respuesta = (
        supabase.table("libros_tp")
        .update(datos)
        .eq("id_libro", item_id)
        .select("*")
        .execute()
    )
    return respuesta.data[0] if respuesta.data else None


def borrar_libros(item_id: int) -> dict | None:
    """Elimina el libro con ese id y devuelve la fila, o None si no existe."""
    respuesta = (
        supabase.table("libros_tp")
        .delete()
        .eq("id_libro", item_id)
        .select("*")
        .execute()
    )
    return respuesta.data[0] if respuesta.data else None
