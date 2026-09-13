"""
01_consultar_cve.py

Consulta vulnerabilidades (CVE) publicadas en la NVD (National Vulnerability
Database, la base de datos pública y oficial de EE.UU.) relacionadas a un
producto o tecnología industrial (ej. "Modbus", "Siemens S7", "SCADA").

Esto es investigación 100% pasiva y legal: se consulta información YA
PUBLICADA públicamente por los fabricantes y organismos de seguridad, no se
escanea ni se accede a ningún sistema. Es el mismo tipo de consulta que
hace un analista de seguridad antes de aplicar parches en una planta.

API pública, sin necesidad de API key para uso liviano (con key se permite
más consultas por minuto): https://nvd.nist.gov/developers/vulnerabilities
"""
import sys
import time
import requests

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def buscar_cves(palabra_clave, resultados_max=10):
    params = {
        "keywordSearch": palabra_clave,
        "resultsPerPage": resultados_max,
    }
    resp = requests.get(NVD_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    vulnerabilidades = data.get("vulnerabilities", [])
    if not vulnerabilidades:
        print(f"No se encontraron CVEs para '{palabra_clave}'.")
        return

    print(f"\n{len(vulnerabilidades)} resultado(s) para '{palabra_clave}':\n")
    for item in vulnerabilidades:
        cve = item["cve"]
        cve_id = cve["id"]
        descripciones = cve.get("descriptions", [])
        descripcion_es = next(
            (d["value"] for d in descripciones if d["lang"] == "es"), None
        )
        descripcion = descripcion_es or next(
            (d["value"] for d in descripciones if d["lang"] == "en"), "(sin descripción)"
        )

        # Severidad (CVSS v3 si está disponible, si no v2)
        metrics = cve.get("metrics", {})
        severidad = "N/D"
        for clave in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            if clave in metrics:
                metrica = metrics[clave][0]
                # En CVSS v3.x, baseSeverity vive dentro de cvssData.
                # En CVSS v2, baseSeverity es un campo al mismo nivel que cvssData.
                severidad = metrica.get("cvssData", {}).get("baseSeverity") \
                    or metrica.get("baseSeverity", "N/D")
                break

        print(f"🔹 {cve_id}  [{severidad}]")
        print(f"   {descripcion[:280]}{'...' if len(descripcion) > 280 else ''}")
        print(f"   Más info: https://nvd.nist.gov/vuln/detail/{cve_id}\n")

        time.sleep(0.3)  # cortesía para no saturar la API pública


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python 01_consultar_cve.py \"<palabra clave>\"")
        print('Ejemplos: "Modbus", "Siemens S7", "SCADA", "Node-RED"')
        sys.exit(1)

    palabra_clave = " ".join(sys.argv[1:])
    buscar_cves(palabra_clave)
