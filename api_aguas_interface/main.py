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
log_handler = StreamlitLogHandler()
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

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

# Streamlit app
def main():
    logger.info("Starting the Streamlit app")
    st.title("Inspection Report Generator")

    st.sidebar.header("Detalles de Inspección")
    nombre = st.sidebar.text_input("Nombre de la Inspección", value=detalles_inspeccion["nombre"])
    fecha = st.sidebar.date_input("Fecha", value=datetime.strptime(detalles_inspeccion["fecha"], "%Y-%m-%d"))
    ubicacion = st.sidebar.text_input("Ubicación", value=detalles_inspeccion["ubicacion"])
    orden_de_trabajo = st.sidebar.text_input("Orden de Trabajo", value=detalles_inspeccion["orden_de_trabajo"])
    clima = st.sidebar.text_input("Clima", value=detalles_inspeccion["clima"])
    inspeccionado_por = st.sidebar.text_input("Inspeccionado Por", value=detalles_inspeccion["inspeccionado_por"])
    numero_certificado = st.sidebar.number_input("Número de Certificado", value=detalles_inspeccion["numero_certificado"], min_value=0)
    referencia_segmento = st.sidebar.text_input("Referencia de Segmento", value=detalles_inspeccion["referencia_segmento"])
    año_fabricacion = st.sidebar.number_input("Año de Fabricación", value=detalles_inspeccion["año_fabricacion"], min_value=0)
    limpieza_previa = st.sidebar.number_input("Limpieza Previa", value=detalles_inspeccion["limpieza_previa"], min_value=0)
    direccion_agua = st.sidebar.text_input("Dirección del Agua", value=detalles_inspeccion["direccion_agua"])
    longitud_entre_juntas = st.sidebar.text_input("Longitud Entre Juntas", value=detalles_inspeccion["longitud_entre_juntas"])
    longitud_total = st.sidebar.text_input("Longitud Total", value=detalles_inspeccion["longitud_total"])
    longitud_inspeccionada = st.sidebar.text_input("Longitud Inspeccionada", value=detalles_inspeccion["longitud_inspeccionada"])
    ciudad = st.sidebar.text_input("Ciudad", value=detalles_inspeccion["ciudad"])
    codigo_ubicacion = st.sidebar.text_input("Código de Ubicación", value=detalles_inspeccion["codigo_ubicacion"])
    detalles_ubicacion = st.sidebar.text_input("Detalles de Ubicación", value=detalles_inspeccion["detalles_ubicacion"])
    area_drenaje = st.sidebar.number_input("Área de Drenaje", value=detalles_inspeccion["area_drenaje"], min_value=0)
    etiqueta_medio = st.sidebar.text_input("Etiqueta de Medio", value=detalles_inspeccion["etiqueta_medio"])
    control_flujo = st.sidebar.text_input("Control de Flujo", value=detalles_inspeccion["control_flujo"])
    no_hoja = st.sidebar.number_input("Número de Hoja", value=detalles_inspeccion["no_hoja"], min_value=0)
    camara_arriba = st.sidebar.text_input("Cámara Arriba", value=detalles_inspeccion["camara_arriba"])
    dist_marco_solera = st.sidebar.number_input("Distancia Marco a Solera", value=detalles_inspeccion["dist_marco_solera"], min_value=0)
    camara_abajo = st.sidebar.text_input("Cámara Abajo", value=detalles_inspeccion["camara_abajo"])
    dist_suelo_solera = st.sidebar.number_input("Distancia Suelo a Solera", value=detalles_inspeccion["dist_suelo_solera"], min_value=0)
    forma = st.sidebar.text_input("Forma", value=detalles_inspeccion["forma"])
    tamaño = st.sidebar.number_input("Tamaño", value=detalles_inspeccion["tamaño"], min_value=0)
    material = st.sidebar.text_input("Material", value=detalles_inspeccion["material"])
    revestimiento = st.sidebar.text_input("Revestimiento", value=detalles_inspeccion["revestimiento"])
    uso = st.sidebar.text_input("Uso", value=detalles_inspeccion["uso"])
    categoria = st.sidebar.text_input("Categoría", value=detalles_inspeccion["categoria"])
    proposito = st.sidebar.text_input("Propósito", value=detalles_inspeccion["proposito"])
    propietario = st.sidebar.text_input("Propietario", value=detalles_inspeccion["propietario"])
    galones_usados = st.sidebar.number_input("Galones Usados", value=detalles_inspeccion["galones_usados"], min_value=0)
    juntas_aprobadas = st.sidebar.number_input("Juntas Aprobadas", value=detalles_inspeccion["juntas_aprobadas"], min_value=0)
    juntas_no_aprobadas = st.sidebar.number_input("Juntas No Aprobadas", value=detalles_inspeccion["juntas_no_aprobadas"], min_value=0)
    mts_por_pixel = st.sidebar.number_input("Metros por Píxel", value=detalles_inspeccion["mts_por_pixel"], min_value=0.001, step=0.001)
    
    username = st.text_input('Username')
    password = st.text_input("Enter a password", type="password")
    endpoint = st.text_input('Endpoint')

    # Initialize tkinter
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)

    # Function to pick a folder
    def pick_folder():
        folder_path = filedialog.askdirectory(master=root)
        logger.debug(f"Folder picked: {folder_path}")
        return folder_path

    # Title of the app
    st.title('Folder Picker and Process Starter')

    # Ensure session state is initialized
    if 'folder_path' not in st.session_state:
        st.session_state.folder_path = ""

    # Layout with two columns
    col1, col2 = st.columns([1, 4])

    # Add folder picker button to the left column
    with col1:
        if st.button('Pick Folder'):
            st.session_state.folder_path = pick_folder()

    # Display the selected folder path in the right column
    with col2:
        if st.session_state.folder_path:
            st.write("Selected Folder:", st.session_state.folder_path)
    
    if st.button("Generate Report"):
        if st.session_state.folder_path:
            report_generator = GenerateReport(endpoint, username, password)

            payload = {
                "name": nombre,
                "date": fecha.strftime("%Y-%m-%d"),
                "ubicacion": ubicacion,
                "orden_de_trabajo": orden_de_trabajo,
                "clima": clima,
                "inspeccionado_por": inspeccionado_por,
                "numero_certificado": numero_certificado,
                "referencia_segmento": referencia_segmento,
                "año_fabricacion": año_fabricacion,
                "limpieza_previa": limpieza_previa,
                "direccion_agua": direccion_agua,
                "longitud_entre_juntas": longitud_entre_juntas,
                "longitud_total": longitud_total,
                "longitud_inspeccionada": longitud_inspeccionada,
                "ciudad": ciudad,
                "codigo_ubicacion": codigo_ubicacion,
                "detalles_ubicacion": detalles_ubicacion,
                "area_drenaje": area_drenaje,
                "etiqueta_medio": etiqueta_medio,
                "control_flujo": control_flujo,
                "no_hoja": no_hoja,
                "camara_arriba": camara_arriba,
                "dist_marco_solera": dist_marco_solera,
                "camara_abajo": camara_abajo,
                "dist_suelo_solera": dist_suelo_solera,
                "forma": forma,
                "tamaño": tamaño,
                "material": material,
                "revestimiento": revestimiento,
                "uso": uso,
                "categoria": categoria,
                "proposito": proposito,
                "propietario": propietario,
                "galones_usados": galones_usados,
                "jutas_aprobadas": juntas_aprobadas,
                "juntas_no_aprobadas": juntas_no_aprobadas,
                "mts_per_pixel": mts_por_pixel,
            }

            with st.spinner("Creating inspection..."):
                logger.info("Creating inspection with payload")
                report_generator.create_inspection(payload=payload)
            with st.spinner("Loading Images..."):    
                logger.info("Loading folder with images")
                report_generator.load_folder(folder=Path(st.session_state.folder_path))

            with st.spinner("Generating report..."):
                logger.info("Generating report")
                report_generator.generate_report()
            
            with st.spinner("Downloading report..."):
                link = report_generator.download_report()
                logger.info(f"Report downloaded, link: {link}")
                st.write("Link Report:", link)
        else:
            st.warning("Please select a folder first")
            logger.warning("No folder selected when trying to generate report")
    
    # Display logs
    st.subheader("Logs")
    st.text_area("Log Output", value=log_handler.get_logs(), height=300)

def launch_streamlit_app():
    app_path = os.path.realpath(__file__)
    if not os.path.isfile(app_path):
        logger.error(f"The file '{app_path}' does not exist.")
        raise FileNotFoundError(f"The file '{app_path}' does not exist.")

    # Run the Streamlit app using subprocess
    # subprocess.Popen(['streamlit', 'run', app_path])

    os.system(f'streamlit run {app_path}')
    logger.info("Streamlit app launched")

if __name__ == "__main__":
    main()
