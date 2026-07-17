import time
import matplotlib.pyplot as plt

# ---------------------------------------------------
# Declaración de la clase Turbina y PID
# ---------------------------------------------------
class PID:
    def __init__(self, kp, ki, kd, salida_min=0, salida_max=100):
        self.kp = kp  # Ganancia proporcional
        self.ki = ki  # Ganancia integral
        self.kd = kd  # Ganancia derivativa
        self.previous_error = 0  # Error anterior
        self.integral = 0  # Suma de errores (integral)
        self.salida_min = salida_min
        self.salida_max = salida_max

    def compute(self, setpoint, measured_value, dt):
        # Calcular el error
        error = setpoint - measured_value

        # Integral candidata (antes de aplicar anti-windup)
        integral_candidata = self.integral + error * dt

        # Calcular la derivada del error
        derivative = error - self.previous_error

        # Salida candidata usando la integral candidata
        salida_candidata = (self.kp * error) + (self.ki * integral_candidata) + (self.kd * derivative)

        # Anti-windup: si la salida está saturada Y el error empuja en la misma
        # dirección de la saturación, no seguimos acumulando integral. Esto evita
        # que el controlador "se vaya de rango" y tarde en reaccionar cuando el
        # error cambia de signo (integral windup).
        saturado_arriba = salida_candidata > self.salida_max and error > 0
        saturado_abajo = salida_candidata < self.salida_min and error < 0
        if not (saturado_arriba or saturado_abajo):
            self.integral = integral_candidata

        # Calcular la salida final del PID con la integral ya corregida
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        # Actualizar el error anterior
        self.previous_error = error

        return max(self.salida_min, min(self.salida_max, output))


class Turbina:
    def __init__(self):
        self.motorAux = False  # Estado del motor auxiliar
        self.junta = False  # Estado de la junta
        self.Q1 = False  # Estado del quemador 1
        self.Q2 = False  # Estado del quemador 2
        self.Valvula = 0.0  # Porcentaje de apertura de la válvula (0-100%)

        self.friccion = 5  # Tasa de fricción (pérdida de RPM)
        self.aporteMotor = 0.0  # Aporte de RPM del motor
        self.aporteQuemadores = 0.0  # Aporte de RPM de los quemadores

        self.RPM = 0.0  # RPM actual de la turbina
        self.pid = PID(kp=0.05, ki=0.01, kd=0.15)  # Controlador PID (ganancias ajustadas)
        self.setpoint = 4600  # RPM objetivo
        self.dt = 1  # Tiempo de actualización en segundos

    def update(self):
        # Calcular aporte del motor
        if self.motorAux and self.junta:
            self.aporteMotor = 10.0  # Si motor+junta, acelera
        else:
            self.aporteMotor = 0.0  # Si no, no hay aporte

        # Calcular aporte de los quemadores
        if self.Q1 or self.Q2:  # Si alguno de los quemadores está encendido
            self.aporteQuemadores = self.Valvula * 0.5  # Aporte proporcional a la apertura de la válvula
        else:
            self.aporteQuemadores = 0.0  # Sin aporte

        # Calcular RPM
        self.RPM += self.aporteMotor + self.aporteQuemadores - self.friccion

        # Limitar RPM a un mínimo de 0
        if self.RPM < 0:
            self.RPM = 0

        # Controlar la válvula usando PID
        self.Valvula = self.pid.compute(self.setpoint, self.RPM, self.dt)
        # Asegurarse de que la válvula esté en el rango [0, 100]
        self.Valvula = max(0, min(100, self.Valvula))


# ---------------------------------------------------
# Inicio de la simulación
# ---------------------------------------------------
def simular(pasos=250, tiempo_real=False):
    """Corre la simulación por una cantidad fija de pasos y devuelve
    el historial de RPM y apertura de válvula para poder graficarlos."""
    tur1 = Turbina()

    # Configurar el estado inicial de la turbina
    tur1.motorAux = True  # Activar motor auxiliar
    tur1.junta = True  # Acoplar la junta
    tur1.Q1 = True  # Encender el quemador 1
    tur1.Q2 = True  # Encender el quemador 2
    tur1.Valvula = 100  # Abrir válvula al 100%

    historial_rpm = []
    historial_valvula = []

    for etapa in range(pasos):
        tur1.update()

        historial_rpm.append(tur1.RPM)
        historial_valvula.append(tur1.Valvula)

        print(f"Etapa: {etapa}, RPM: {tur1.RPM:.2f}, Válvula: {tur1.Valvula:.2f}, "
              f"Motor Aux: {tur1.motorAux}, Junta: {tur1.junta}, Q1: {tur1.Q1}, Q2: {tur1.Q2}")

        # Ejemplo de condición para controlar componentes
        if tur1.RPM > tur1.setpoint * 1.05:
            tur1.motorAux = False  # Apagar motor si las RPM superan el setpoint por margen
            print("Motor Aux apagado: RPM por encima del margen permitido.")

        if tiempo_real:
            time.sleep(tur1.dt)

    return historial_rpm, historial_valvula, tur1.setpoint


def graficar(historial_rpm, historial_valvula, setpoint, salida="assets/grafico_rpm.png"):
    """Genera un gráfico de RPM y apertura de válvula a lo largo del tiempo."""
    tiempo = list(range(len(historial_rpm)))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)

    ax1.plot(tiempo, historial_rpm, color="#1f77b4", label="RPM turbina")
    ax1.axhline(y=setpoint, color="#d62728", linestyle="--", label=f"Setpoint ({setpoint} RPM)")
    ax1.set_ylabel("RPM")
    ax1.set_title("Respuesta del control PID: RPM vs tiempo")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(tiempo, historial_valvula, color="#2ca02c", label="Apertura de válvula (%)")
    ax2.set_xlabel("Etapa (segundos simulados)")
    ax2.set_ylabel("Válvula (%)")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(salida, dpi=150)
    print(f"Gráfico guardado en: {salida}")


if __name__ == "__main__":
    try:
        rpm_hist, valvula_hist, setpoint = simular(pasos=250, tiempo_real=False)
        graficar(rpm_hist, valvula_hist, setpoint)
    except KeyboardInterrupt:
        print("Simulación finalizada")
