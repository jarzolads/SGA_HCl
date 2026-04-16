import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import pandas as pd
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="SGA - Panel Interactivo de Proceso",
    page_icon="🌱",
    layout="wide"
)

st.title("Sistema de Gestión Ambiental y Proceso")
st.markdown("Selecciona un equipo en el diagrama (Diagrama DTI/PFD) para visualizar sus métricas de sostenibilidad, balances de energía y estado de operación.")

# --- 1. BASE DE DATOS DEL SGA (LCA y Operación) ---
sga_data = {
    "B-110": {
        "equipo": "Tanque de Alimentación (B-110)",
        "funcion": "Almacenamiento de materia prima",
        "estado": "Operativo",
        "emisiones_co2": "1.2 kg CO2eq/h",
        "consumo_energia": "5 kWh",
        "impacto_lca": "Bajo - Materiales de origen sostenible",
        "observaciones": "Niveles estables. Cumple normativa de contención."
    },
    "W-110": {
        "equipo": "Intercambiador de Calor (W-110)",
        "funcion": "Recuperación de energía térmica",
        "estado": "Alerta Preventiva",
        "emisiones_co2": "15.4 kg CO2eq/h",
        "consumo_energia": "120 kWh",
        "impacto_lca": "Medio - Alta huella térmica en fase de uso",
        "observaciones": "Eficiencia de transferencia disminuida un 4%. Programar limpieza."
    },
    "K-110": {
        "equipo": "Columna Separadora Principal (K-110)",
        "funcion": "Separación de fases/fraccionamiento",
        "estado": "Operativo",
        "emisiones_co2": "45.0 kg CO2eq/h",
        "consumo_energia": "350 kWh",
        "impacto_lca": "Alto - Principal consumidor energético del proceso",
        "observaciones": "Operando bajo parámetros de diseño con lazos de control PID estables."
    }
}

# --- 2. DEFINICIÓN DE COORDENADAS (Hitboxes) ---
# Define los rangos de píxeles (x_min, x_max, y_min, y_max) para cada equipo
# Ajusta estos valores según la resolución de tu imagen 'diagrama_proceso.png'
hitboxes = {
    "B-110": (310, 400, 55, 145),
    "W-110": (600, 700, 220, 320),
    "K-110": (930, 1030, 310, 410)
}

def get_clicked_equipment(x, y):
    """Retorna el ID del equipo si el clic coincide con sus coordenadas."""
    for eq_id, (xmin, xmax, ymin, ymax) in hitboxes.items():
        if xmin <= x <= xmax and ymin <= y <= ymax:
            return eq_id
    return None

# --- 3. INTERFAZ Y RENDERIZADO ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Diagrama de Flujo (PFD / DTI)")
    try:
        # Renderiza la imagen y captura el evento de clic
        img = Image.open("Diagrama DTI-2.png")
        click_data = streamlit_image_coordinates(img, key="pfd_click")
    except FileNotFoundError:
        st.error("⚠️ No se encontró la imagen 'diagrama_proceso.png'.")
        click_data = None

with col2:
    st.subheader("Indicadores del Equipo")
    
    if click_data is not None:
        x_click, y_click = click_data["x"], click_data["y"]
        eq_id = get_clicked_equipment(x_click, y_click)
        
        if eq_id and eq_id in sga_data:
            data = sga_data[eq_id]
            
            st.markdown(f"### {data['equipo']}")
            
            # Etiqueta de estado
            color = "green" if data["estado"] == "Operativo" else "orange"
            st.markdown(f"**Estado:** :{color}[{data['estado']}]")
            st.divider()
            
            # Panel de métricas ambientales
            met_col1, met_col2 = st.columns(2)
            met_col1.metric(label="Huella de Carbono", value=data["emisiones_co2"])
            met_col2.metric(label="Consumo Eléctrico", value=data["consumo_energia"])
            
            # Información adicional
            st.info(f"**Análisis de Ciclo de Vida:**\n{data['impacto_lca']}")
            st.write(f"**Función en el Proceso:** {data['funcion']}")
            st.write(f"**Notas de Control:** {data['observaciones']}")
            
        else:
            st.write("Haz clic sobre un equipo específico (ej. Tanque B-110, Intercambiador W-110) en el diagrama para evaluar sus parámetros ambientales.")
    else:
        st.write("Esperando interacción con el diagrama...")
