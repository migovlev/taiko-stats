import requests

from config import THUNDERSKILL_URL


def download_data():
    """Descarga el JSON de ThunderSkill."""

    response = requests.get(THUNDERSKILL_URL, timeout=30)
    response.raise_for_status()

    return response.json()


def get_squad_info(data):
    """Devuelve la información del escuadrón."""

    return data["squadinfo"]


def get_players(data):
    """Devuelve la lista de jugadores."""

    return data["players"]