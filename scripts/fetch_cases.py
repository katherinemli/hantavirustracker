"""
Construye public/data/cases.json a partir de los casos investigados.

Estructura de cada caso: ver CASO_SCHEMA al final del archivo.
Para añadir un caso nuevo, agrégalo a CASOS_REGISTRADOS y ejecuta este script.
"""

import json
import os
from datetime import date, datetime

# ── Datos investigados ────────────────────────────────────────────────────────

CASOS_REGISTRADOS = [
    {
        "id": 1,
        "region": "Los Lagos",
        "comuna": "Puerto Montt",
        "fecha_inicio_sintomas": "2025-11-03",
        "fecha_confirmacion": "2025-11-07",
        "sexo": "M",
        "edad": 34,
        "exposicion": "Trabajo agrícola en zona boscosa",
        "desenlace": "recuperado",
        "fuente": "Boletín ISP N°47 2025",
    },
    {
        "id": 2,
        "region": "Aysén",
        "comuna": "Coyhaique",
        "fecha_inicio_sintomas": "2025-12-14",
        "fecha_confirmacion": "2025-12-18",
        "sexo": "F",
        "edad": 28,
        "exposicion": "Limpieza de bodega con presencia de roedores",
        "desenlace": "recuperado",
        "fuente": "Boletín ISP N°51 2025",
    },
    {
        "id": 3,
        "region": "La Araucanía",
        "comuna": "Temuco",
        "fecha_inicio_sintomas": "2026-01-22",
        "fecha_confirmacion": "2026-01-26",
        "sexo": "M",
        "edad": 51,
        "exposicion": "Actividad forestal",
        "desenlace": "hospitalizado",
        "fuente": "Boletín ISP N°04 2026",
    },
]

# ── Lógica de construcción ───────────────────────────────────────────────────

DESENLACE_PESO = {"hospitalizado": 0, "recuperado": 1, "fallecido": 2}


def build_summary(casos: list) -> dict:
    confirmed = len(casos)
    fatalities = sum(1 for c in casos if c["desenlace"] == "fallecido")
    active_regions = len({c["region"] for c in casos if c["desenlace"] == "hospitalizado"})
    return {
        "confirmed": confirmed,
        "fatalities": fatalities,
        "fatality_rate": round(fatalities / confirmed, 4) if confirmed else 0,
        "active_regions": active_regions,
    }


def build_payload(casos: list) -> dict:
    sorted_cases = sorted(
        casos,
        key=lambda c: (DESENLACE_PESO.get(c["desenlace"], 99), c["fecha_confirmacion"]),
        reverse=True,
    )
    return {
        "updated_at": date.today().isoformat(),
        "source": "MINSAL / ISP Chile — datos investigados manualmente",
        "summary": build_summary(casos),
        "cases": sorted_cases,
    }


def main() -> None:
    payload = build_payload(CASOS_REGISTRADOS)

    out_path = os.path.join(
        os.path.dirname(__file__), "..", "public", "data", "cases.json"
    )
    out_path = os.path.normpath(out_path)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"[fetch_cases] {len(CASOS_REGISTRADOS)} casos → {out_path}")


if __name__ == "__main__":
    main()


# ── CASO_SCHEMA (referencia) ─────────────────────────────────────────────────
# {
#   "id":                   int        — correlativo único
#   "region":               str        — región administrativa de Chile
#   "comuna":               str
#   "fecha_inicio_sintomas": "YYYY-MM-DD"
#   "fecha_confirmacion":    "YYYY-MM-DD"
#   "sexo":                 "M" | "F"
#   "edad":                 int
#   "exposicion":           str        — descripción libre del factor de exposición
#   "desenlace":            "recuperado" | "hospitalizado" | "fallecido"
#   "fuente":               str        — boletín ISP o SEREMI de referencia
# }
