import requests

THUNDERSKILL_URL = "https://thunderskill.com/en/squad/%5BTAIKO%5D/export/json"

print("Descargando datos de ThunderSkill...")

response = requests.get(THUNDERSKILL_URL, timeout=30)
response.raise_for_status()

data = response.json()

print("\n=== INFORMACIÓN DEL ESCUADRÓN ===\n")

# Mostrar todas las claves disponibles
import json

print("\n=== SQUAD INFO ===\n")
print(json.dumps(data["squadinfo"], indent=4, ensure_ascii=False))

print("\n=== PRIMER JUGADOR ===\n")
print(json.dumps(data["players"][0], indent=4, ensure_ascii=False))