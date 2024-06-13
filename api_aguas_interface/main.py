import streamlit as st
import subprocess
import os
from datetime import datetime
from pathlib import Path
from api_aguas_interface.backend import GenerateReport
import tkinter as tk
from tkinter import filedialog
import logging 
from api_aguas_interface.logger_config import logger, StreamlitLogHandler  # Import the logger from the logger_config module

# Initialize the log handler and add it to the logger
def setup_logger():
    log_handler = StreamlitLogHandler()
    log_handler.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)
    return log_handler

log_handler = setup_logger()

# Default inspection details
detalles_inspeccion = {
    "nombre": f'inspección {datetime.now()}',
    "fecha": "2023-11-28",
    "ubicacion": "string",
    "orden_de_trabajo": "string",
    "clima": "string",
    "inspeccionado_por": "string",
    "numero_certificado": 0,
    "referencia_segmento": "string",
    "año_fabricacion": 0,
    "limpieza_previa": 0,
    "direccion_agua": "string",
    "longitud_entre_juntas": "string",
    "longitud_total": "string",
    "longitud_inspeccionada": "string",
    "ciudad": "string",
    "codigo_ubicacion": "string",
    "detalles_ubicacion": "string",
    "area_drenaje": 0,
    "etiqueta_medio": "string",
    "control_flujo": "string",
    "no_hoja": 0,
    "camara_arriba": "string",
    "dist_marco_solera": 0,
    "camara_abajo": "string",
    "dist_suelo_solera": 0,
    "forma": "string",
    "tamaño": 0,
    "material": "string",
    "revestimiento": "string",
    "uso": "string",
    "categoria": "string",
    "proposito": "string",
    "propietario": "string",
    "galones_usados": 0,
    "juntas_aprobadas": 0,
    "juntas_no_aprobadas": 0,
    "mts_por_pixel": 0.001
}

def initialize_tkinter():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    return root

def pick_folder(root):
    folder_path = filedialog.askdirectory(master=root)
    logger.debug(f"Carpeta: {folder_path}")
    return folder_path

def get_inspection_details():
    st.sidebar.header("Detalles de Inspección")
    details = {
        "nombre": st.sidebar.text_input("Nombre de la Inspección", value=detalles_inspeccion["nombre"]),
        "fecha": st.sidebar.date_input("Fecha", value=datetime.strptime(detalles_inspeccion["fecha"], "%Y-%m-%d")),
        "ubicacion": st.sidebar.text_input("Ubicación", value=detalles_inspeccion["ubicacion"]),
        "orden_de_trabajo": st.sidebar.text_input("Orden de Trabajo", value=detalles_inspeccion["orden_de_trabajo"]),
        "clima": st.sidebar.text_input("Clima", value=detalles_inspeccion["clima"]),
        "inspeccionado_por": st.sidebar.text_input("Inspeccionado Por", value=detalles_inspeccion["inspeccionado_por"]),
        "numero_certificado": st.sidebar.number_input("Número de Certificado", value=detalles_inspeccion["numero_certificado"], min_value=0),
        "referencia_segmento": st.sidebar.text_input("Referencia de Segmento", value=detalles_inspeccion["referencia_segmento"]),
        "año_fabricacion": st.sidebar.number_input("Año de Fabricación", value=detalles_inspeccion["año_fabricacion"], min_value=0),
        "limpieza_previa": st.sidebar.number_input("Limpieza Previa", value=detalles_inspeccion["limpieza_previa"], min_value=0),
        "direccion_agua": st.sidebar.text_input("Dirección del Agua", value=detalles_inspeccion["direccion_agua"]),
        "longitud_entre_juntas": st.sidebar.text_input("Longitud Entre Juntas", value=detalles_inspeccion["longitud_entre_juntas"]),
        "longitud_total": st.sidebar.text_input("Longitud Total", value=detalles_inspeccion["longitud_total"]),
        "longitud_inspeccionada": st.sidebar.text_input("Longitud Inspeccionada", value=detalles_inspeccion["longitud_inspeccionada"]),
        "ciudad": st.sidebar.text_input("Ciudad", value=detalles_inspeccion["ciudad"]),
        "codigo_ubicacion": st.sidebar.text_input("Código de Ubicación", value=detalles_inspeccion["codigo_ubicacion"]),
        "detalles_ubicacion": st.sidebar.text_input("Detalles de Ubicación", value=detalles_inspeccion["detalles_ubicacion"]),
        "area_drenaje": st.sidebar.number_input("Área de Drenaje", value=detalles_inspeccion["area_drenaje"], min_value=0),
        "etiqueta_medio": st.sidebar.text_input("Etiqueta de Medio", value=detalles_inspeccion["etiqueta_medio"]),
        "control_flujo": st.sidebar.text_input("Control de Flujo", value=detalles_inspeccion["control_flujo"]),
        "no_hoja": st.sidebar.number_input("Número de Hoja", value=detalles_inspeccion["no_hoja"], min_value=0),
        "camara_arriba": st.sidebar.text_input("Cámara Arriba", value=detalles_inspeccion["camara_arriba"]),
        "dist_marco_solera": st.sidebar.number_input("Distancia Marco a Solera", value=detalles_inspeccion["dist_marco_solera"], min_value=0),
        "camara_abajo": st.sidebar.text_input("Cámara Abajo", value=detalles_inspeccion["camara_abajo"]),
        "dist_suelo_solera": st.sidebar.number_input("Distancia Suelo a Solera", value=detalles_inspeccion["dist_suelo_solera"], min_value=0),
        "forma": st.sidebar.text_input("Forma", value=detalles_inspeccion["forma"]),
        "tamaño": st.sidebar.number_input("Tamaño", value=detalles_inspeccion["tamaño"], min_value=0),
        "material": st.sidebar.text_input("Material", value=detalles_inspeccion["material"]),
        "revestimiento": st.sidebar.text_input("Revestimiento", value=detalles_inspeccion["revestimiento"]),
        "uso": st.sidebar.text_input("Uso", value=detalles_inspeccion["uso"]),
        "categoria": st.sidebar.text_input("Categoría", value=detalles_inspeccion["categoria"]),
        "proposito": st.sidebar.text_input("Propósito", value=detalles_inspeccion["proposito"]),
        "propietario": st.sidebar.text_input("Propietario", value=detalles_inspeccion["propietario"]),
        "galones_usados": st.sidebar.number_input("Galones Usados", value=detalles_inspeccion["galones_usados"], min_value=0),
        "juntas_aprobadas": st.sidebar.number_input("Juntas Aprobadas", value=detalles_inspeccion["juntas_aprobadas"], min_value=0),
        "juntas_no_aprobadas": st.sidebar.number_input("Juntas No Aprobadas", value=detalles_inspeccion["juntas_no_aprobadas"], min_value=0),
        "mts_por_pixel": st.sidebar.number_input("Metros por Píxel", value=detalles_inspeccion["mts_por_pixel"], min_value=0.001, step=0.001),
    }
    return details

def display_folder_picker():
    root = initialize_tkinter()

    # Title of the app
    st.subheader('Selección de carpeta y generación de reporte')

    # Ensure session state is initialized
    if 'folder_path' not in st.session_state:
        st.session_state.folder_path = ""

    # Layout with two columns
    col1, col2 = st.columns([1, 4])

    # Add folder picker button to the left column
    with col1:
        if st.button('Selección de carpeta'):
            st.session_state.folder_path = pick_folder(root)

    # Display the selected folder path in the right column
    with col2:
        if st.session_state.folder_path:
            st.write("Carpeta seleccionada:", st.session_state.folder_path)

def generate_report(endpoint, username, password, inspection_details, folder_path):
    report_generator = GenerateReport(endpoint, username, password)

    payload = {
        "name": inspection_details["nombre"],
        "date": inspection_details["fecha"].strftime("%Y-%m-%d"),
        "ubicacion": inspection_details["ubicacion"],
        "orden_de_trabajo": inspection_details["orden_de_trabajo"],
        "clima": inspection_details["clima"],
        "inspeccionado_por": inspection_details["inspeccionado_por"],
        "numero_certificado": inspection_details["numero_certificado"],
        "referencia_segmento": inspection_details["referencia_segmento"],
        "año_fabricacion": inspection_details["año_fabricacion"],
        "limpieza_previa": inspection_details["limpieza_previa"],
        "direccion_agua": inspection_details["direccion_agua"],
        "longitud_entre_juntas": inspection_details["longitud_entre_juntas"],
        "longitud_total": inspection_details["longitud_total"],
        "longitud_inspeccionada": inspection_details["longitud_inspeccionada"],
        "ciudad": inspection_details["ciudad"],
        "codigo_ubicacion": inspection_details["codigo_ubicacion"],
        "detalles_ubicacion": inspection_details["detalles_ubicacion"],
        "area_drenaje": inspection_details["area_drenaje"],
        "etiqueta_medio": inspection_details["etiqueta_medio"],
        "control_flujo": inspection_details["control_flujo"],
        "no_hoja": inspection_details["no_hoja"],
        "camara_arriba": inspection_details["camara_arriba"],
        "dist_marco_solera": inspection_details["dist_marco_solera"],
        "camara_abajo": inspection_details["camara_abajo"],
        "dist_suelo_solera": inspection_details["dist_suelo_solera"],
        "forma": inspection_details["forma"],
        "tamaño": inspection_details["tamaño"],
        "material": inspection_details["material"],
        "revestimiento": inspection_details["revestimiento"],
        "uso": inspection_details["uso"],
        "categoria": inspection_details["categoria"],
        "proposito": inspection_details["proposito"],
        "propietario": inspection_details["propietario"],
        "galones_usados": inspection_details["galones_usados"],
        "jutas_aprobadas": inspection_details["juntas_aprobadas"],
        "juntas_no_aprobadas": inspection_details["juntas_no_aprobadas"],
        "mts_per_pixel": inspection_details["mts_por_pixel"],
    }

    with st.spinner("Creando inspección..."):
        logger.info("Creating inspection with payload")
        report_generator.create_inspection(payload=payload)
    with st.spinner("Cargando imágenes..."):    
        logger.info("Loading folder with images")
        report_generator.load_folder(folder=Path(folder_path))

    with st.spinner("Generando reporte..."):
        logger.info("Generating report")
        report_generator.generate_report()
    
    with st.spinner("Descargando reporte..."):
        link = report_generator.download_report()
        logger.info(f"Report downloaded, link: {link}")
        st.write("Link Report:", link)

def main():
    logger.info("Starting the Streamlit app")
    st.title("Generador de reportes de inspección")

    inspection_details = get_inspection_details()
    st.subheader('Login')
    username = st.text_input('Nombre de usuario')
    password = st.text_input("Constraseña", type="password")
    endpoint = st.text_input('Endpoint')

    display_folder_picker()
    
    if st.button("Generar reporte"):
        if st.session_state.folder_path:
            generate_report(endpoint, username, password, inspection_details, st.session_state.folder_path)
        else:
            st.warning("Por favor seleccione una carpeta primero")
            logger.warning("No folder selected when trying to generate report")
    
    # Display logs
    st.subheader("Logs")
    st.text_area("Log Output", value=log_handler.get_logs(), height=300)


def launch_streamlit_app():
    app_path = os.path.realpath(__file__)
    if not os.path.isfile(app_path):
        logger.error(f"The file '{app_path}' does not exist.")
        raise FileNotFoundError(f"The file '{app_path}' does not exist.")

    os.system(f'streamlit run {app_path}')
    logger.info("Streamlit app launched")


if __name__ == "__main__":
    main()
