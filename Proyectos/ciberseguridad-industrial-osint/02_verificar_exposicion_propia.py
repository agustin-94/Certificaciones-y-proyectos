"""
02_verificar_exposicion_propia.py

Chequea qué ve Shodan (el motor de búsqueda de dispositivos conectados a
internet) sobre TU PROPIA IP pública — es decir, qué puertos/servicios de
tu propia red son visibles públicamente desde internet.

⚠️ IMPORTANTE — Uso ético y legal:
Este script SOLO consulta tu propia IP pública, obtenida automáticamente.
Shodan permite buscar información sobre CUALQUIER IP porque indexa datos
ya públicos, pero consultar o intentar acceder a dispositivos de terceros
sin autorización explícita es ilegal en la gran mayoría de las
jurisdicciones (incluida Argentina, bajo la Ley 26.388 de Delitos
Informáticos) y viola los términos de servicio de Shodan. Este script no
acepta una IP arbitraria por diseño: siempre resuelve y consulta la IP
pública de quien lo ejecuta.

Requiere una cuenta gratuita en https://www.shodan.io/ y tu API key
(Account → API Key). Anotala en la variable SHODAN_API_KEY o expórtala
como variable de entorno.
"""
import os
import sys
import requests

SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY", "TU_API_KEY_ACA")


def obtener_ip_publica():
    resp = requests.get("https://api.ipify.org?format=json", timeout=10)
    resp.raise_for_status()
    return resp.json()["ip"]


def consultar_shodan(ip):
    url = f"https://api.shodan.io/shodan/host/{ip}"
    resp = requests.get(url, params={"key": SHODAN_API_KEY}, timeout=15)

    if resp.status_code == 404:
        print(f"Shodan no tiene información indexada sobre {ip}.")
        print("Buena señal: significa que no hay servicios tuyos expuestos")
        print("y detectados en sus últimos rastreos.")
        return

    resp.raise_for_status()
    data = resp.json()

    print(f"\nInformación pública indexada por Shodan sobre {ip}:\n")
    print(f"Organización: {data.get('org', 'N/D')}")
    print(f"Ciudad/País:  {data.get('city', 'N/D')}, {data.get('country_name', 'N/D')}")
    print(f"Puertos abiertos detectados: {data.get('ports', [])}\n")

    for servicio in data.get("data", []):
        puerto = servicio.get("port")
        producto = servicio.get("product", "desconocido")
        version = servicio.get("version", "")
        print(f"  🔸 Puerto {puerto}: {producto} {version}")

    print(
        "\nSi ves puertos o servicios que no reconocés o que no deberían "
        "estar expuestos a internet (paneles de router, cámaras, servicios "
        "de administración remota), revisá la sección 'Mitigación' del "
        "README de este proyecto."
    )


if __name__ == "__main__":
    if SHODAN_API_KEY == "TU_API_KEY_ACA":
        print("Falta configurar tu API key de Shodan (variable SHODAN_API_KEY).")
        sys.exit(1)

    ip = obtener_ip_publica()
    print(f"Tu IP pública actual es: {ip}")
    consultar_shodan(ip)
