"""
02_verificar_exposicion_propia.py

Chequea qué ve Shodan sobre TU PROPIA IP pública — es decir, qué puertos y
servicios de tu propia red son visibles públicamente desde internet.

Usa InternetDB (https://internetdb.shodan.io), la API gratuita de Shodan
pensada exactamente para este caso de uso: consultar la exposición de una
IP puntual sin necesitar cuenta, API key ni créditos de consulta (a
diferencia de la API completa /shodan/host/, que sí requiere créditos aún
en cuentas registradas).

⚠️ IMPORTANTE — Uso ético y legal:
Este script SOLO consulta tu propia IP pública, obtenida automáticamente.
Shodan permite consultar información sobre CUALQUIER IP porque indexa datos
ya públicos, pero usar esa información para acceder a dispositivos de
terceros sin autorización explícita es ilegal en la gran mayoría de las
jurisdicciones (incluida Argentina, bajo la Ley 26.388 de Delitos
Informáticos) y viola los términos de servicio de Shodan. Este script no
acepta una IP arbitraria por diseño: siempre resuelve y consulta la IP
pública de quien lo ejecuta.
"""
import requests

INTERNETDB_URL = "https://internetdb.shodan.io/{ip}"


def obtener_ip_publica():
    resp = requests.get("https://api.ipify.org?format=json", timeout=10)
    resp.raise_for_status()
    return resp.json()["ip"]


def consultar_shodan(ip):
    resp = requests.get(INTERNETDB_URL.format(ip=ip), timeout=15)

    if resp.status_code == 404:
        print(f"Shodan no tiene información indexada sobre {ip}.")
        print("Buena señal: significa que no hay servicios tuyos expuestos")
        print("y detectados en sus últimos rastreos.")
        return

    resp.raise_for_status()
    data = resp.json()

    puertos = data.get("ports", [])
    print(f"\nInformación pública indexada por Shodan sobre {ip}:\n")
    print(f"Puertos abiertos detectados: {puertos or '(ninguno)'}")

    hostnames = data.get("hostnames", [])
    if hostnames:
        print(f"Hostnames asociados: {hostnames}")

    cves = data.get("vulns", [])
    if cves:
        print(f"\n⚠️  CVEs asociadas a servicios detectados en esta IP:")
        for cve in cves:
            print(f"  🔸 {cve}  →  https://nvd.nist.gov/vuln/detail/{cve}")
    else:
        print("\nNo hay CVEs conocidas asociadas a esta IP en este momento.")

    print(
        "\nSi ves puertos o servicios que no reconocés o que no deberían "
        "estar expuestos a internet (paneles de router, cámaras, servicios "
        "de administración remota), revisá la sección 'Mitigación' del "
        "README de este proyecto."
    )


if __name__ == "__main__":
    ip = obtener_ip_publica()
    print(f"Tu IP pública actual es: {ip}")
    consultar_shodan(ip)
