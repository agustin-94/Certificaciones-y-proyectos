# Dashboard OCR + MQTT (Python ↔ Node-RED)

## Descripción
Proyecto integrador que conecta dos piezas independientes del portafolio
en un flujo de datos real de punta a punta, simulando un caso de uso
IT/OT típico: un sistema de reconocimiento de dígitos en Python publica
lecturas por MQTT, y un dashboard en Node-RED las recibe y visualiza en
tiempo real.

```
┌─────────────────┐        MQTT        ┌──────────────────────┐
│  predictor_mqtt   │ ──topic: ocr/digito──▶│   Node-RED Dashboard   │
│  (ocr-digitos)    │                     │  (gauge + chart + texto)│
└─────────────────┘                     └──────────────────────┘
        ▲
        │
   modelo_ocr.h5
   (train.py)
```

## Componentes
- **`predictor_mqtt.py`** (del proyecto [`ocr-digitos`](../ocr-digitos)):
  publica cada dígito reconocido al topic `ocr/digito`.
- **Broker MQTT (Mosquitto)**: intermediario de mensajería, corriendo en
  `localhost:1883`.
- **`flow.json`** (este proyecto): flujo de Node-RED que se suscribe al
  topic y arma un dashboard con:
  - Un **gauge** mostrando el último dígito recibido (0-9)
  - Un **gráfico de línea** con el historial de dígitos en el tiempo
  - Un **texto** con el último dígito y la hora de recepción

## Resultado
![Dashboard funcionando](assets/dashboard_funcionando.png)

## Cómo levantar la integración completa

### 1. Broker MQTT
```powershell
cd "C:\Program Files\Mosquitto"
.\mosquitto.exe -v
```

### 2. Node-RED + Dashboard
Si no tenés Node-RED instalado:
```bash
npm install -g node-red
```

Necesitás además el paquete de dashboard (los nodos `ui_gauge`,
`ui_chart`, `ui_text` no vienen por defecto):
```bash
npm install -g node-red-dashboard
```
O instalalo desde el editor: menú ☰ → *Manage palette* → pestaña
*Install* → buscar `node-red-dashboard` → *Install*.

Arrancar Node-RED:
```bash
node-red
```
Abrir `http://localhost:1880`, importar `flow.json` (☰ → *Import* →
pegar el contenido del archivo), click en *Deploy*.

### 3. Publicador Python
```powershell
cd ocr-digitos
python predictor_mqtt.py
```

### 4. Ver el dashboard
Abrir `http://localhost:1880/ui` — ahí se ve el gauge, el gráfico y el
texto actualizándose cada vez que el script de Python publica un nuevo
dígito (cada 3 segundos en modo simulación).

## Tecnologías
- Python (paho-mqtt)
- Mosquitto (broker MQTT)
- Node-RED + node-red-dashboard

## Conceptos aplicados
- Arquitectura productor/consumidor con mensajería (MQTT)
- Integración entre un componente de Machine Learning (Python) y un
  sistema de automatización industrial (Node-RED)
- Visualización de datos en tiempo real

## Notas
Este proyecto depende de tener corriendo, al mismo tiempo: el broker
Mosquitto, Node-RED con el flujo importado, y el script de Python. Para
quien solo quiera ver el resultado sin levantar todo el stack, la captura
en `assets/dashboard_funcionando.png` muestra el dashboard en
funcionamiento.
