import os
import shutil
from pathlib import Path

from app import schemas
from app.core.config import settings

from fastapi import UploadFile
from fastapi.responses import FileResponse

from datetime import datetime
from typing import Literal


class CRUDDocuments:
    def get_file(
        self, num_document: str, filename: str, kind: Literal[0, 1, 2] = 0
    ) -> FileResponse | None:
        """
        Obtiene un archivo de un paciente dado su número de documento y nombre

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar
            filename (str): Nombre del archivo que se desea obtener
            kind (Literal[0, 1, 2]): Indica qué tipo de archivo se desea obtener. Los valores posibles son:
                - 0: Archivo de la historia clínica del paciente.
                - 1: Archivo de las órdenes médicas del paciente.
                - 2: Archivo de los resultados médicos del paciente.

        Returns:
            fastapi.responses.FileResponse | None: Retorna un archivo con el contenido del archivo solicitado
            o None si no existe el paciente
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        if not os.path.isdir(patient_path):
            return None

        if kind == 0:
            path: str = f"{patient_path}/{filename}"
        elif kind == 1:
            path: str = f"{patient_path}/orders/{filename}"
        else:
            path: str = f"{patient_path}/results/{filename}"

        return FileResponse(
            path, media_type="application/octet-stream", filename=filename
        )

    def get_documents(self, num_document: str) -> schemas.AllFiles | None:
        """
        Obtiene todos los nombre de los documentos asociados a un paciente dado su número
        de documento

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar

        Returns:
            schemas.AllFiles: Retorna un listado de archivos con todos los documentos
            asociados al paciente
        """
        if not os.path.isdir(f"{settings.PATIENT_DOCS_PATH}/{num_document}"):
            return None

        history = self.get_history(num_document)
        orders = self.get_files(num_document, "orders").filenames
        results = self.get_files(num_document, "results").filenames

        return schemas.AllFiles(
            num_document=num_document, history=history, orders=orders, results=results
        )

    def get_history(self, num_document: str) -> str | None:
        """
        Obtiene la historia clínica de un paciente dado su número de documento

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar

        Returns:
            str: Retorna el nombre del archivo correspondiente a la historia
            clínica del paciente
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        if not os.path.isdir(patient_path):
            return None

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
            if not os.path.isdir(patient_path):
                continue
            histories.append(f"{patient_path}/{settings.HISTORY_FILENAME}")

        return histories

    def get_files(
        self, num_document: str, kind: schemas.KindFiles
    ) -> schemas.Files | None:
        """
        Obtiene el nombre de todos los archivos de un tipo de documento dentro del hospital
        dado su número de documento sin incluir el archivo de la historia clínica

        Args:
            num_document (str): Número de documento del paciente al que se quiere consultar
            kind (Literal["orders", "results"]): Indica qué tipo de archivo se desea obtener. Los valores posibles son:
                - "orders": Archivo de las órdenes médicas del paciente.
                - "results": Archivo de los resultados médicos del paciente.

        Returns:
            list[str] | None: Retorna una lista con los nombres de los archivos del tipo de documento solicitado
            o None si no existe el paciente
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        if not os.path.isdir(patient_path):
            return None

        filenames: list[str] = [file for file in os.listdir(f"{patient_path}/{kind}")]
        return schemas.Files(num_document=num_document, filenames=filenames, kind=kind)

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
        if os.path.exists(patient_path):
            return None

        os.mkdir(patient_path)
        os.mkdir(
            f"{patient_path}/histories"
        )  # Agregar carpeta de historial de historias clínicas
        os.mkdir(f"{patient_path}/orders")  # Agregar carpeta de ordenes médicas
        os.mkdir(f"{patient_path}/results")  # Agregar carpeta de resultados médicos
        Path(f"{patient_path}/{settings.HISTORY_FILENAME}").touch()

    async def update_history(
        self, num_document: str, history: UploadFile
    ) -> Literal[0, 1, 2, 3]:
        """
        Actualiza la historia clínica de un paciente. Cuando se actualiza la historia clínica
        se crea guarda la versión actualizada en el archivo 'history.txt' del paciente y la
        versión anterior se guarda en la carpeta `./patient_docs/{num_document}/histories`.

        Args:
            num_document (str): Número de documento del paciente al que se le quiere actualizar
            la historia clínica
            history (fastapi.UploadFile): Archivo actualizado con la historia clínica del paciente

        Returns:
            typing.Literal[0, 1, 2]: Retorna un número entero simbolizando el estado de la respuesta. Estos son los
            los posibles resultados:
                - 0: Resultado exitoso.
                - 1: Error guardando el historial de la historia clínica.
                - 2: Error al actualizar la historia clínica.
                - 3: Paciente no encontrado.
        """
        # Mover archivo de la historia clínica en los historiales del paciente
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        if not os.path.isdir(patient_path):
            return 3

        history_path: str = f"{patient_path}/histories"
        history_filename: str = f"{patient_path}/{settings.HISTORY_FILENAME}"
        update_filename: str = (
            f'{history_path}/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'
        )

        try:
            shutil.copyfile(history_filename, update_filename)
        except Exception as e:
            print(f"Copiar archivo en {update_filename} falló: {repr(e)}")
            return 1

        # Actualizar archivo de la historia clínica del paciente
        try:
            with open(history_filename, "wb") as f:
                content = await history.read()
                f.write(content)
        except Exception as e:
            print(
                f"Actualizar archivo de la historia clínica del paciente falló: {repr(e)}"
            )
            return 2

        return 0

    async def add_file(
        self, num_document: str, kind: schemas.KindFiles, file: UploadFile
    ) -> Literal[0, 1, 2]:
        """
        Agrega un archivo de una orden médica o resultado médico a un determinado paciente

        Args:
            num_document (str): Número de documento del paciente al que se le quiere actualizar
            la historia clínica
            kind (Literal["orders", "results"]): Indica qué tipo de archivo se desea agregar. Los valores posibles son:
                - "orders": Archivo de las órdenes médicas del paciente.
                - "results": Archivo de los resultados médicos del paciente.
            file (fastapi.UploadFile): Archivo del paciente

        Returns:
            typing.Literal[0, 1]: Retorna un número entero simbolizando el estado de la respuesta. Estos son los
            los posibles resultados:
                - 0: Resultado exitoso.
                - 1: Error guardando el archivo.
                - 2: Paciente no encontrado.
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        if not os.path.isdir(patient_path):
            return 2
        name, ext = os.path.splitext(file.filename)
        filename = f"{patient_path}/{kind}/{name}"
        filename += f'_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}{ext}'

        try:
            with open(filename, "wb") as f:
                content = await file.read()
                f.write(content)
        except Exception as e:
            print(f"Agregar archivo de {kind} del paciente falló: {repr(e)}")
            return 1

        return 0

    def delete_file(
        self, num_document: str, filename: str, kind: schemas.KindFiles
    ) -> Literal[0, 1, 2, 3]:
        """
        Elimina un archivo médico de un determinado paciente (no incluye la historia clínica)

        Args:
            num_document (str): Número de documento del paciente
            filename (str): Nombre del archivo que se desea eliminar
            kind (typing.Literal["orders", "results"]): Indica qué tipo de archivo se desea eliminar. Los valores posibles son:
                - "orders": Archivo de las órdenes médicas del paciente.
                - "results": Archivo de los resultados médicos del paciente.

        Returns:
            Literal[0, 1, 2]: Retorna un número entero simbolizando el estado de la respuesta. Estos son los
            los posibles resultados:
                - 0: Resultado exitoso.
                - 1: Archivo no encontrado.
                - 2: Error desconocido borrando el archivo.
                - 3: Paciente no encontrado.
        """
        patient_path: str = f"{settings.PATIENT_DOCS_PATH}/{num_document}"
        if not os.path.isdir(patient_path):
            return 3
        filename: str = f"{patient_path}/{kind}/{filename}"

        try:
            os.remove(filename)
        except FileNotFoundError:
            return 1
        except Exception as e:
            print(repr(e))
            return 2

        return 0


crud_document = CRUDDocuments()
