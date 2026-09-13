"""
03_escaneo_red_local.py

Escanea la red LOCAL indicada (por defecto, la de tu propia casa/laboratorio)
usando nmap, para inventariar qué dispositivos y puertos están expuestos
DENTRO de tu propia red — el primer paso de cualquier auditoría de
seguridad industrial: no podés proteger lo que no sabés que tenés
conectado.

⚠️ IMPORTANTE — Uso ético y legal:
Correr esto SOLO contra redes que administrás o para las que tenés
autorización explícita por escrito (ej. la red de un cliente, con permiso
firmado). Escanear redes ajenas sin autorización es ilegal. Por defecto,
este script apunta a un rango de red privado (RFC 1918) típico de un
router hogareño; cambiá RED_OBJETIVO solo por otra red privada propia.

Requiere Kali Linux (o cualquier distro) con nmap instalado, y la
librería python-nmap:
    sudo apt install nmap
    pip install python-nmap
"""
import sys
import nmap

# Cambiar solo por un rango de TU propia red (ver tu IP con `ip a` o `ifconfig`)
RED_OBJETIVO = "192.168.0.0/24"


def escanear(red):
    scanner = nmap.PortScanner()
    print(f"Escaneando {red} (puede tardar uno o dos minutos)...\n")

    # -sn: solo descubrimiento de hosts (ping scan), no escanea puertos.
    # Es el modo más liviano y menos intrusivo para un primer inventario.
    scanner.scan(hosts=red, arguments="-sn")

    hosts_activos = scanner.all_hosts()
    print(f"Dispositivos encontrados en la red: {len(hosts_activos)}\n")

    for host in hosts_activos:
        estado = scanner[host].state()
        nombre = scanner[host].hostname() or "(sin nombre resuelto)"
        print(f"  🔹 {host}  —  {nombre}  [{estado}]")

    print(
        "\nPara un inventario más detallado de puertos/servicios de UN "
        "dispositivo puntual de tu red (por ejemplo tu propio router o un "
        "PLC/gateway de laboratorio), corré por separado:\n"
        "    nmap -sV <ip_del_dispositivo>\n"
        "sobre esa IP específica, una vez identificada acá."
    )


if __name__ == "__main__":
    red = sys.argv[1] if len(sys.argv) > 1 else RED_OBJETIVO
    escanear(red)
