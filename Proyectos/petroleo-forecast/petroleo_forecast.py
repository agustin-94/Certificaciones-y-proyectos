"""
Pronóstico de producción de petróleo (cuenca Golfo San Jorge) con XGBoost.

Pipeline:
1. Cargar y filtrar el dataset de producción de petróleo por cuenca.
2. Agregar la producción mensual (promedio) de la cuenca elegida.
3. Separar los últimos 10 períodos como validación "real" (los que el
   modelo nunca ve durante el entrenamiento).
4. Entrenar un XGBRegressor con early stopping.
5. Comparar la predicción contra los valores reales y graficar.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xgboost as xgb
from sklearn.model_selection import train_test_split

CUENCA = "GOLFO SAN JORGE"
ARCHIVO_DATOS = "PetroleoArg.csv"
COLUMNAS_INTERESANTES = [
    "empresa", "anio", "mes", "provincia", "cantidad",
    "indice_tiempo", "areayacimiento", "concepto", "cuenca",
]


def cargar_datos(archivo=ARCHIVO_DATOS):
    df = pd.read_csv(archivo)
    return df[COLUMNAS_INTERESANTES]


def agregar_por_cuenca(datos, cuenca=CUENCA):
    """Filtra por cuenca y agrega (promedio) la producción por período de tiempo."""
    filtrado = datos.query("cuenca == @cuenca")

    # numeric_only=True: versiones recientes de pandas intentan promediar
    # también las columnas de texto si no se lo indicamos explícitamente,
    # y eso rompe con TypeError.
    agregado = filtrado.groupby("indice_tiempo").mean(numeric_only=True)
    agregado.index = pd.to_datetime(agregado.index, format="%Y-%m")
    agregado = agregado.sort_index()
    return agregado


def graficar_serie(serie, salida="assets/produccion_historica.png"):
    plt.figure(figsize=(14, 6))
    sns.set(font_scale=0.8)
    ax = sns.lineplot(x=serie.index, y="cantidad", data=serie)
    ax.set_xlabel("Año")
    ax.set_ylabel(f"Producción de petróleo — {CUENCA}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(salida, dpi=150)
    plt.close()
    print(f"Gráfico histórico guardado en: {salida}")


def entrenar_modelo(serie):
    """Separa los últimos 10 períodos como validación real, entrena el
    modelo con el resto y devuelve el modelo + los datos de validación."""
    df_ultimos_10 = serie.iloc[-10:]
    df_sin_ultimos_10 = serie.iloc[:-10]

    X = df_sin_ultimos_10.iloc[:, :-1].values
    y = df_sin_ultimos_10.iloc[:, -1].values
    X_valid = df_ultimos_10.iloc[:, :-1].values
    y_valid = df_ultimos_10.iloc[:, -1].values

    # Nota: para series de tiempo suele evitarse el shuffle aleatorio del
    # train_test_split (podría "filtrar" información de meses futuros hacia
    # el entrenamiento). Acá se mantiene el shuffle porque las únicas
    # features son año/mes (no hay lags), así que no hay fuga real de
    # información temporal — pero es algo a tener en cuenta si se agregan
    # variables que sí dependan del orden temporal (ej. medias móviles).
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Tamaño de X_train:", X_train.shape)
    print("Tamaño de y_train:", y_train.shape)
    print("Tamaño de X_test:", X_test.shape)
    print("Tamaño de y_test:", y_test.shape)

    # En XGBoost >= 2.0, eval_metric y early_stopping_rounds van en el
    # constructor del modelo, no en .fit()
    modelo = xgb.XGBRegressor(
        n_estimators=500,
        objective="reg:squarederror",
        random_state=42,
        eval_metric="rmse",
        early_stopping_rounds=9,
    )
    modelo.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False,
    )

    return modelo, df_ultimos_10, X_valid, y_valid


def comparar_prediccion(modelo, serie, df_ultimos_10, X_valid):
    y_pred = modelo.predict(X_valid)

    y_pred_df = pd.DataFrame(y_pred, columns=["cantidad_pred"])
    y_pred_df.index = df_ultimos_10.index

    df_compare = pd.concat([serie, y_pred_df], axis=1)
    return df_compare


def graficar_comparacion(df_compare, salida="assets/prediccion_vs_real.png"):
    plt.figure(figsize=(14, 6))
    ultimos = df_compare.iloc[-15:]
    plt.plot(ultimos.index, ultimos["cantidad"], marker="o", label="Real")
    plt.plot(ultimos.index, ultimos["cantidad_pred"], marker="o", label="Predicción (XGBoost)")
    plt.xlabel("Período")
    plt.ylabel(f"Producción de petróleo — {CUENCA}")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(salida, dpi=150)
    plt.close()
    print(f"Gráfico de comparación guardado en: {salida}")


def main():
    datos = cargar_datos()
    serie = agregar_por_cuenca(datos)

    graficar_serie(serie)

    modelo, df_ultimos_10, X_valid, y_valid = entrenar_modelo(serie)
    df_compare = comparar_prediccion(modelo, serie, df_ultimos_10, X_valid)

    graficar_comparacion(df_compare)

    print("\nComparación (últimos 10 períodos reales vs predichos):")
    print(df_compare.tail(10)[["cantidad", "cantidad_pred"]])


if __name__ == "__main__":
    main()
