"""
Construye public/data/cases.json con estructura global para el brote MV Hondius.
Fuentes de referencia: WHO, CDC, ECDC, ProMED-mail.

Para añadir o corregir un caso: edita CASOS o NEWS_FEED y vuelve a ejecutar.
"""

import json
import os
from datetime import date

# ── Ruta estimada del MV Hondius ─────────────────────────────────────────────
# Coordenadas [lat, lng] desde Ushuaia hacia Rotterdam vía el Atlántico.
SHIP_ROUTE = [
    [-54.80, -68.30],   # Ushuaia, Argentina
    [-57.00, -60.00],   # Paso Drake
    [-54.25, -36.50],   # Georgia del Sur
    [-51.70, -59.52],   # Islas Malvinas
    [-34.90, -56.20],   # Montevideo, Uruguay
    [-22.90, -43.17],   # Río de Janeiro, Brasil
    [ 14.93, -23.51],   # Cabo Verde
    [ 38.72,  -9.14],   # Lisboa, Portugal
    [ 51.90,   4.48],   # Rotterdam, Países Bajos
]

# ── Casos registrados ─────────────────────────────────────────────────────────
# status: "Confirmed" | "Monitoring"
CASOS = [
    {
        "id": 1,
        "country": "Argentina",
        "region": "Tierra del Fuego",
        "lat": -54.80,
        "lng": -68.30,
        "status": "Confirmed",
        "pathogen": "Hantavirus Andes (ANDV)",
        "date": "2026-04-15",
        "source_url": "https://www.who.int/emergencies/disease-outbreak-news",
        "source_agency": "WHO",
        "notes": "Tripulante del MV Hondius. Exposición confirmada en zona endémica.",
    },
    {
        "id": 2,
        "country": "Chile",
        "region": "Magallanes",
        "lat": -53.16,
        "lng": -70.91,
        "status": "Confirmed",
        "pathogen": "Hantavirus Andes (ANDV)",
        "date": "2026-04-18",
        "source_url": "https://www.who.int/emergencies/disease-outbreak-news",
        "source_agency": "WHO",
        "notes": "Pasajero con historial de contacto en área subantártica.",
    },
    {
        "id": 3,
        "country": "Netherlands",
        "region": "Rotterdam",
        "lat": 51.90,
        "lng": 4.48,
        "status": "Confirmed",
        "pathogen": "Hantavirus Andes (ANDV)",
        "date": "2026-04-28",
        "source_url": "https://www.ecdc.europa.eu/en/publications-data/rapid-risk-assessments",
        "source_agency": "ECDC",
        "notes": "Pasajero repatriado. Primer caso confirmado en Europa.",
    },
    {
        "id": 4,
        "country": "Germany",
        "region": "Hamburg",
        "lat": 53.55,
        "lng": 10.00,
        "status": "Monitoring",
        "pathogen": "Hantavirus Andes (ANDV)",
        "date": "2026-04-30",
        "source_url": "https://www.ecdc.europa.eu/en/news-events",
        "source_agency": "ECDC",
        "notes": "Contactos cercanos bajo vigilancia activa. Sin síntomas al momento.",
    },
    {
        "id": 5,
        "country": "United Kingdom",
        "region": "London",
        "lat": 51.51,
        "lng": -0.13,
        "status": "Monitoring",
        "pathogen": "Hantavirus Andes (ANDV)",
        "date": "2026-04-30",
        "source_url": "https://www.gov.uk/government/organisations/uk-health-security-agency",
        "source_agency": "UKHSA",
        "notes": "Tres pasajeros bajo monitoreo. UKHSA coordina con ECDC.",
    },
    {
        "id": 6,
        "country": "France",
        "region": "Île-de-France",
        "lat": 48.85,
        "lng": 2.35,
        "status": "Monitoring",
        "pathogen": "Hantavirus Andes (ANDV)",
        "date": "2026-05-01",
        "source_url": "https://www.ecdc.europa.eu/en/news-events",
        "source_agency": "ECDC",
        "notes": "Pasajeros identificados. Autoridades sanitarias en coordinación con ECDC.",
    },
    {
        "id": 7,
        "country": "United States",
        "region": "New York",
        "lat": 40.71,
        "lng": -74.01,
        "status": "Monitoring",
        "pathogen": "Hantavirus Andes (ANDV)",
        "date": "2026-05-02",
        "source_url": "https://www.cdc.gov/hantavirus",
        "source_agency": "CDC",
        "notes": "Pasajero estadounidense identificado. CDC emite guía de seguimiento.",
    },
    {
        "id": 8,
        "country": "Belgium",
        "region": "Brussels",
        "lat": 50.85,
        "lng": 4.35,
        "status": "Monitoring",
        "pathogen": "Hantavirus Andes (ANDV)",
        "date": "2026-05-03",
        "source_url": "https://www.ecdc.europa.eu/en/news-events",
        "source_agency": "ECDC",
        "notes": "Caso bajo evaluación epidemiológica por Sciensano.",
    },
]

# ── Feed de noticias ──────────────────────────────────────────────────────────
NEWS_FEED = [
    {
        "date": "2026-05-10",
        "title": "WHO: Multi-country alert — ANDV cases linked to MV Hondius expedition cruise",
        "agency": "WHO",
        "url": "https://www.who.int/emergencies/disease-outbreak-news",
        "langs": ["en", "fr", "es"],
    },
    {
        "date": "2026-05-08",
        "title": "ECDC Rapid Risk Assessment: Hantavirus Andes in returning travellers from South America",
        "agency": "ECDC",
        "url": "https://www.ecdc.europa.eu/en/publications-data/rapid-risk-assessments",
        "langs": ["en"],
    },
    {
        "date": "2026-05-07",
        "title": "OPS/PAHO: Alerta epidemiológica — Hantavirus Andes (ANDV) en viajeros internacionales",
        "agency": "PAHO",
        "url": "https://www.paho.org/es/alertas-y-respuestas-por-paises",
        "langs": ["es"],
    },
    {
        "date": "2026-05-05",
        "title": "CDC Travel Health Notice: Hantavirus (ANDV) Risk — Patagonia and Sub-Antarctic",
        "agency": "CDC",
        "url": "https://www.cdc.gov/hantavirus",
        "langs": ["en"],
    },
    {
        "date": "2026-05-03",
        "title": "ProMED-mail: HANTAVIRUS PULMONARY SYNDROME — MULTI-COUNTRY (04): MV Hondius link",
        "agency": "ProMED",
        "url": "https://promedmail.org",
        "langs": ["en"],
    },
    {
        "date": "2026-04-28",
        "title": "ECDC: First ANDV case confirmed in Europe — Netherlands reports repatriated cruise passenger",
        "agency": "ECDC",
        "url": "https://www.ecdc.europa.eu/en/news-events",
        "langs": ["en", "fr"],
    },
]


# ── Construcción del payload ──────────────────────────────────────────────────

def build_summary(casos: list) -> dict:
    confirmed  = sum(1 for c in casos if c["status"] == "Confirmed")
    monitoring = sum(1 for c in casos if c["status"] == "Monitoring")
    countries  = len({c["country"] for c in casos})
    return {
        "confirmed":       confirmed,
        "monitoring":      monitoring,
        "countries_alert": countries,
    }


def main() -> None:
    payload = {
        "updated_at": date.today().isoformat(),
        "outbreak":   "MV Hondius — Hantavirus Andes (ANDV)",
        "source":     "WHO / CDC / ECDC / ProMED-mail",
        "summary":    build_summary(CASOS),
        "ship_route": SHIP_ROUTE,
        "cases":      CASOS,
        "news_feed":  NEWS_FEED,
    }

    out = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "public", "data", "cases.json")
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)

    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"[fetch_cases] {len(CASOS)} casos · {payload['summary']} → {out}")


if __name__ == "__main__":
    main()
