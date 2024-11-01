import os

from fastapi import UploadFile
from typing import Literal


class CRUDDocuments:
    def get_documents(self, num_document: str) -> ...:
        """
        Obtiene todos los documentos asociados a un paciente dado su número 
        de documento

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar
        
        Returns:
            ...: Retorna un archivo zip con todos los documentos
            asociados
        """
        pass

    def get_history(self, num_document: str) -> ...:
        """
        Obtiene la historia clínica de un paciente dado su número de documento

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar

        Returns:
            ...: Retorna el archivo correspondiente a la historia
            clínical del paciente
        """
        pass

    def get_histories(self) -> ...:
        """
        Obtiene todas las historias clínicas de los pacientes dentro del hospital

        Returns:
            ...: Retorna un zip con todos las historias clínicas
            de los pacientes dentro del hospital
        """
        pass

    def get_orders(self, num_document: str) -> ...:
        """
        Obtiene todas las ordenes médicas de un paciente dentro del hospital dado su número de
        documento

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar
        
        Returns:
            ...: Retorna un zip con todas las ordenes médicas del paciente
        """
        pass

    def get_results(self, num_document: str) -> ...:
        """
        Obtiene todas los resultados médicos de un paciente dentro del hospital dado su número de
        documento

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar
        
        Returns:
            ...: Retorna un zip con todos los resultados médicos del paciente
        """
        pass
    
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
        pass

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
    
    def add_order(self, num_document: str, order: UploadFile) -> Literal[0, 1]:
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
        pass

    def add_result(self, num_document: str, result: UploadFile) -> Literal[0, 1]:
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
        pass

    def delete_file(self, num_document: str, filename: str):
        """
        Elimina un archivo médico de un determinado paciente (no incluye la historia clínica)

        Args:
            num_document (str): Número de documento del paciente al que se le quiere actualizar
            la historia clínica
            filename (str): Nombre del archivo que se desea eliminar

        Returns:
            int: Retorna un número entero simbolizando el estado de la respuesta. Estos son los
            los posibles resultados:
            - 0: Resultado exitoso.
            - 1: Error guardando el archivo.
        """
        pass


crud_document = CRUDDocuments()
