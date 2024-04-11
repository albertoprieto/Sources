import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import boto3

class DocumentDownloader:
    """
    Esta clase maneja la descarga de documentos desde un sitio web y su posterior carga en Amazon S3.
    """

    def __init__(self):
        """
        Inicializa la clase con las variables de configuración y el controlador de Selenium.
        """
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(20)
        self.carpeta_descargas = os.environ.get('fd')
        self.s3_bucket_name = os.environ.get('bucket')
        self.s3_key_prefix = os.environ.get('prefix')

    def upload_to_s3(self, file_path: str, s3_key: str) -> None:
        """
        Sube un archivo a Amazon S3.

        Args:
            file_path (str): Ruta local del archivo a subir.
            s3_key (str): Clave en S3 donde se almacenará el archivo.

        Returns:
            None
        """
        s3 = boto3.client('s3')
        with open(file_path, 'rb') as file_data:
            s3.upload_fileobj(file_data, self.s3_bucket_name, s3_key)

    def verificar_archivo_descargado(self, ruta_carpeta_descargas: str, nombre_base: str) -> str:
        """
        Verifica si un archivo ha sido descargado.

        Args:
            ruta_carpeta_descargas (str): Ruta de la carpeta de descargas.
            nombre_base (str): Nombre base del archivo a buscar.

        Returns:
            str: Ruta completa del archivo descargado si se encuentra, None en caso contrario.
        """
        lista_archivos = os.listdir(ruta_carpeta_descargas)
        for archivo in lista_archivos:
            ruta_archivo = os.path.join(ruta_carpeta_descargas, archivo)
            if os.path.isfile(ruta_archivo) and nombre_base == archivo:
                print(ruta_archivo, 'Encontrado')
                time.sleep(10)
                return ruta_archivo
        return None

    def download_and_upload(self):
        """
        Descarga documentos desde un sitio web y los carga en Amazon S3.
        """
        self.driver.get(os.environ.get('URL'))
        input("Por favor, inicia sesión manualmente y presiona Enter cuando hayas terminado...")

        processed_lines = set()
        if os.path.exists('procesados.txt'):
            with open('procesados.txt', 'r') as f:
                processed_lines = set(line.strip() for line in f)
        x = 0
        contador = 0

        with open("llaves.txt", "r") as file:
            for linea in file:
                linea = linea.strip()
                if linea in processed_lines:
                    continue  # Skip already processed lines

                rfc = self.driver.find_element(By.ID, "llaveefaa96db-16e4-4990-976f-a64001852b18")
                rfc.clear()
                rfc.send_keys(linea)
                print('Procesando', linea)
                boton_consultar = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "btnConsultar")))
                boton_consultar.click()

                form_descarga = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "frmDescargaDocumentos")))
                time.sleep(3)
                elemento_descargar = form_descarga.find_element(By.CLASS_NAME, "btn-group")
                elemento_descargar.click()
                enlace_documentos_llaves = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "btnDescargarDocumentosLlaves")))
                enlace_documentos_llaves.click()

                if x == 1:
                    nombre_base = f"Documentos_Llaves{time.strftime('%d_%m_%Y')}.zip"
                    x = 2
                else:
                    nombre_base = f"Documentos_Llaves{time.strftime('%d_%m_%Y')}({contador}).zip"

                print('Buscando el archivo', nombre_base)
                ruta_archivo = os.path.join(self.carpeta_descargas, nombre_base)

                while not os.path.exists(ruta_archivo) or os.path.getsize(ruta_archivo) == 0:
                    time.sleep(1)
                print('Encontrado', nombre_base)
                contador += 1

                with open('procesados.txt', 'a') as f:
                    f.write(linea + '\n')

                with open('asociados.txt', 'a') as f:
                    f.write(linea + ' ' + nombre_base + '\n')

                # Subir archivo a S3
                s3_key = os.path.join(self.s3_key_prefix, nombre_base)
                self.upload_to_s3(ruta_archivo, s3_key)

        # Cerrar el controlador de Selenium
        self.driver.quit()

# Pruebas unitarias
def test_download_and_upload():
    downloader = DocumentDownloader()
    downloader.upload_to_s3 = MagicMock()
    downloader.download_and_upload()
    assert downloader.upload_to_s3.called_once()

if __name__ == "__main__":
    test_download_and_upload()  # Ejecutar pruebas unitarias
