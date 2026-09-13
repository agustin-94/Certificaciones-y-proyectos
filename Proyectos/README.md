# Stack de monitoreo con Docker — Node-RED + InfluxDB + Grafana

Proyecto de práctica hecho al finalizar el curso **["Virtualización y
Docker"](https://escuela.ingelearn.com/course/virtualizacion-y-docker)** de
Ingelearn (fundamentos de virtualización con VMs, snapshots y redes;
virtualización por contenedores con Docker y Podman; despliegue de
servicios como Node-RED, Grafana e InfluxDB).

Levanta con `docker-compose` un stack completo de monitoreo industrial:
un sensor simulado (temperatura y presión de un tanque) genera datos en
Node-RED, que se escriben en InfluxDB como serie temporal y se visualizan
en un dashboard de Grafana — el mismo patrón que se usa para monitoreo real
de planta (SCADA/IT-OT), pero corriendo en contenedores en vez de en
hardware dedicado.

## El pipeline corriendo en vivo

**Node-RED** generando y enviando lecturas simuladas a InfluxDB cada 5 segundos:

![Flow de Node-RED con datos en vivo](ejemplos/docker-stack-grafana1.png)

**Grafana** consultando InfluxDB y graficando la serie temporal de temperatura y presión:

![Dashboard de Grafana con datos reales](ejemplos/docker-stack-grafana2.png)

## Arquitectura

```
┌────────────┐      HTTP (line protocol)      ┌────────────┐      Query      ┌──────────┐
│  Node-RED  │ ───────────────────────────────▶│  InfluxDB  │◀───────────────│ Grafana  │
│ (simulador │                                  │ (histórico │                 │(dashboard│
│  + lógica) │                                  │  de series)│                 │ en vivo) │
└────────────┘                                  └────────────┘                 └──────────┘
     :1880                                           :8086                         :3000
```

Los tres servicios corren en contenedores separados, conectados por la red
default que crea `docker-compose`, y cada uno con su propio volumen para
persistir datos entre reinicios.

## Cómo correrlo

Requiere Docker y Docker Compose instalados.

```bash
git clone https://github.com/agustin-94/Certificaciones-y-proyectos.git
cd Certificaciones-y-proyectos/docker-monitoreo-stack
docker compose up -d
```

Esto levanta:

| Servicio | URL | Usuario / clave |
|---|---|---|
| Node-RED | http://localhost:1880 | — |
| InfluxDB | http://localhost:8086 | admin / admin12345 |
| Grafana | http://localhost:3000 | admin / admin12345 |

El flow de Node-RED (`node-red-data/flows.json`) ya viene cargado: cada 5
segundos simula una lectura de temperatura y presión, y la manda a InfluxDB
vía su API HTTP (formato *line protocol*), sin necesidad de instalar nodos
adicionales.

### Ver los datos en Grafana

1. Entrá a Grafana → **Connections → Data sources → Add data source →
   InfluxDB**.
2. Configurá:
   - Query language: **Flux**
   - URL: `http://influxdb:8086`
   - Organization: `bariloche-lab`
   - Token: `dev-token-cambiar-en-produccion`
   - Default bucket: `planta`
3. Creá un dashboard con un panel **Time series** que consulte:
   ```flux
   from(bucket: "planta")
     |> range(start: -15m)
     |> filter(fn: (r) => r._measurement == "tanque")
   ```

## Por qué estos valores por defecto

Las credenciales y el token de InfluxDB están hardcodeados en el
`docker-compose.yml` a propósito de que sea un proyecto que cualquiera
pueda levantar y probar en 2 minutos sin configurar nada. **En un entorno
real esto iría en variables de entorno / secrets, nunca en el repo.**

## Qué demuestra este proyecto

- Uso de **Docker Compose** para orquestar múltiples servicios con
  dependencias, puertos y volúmenes persistentes.
- Integración de **Node-RED** como capa de ingesta/lógica hacia una base de
  datos de series temporales (**InfluxDB**), sin depender de paquetes
  adicionales — usando la API HTTP nativa de Influx.
- Armado de un **dashboard de monitoreo** en **Grafana** a partir de esos
  datos, verificado en vivo con datos reales fluyendo de punta a punta.
- Aplicación directa de los contenidos del curso de virtualización y
  contenedores a un caso de uso de automatización/IT-OT, en línea con el
  resto del portafolio (`node-red-tanque`, `dashboard-ocr-mqtt`).

## Stack

`Docker` · `Docker Compose` · `Node-RED` · `InfluxDB 2.x` · `Grafana`
