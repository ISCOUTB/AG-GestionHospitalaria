import os
from pathlib import Path

from app import schemas
from app.core.config import settings

from fastapi import UploadFile
from fastapi.responses import FileResponse

from datetime import datetime
from typing import Literal


class CRUDDocuments:
    def get_file(self, num_document: str, filename: str) -> FileResponse:
        """
        Obtiene un archivo de un paciente dado su número de documento y nombre

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar
            filename (str): Nombre del archivo que se desea obtener
        
        Returns:
            FileResponse: Retorna un archivo con el contenido del archivo solicitado
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        return FileResponse(f'{patient_path}/{filename}')

    def get_documents(self, num_document: str) -> schemas.Files:
        """
        Obtiene todos los nombre de los documentos asociados a un paciente dado su número
        de documento

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar
        
        Returns:
            schemas.Files: Retorna un listado de archivos con todos los documentos
            asociados al paciente
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        history = self.get_history(num_document)
        orders = self.get_orders(num_document)
        results = self.get_results(num_document)
        
        return schemas.Files(history=history, orders=orders, results=results)

    def get_history(self, num_document: str) -> str:
        """
        Obtiene la historia clínica de un paciente dado su número de documento

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar

        Returns:
            str: Retorna el nombre del archivo correspondiente a la historia
            clínica del paciente
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        return f"{patient_path}/{settings.HISTORY_FILENAME}"

    def get_histories(self) -> list[str]:
        """
        Obtiene todas las historias clínicas de los pacientes dentro del hospital

        Returns:
            list[str]: Retorna una lista con todos las historias clínicas 
            de los pacientes dentro del hospital
        """
        histories: list[str] = []
        for num_document in os.listdir(settings.PATIENT_DOCS_PATH):
            patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
            histories.append(f"{patient_path}/{settings.HISTORY_FILENAME}")
        
        return histories

    def get_orders(self, num_document: str) -> list[str]:
        """
        Obtiene el nombre de todos los archivos de las ordenes médicas de un paciente dentro del hospital 
        dado su número de documento

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar
        
        Returns:
            list[str]: Retorna una lista con los nombres de los archivos de las ordenes médicas del paciente
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        return [file for file in os.listdir(f'{patient_path}/orders')]

    def get_results(self, num_document: str) -> list[str]:
        """
        Obtiene el nombre de todos los archivos de los resultados médicos de un paciente dentro del hospital 
        dado su número de documento

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar
        
        Returns:
            ...: Retorna un zip con todos los resultados médicos del paciente
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        return [file for file in os.listdir(f'{patient_path}/results')]
    
    def add_history(self, num_document: str) -> None:
        """
        Crea la historia clínica de un paciente complemetamente vacía. Este método únicamente
        se invoca cuando se agrega un nuevo paciente dentro del sistema.

        Args:
            num_document (str): Número de documento del paciente al que se le quiere crear
            la historia clínica
        
        Returns:
            None: Crea la historia clínica de un paciente como un archivo txt vacío. En caso
            de ya existir, lo omite.
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        Path(f'{patient_path}/{settings.HISTORY_FILENAME}').touch()

    def update_history(self, num_document: str, history: UploadFile) -> Literal[0, 1]:
        """
        Actualiza la historia clínica de un paciente

        Args:
            num_document (str): Número de documento del paciente al que se le quiere actualizar
            la historia clínica
            history (fastapi.UploadFile): Archivo actualizado con la historia clínica del paciente
        
        Returns:
            int: Retorna un número entero simbolizando el estado de la respuesta. Estos son los
            los posibles resultados:
                - 0: Resultado exitoso.
                - 1: Error guardando el archivo.
        """
        pass
    
    async def add_order(self, num_document: str, order: UploadFile) -> Literal[0, 1]:
        """
        Agrega una orden médica a un determinado paciente

        Args:
            num_document (str): Número de documento del paciente al que se le quiere actualizar
            la historia clínica
            order (fastapi.UploadFile): Archivo de la orden médica del paciente
        
        Returns:
            int: Retorna un número entero simbolizando el estado de la respuesta. Estos son los
            los posibles resultados:
            - 0: Resultado exitoso.
            - 1: Error guardando el archivo.
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        order_path: str = f"{patient_path}/orders"
        filename: str = f'{order_path}/{order.filename}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
        
        try:
            with open(filename, 'wb') as f:
                content = await order.read()
                f.write(content)
        except Exception as e:
            print(repr(e))
            return 1

        return 0

    async def add_result(self, num_document: str, result: UploadFile) -> Literal[0, 1]:
        """
        Agrega un resultado médico de un determinado paciente

        Args:
            num_document (str): Número de documento del paciente al que se le quiere actualizar
            la historia clínica
            order (fastapi.UploadFile): Archivo del resultado del examen médico del paciente
        
        Returns:
            int: Retorna un número entero simbolizando el estado de la respuesta. Estos son los
            los posibles resultados:
            - 0: Resultado exitoso.
            - 1: Error guardando el archivo.
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        result_path: str = f"{patient_path}/results"
        filename: str = f'{result_path}/{result.filename}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
        
        try:
            with open(filename, 'wb') as f:
                content = await result.read()
                f.write(content)
        except Exception as e:
            print(repr(e))
            return 1
        
        return 0

    def delete_file(self, num_document: str, filename: str, order: bool = False):
        """
        Elimina un archivo médico de un determinado paciente (no incluye la historia clínica)

        Args:
            num_document (str): Número de documento del paciente al que se le quiere actualizar
            la historia clínica
            filename (str): Nombre del archivo que se desea eliminar
            order (bool): Indica si el archivo es de la orden médica o de resultados médicos

        Returns:
            int: Retorna un número entero simbolizando el estado de la respuesta. Estos son los
            los posibles resultados:
            - 0: Resultado exitoso.
            - 1: Archivo no encontrado.
            - 2: Error desconocido borrando el archivo.
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        if order:
            order_path: str = f"{patient_path}/orders"
            filename: str = f'{order_path}/{filename}'
        else:
            result_path: str = f"{patient_path}/results"
            filename: str = f'{result_path}/{filename}'
        
        try:
            os.remove(filename)
        except FileNotFoundError:
            return 1
        except Exception as e:
            print(repr(e))
            return 2
        
        return 0


crud_document = CRUDDocuments()
