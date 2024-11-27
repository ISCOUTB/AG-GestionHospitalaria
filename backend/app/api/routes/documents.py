import os
from time import perf_counter

from fastapi import APIRouter, status, File, UploadFile, Request
from fastapi.responses import FileResponse

from app.api.deps import Doctor, NonPatient, log_request
from app.api import exceptions

from app.core.config import settings
from app.crud import crud_document

from app import schemas

router = APIRouter(prefix="/documents")


@router.get("/all/{num_document}")
async def get_all_documents(
    num_document: str, request: Request, current_user: NonPatient
) -> schemas.AllFiles:
    """
    Obtiene todos los documentos asociados a un paciente
    """
    start_time = perf_counter()
    documents = crud_document.get_documents(num_document)
    if documents is None:
        raise exceptions.patient_not_found
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return documents


@router.get("/all")
async def get_all(request: Request, current_user: NonPatient) -> list[schemas.AllFiles]:
    """
    Obtiene todos los documentos de todos los pacientes en un archivo .zip
    """
    start_time = perf_counter()
    documents: list[schemas.AllFiles] = []
    root_path = settings.PATIENT_DOCS_PATH
    for num_document in os.listdir(root_path):
        if not os.path.isdir(f"{root_path}/{num_document}"):
            continue
        documents.append(crud_document.get_documents(num_document))

    process_time = perf_counter() - start_time
    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return documents


@router.get("/histories/{num_document}", summary="Get Clinical History")
async def download_history(
    num_document: str, request: Request, current_user: NonPatient
) -> FileResponse:
    """
    Obtiene la historia clínica de un determinado paciente en un archivo .txt
    """
    start_time = perf_counter()
    file = crud_document.get_file(num_document, settings.HISTORY_FILENAME)
    if file is None:
        raise exceptions.patient_not_found
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return file


@router.get("/histories", summary="Get Clinical Histories")
async def get_histories(request: Request, current_user: NonPatient) -> list[str]:
    """
    Obtiene todas las historias clínicas de todos los pacientes
    """
    start_time = perf_counter()
    histories = crud_document.get_histories()
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return histories


@router.get("/orders/{num_document}")
async def get_orders(
    num_document: str, request: Request, current_user: NonPatient
) -> schemas.Files:
    """
    Obtiene todas las órdenes médicas de un determinado paciente
    """
    start_time = perf_counter()
    orders = crud_document.get_files(num_document, "orders")
    if orders is None:
        raise exceptions.patient_not_found
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return orders


@router.get("/orders/{num_document}/{filename}")
async def download_order(
    num_document: str, filename: str, request: Request, current_user: NonPatient
) -> FileResponse:
    """
    Obtiene un archivo de una orden médica de un determinado paciente
    """
    start_time = perf_counter()
    file = crud_document.get_file(num_document, filename, 1)
    if file is None:
        raise exceptions.patient_not_found
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return file


@router.get("/results/{num_document}")
async def get_results(
    num_document: str, request: Request, current_user: NonPatient
) -> schemas.Files:
    """
    Obtiene todos los resultados de los examenes médicos para un determinado paciente
    """
    start_time = perf_counter()
    results = crud_document.get_files(num_document, "results")
    if results is None:
        raise exceptions.patient_not_found
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return results


@router.get("/results/{num_document}/{filename}")
async def download_result(
    num_document: str, filename: str, request: Request, current_user: NonPatient
) -> FileResponse:
    """
    Obtiene un archivo de un resultado médico de un determinado paciente
    """
    start_time = perf_counter()
    file = crud_document.get_file(num_document, filename, 2)
    if file is None:
        raise exceptions.patient_not_found
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return file


@router.put("/histories/{num_document}", summary="Update Clinical History")
async def update_history(
    num_document: str,
    request: Request,
    current_user: Doctor,
    history: UploadFile = File(...),
) -> schemas.ApiResponse:
    """
    Actualiza la historia clínica de un determinado paciente
    """
    start_time = perf_counter()
    if os.path.splitext(history.filename)[1] not in settings.ALLOWED_EXTENSIONS_HISTORY:
        print(1, history.filename)
        raise exceptions.file_extention_not_allowed

    out = await crud_document.update_history(num_document, history)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_500_INTERNAL_SERVER_ERROR, *log_data)
        raise exceptions.failed_to_save_historial
    if out == 2:
        await log_request(request, status.HTTP_500_INTERNAL_SERVER_ERROR, *log_data)
        raise exceptions.failed_to_save_file
    if out == 3:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    await log_request(request, status.HTTP_200_OK, *log_data)
    return schemas.ApiResponse(detail="Historia clínica actualizada correctamente")


@router.post("/{num_document}", status_code=status.HTTP_201_CREATED)
async def add_file(
    num_document: str,
    kind: schemas.KindFiles,
    request: Request,
    current_user: Doctor,
    file: UploadFile = File(...),
) -> schemas.ApiResponse:
    """
    Agrega un documento médico (ya sea orden o resultados de un examen) a un determinado paciente
    """
    start_time = perf_counter()
    allowed_extensions = (
        settings.ALLOWED_EXTENSIONS_ORDERS
        if kind == "orders"
        else settings.ALLOWED_EXTENSIONS_RESULTS
    )

    if os.path.splitext(file.filename)[1] not in allowed_extensions:
        raise exceptions.file_extention_not_allowed

    out = await crud_document.add_file(num_document, kind, file)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_500_INTERNAL_SERVER_ERROR, *log_data)
        raise exceptions.failed_to_save_order
    if out == 2:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    await log_request(request, status.HTTP_201_CREATED, *log_data)
    return schemas.ApiResponse(detail="Archivo agregado correctamente")


@router.delete("/{num_document}")
async def delete_file(
    num_document: str,
    filename: str,
    kind: schemas.KindFiles,
    request: Request,
    current_user: NonPatient,
) -> schemas.ApiResponse:
    """
    Elimina un archivo médico de un determinado paciente (no incluye la historia clínica)
    """
    start_time = perf_counter()
    out = crud_document.delete_file(num_document, filename, kind)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_500_INTERNAL_SERVER_ERROR, *log_data)
        raise exceptions.failed_to_found_file
    if out == 2:
        await log_request(request, status.HTTP_500_INTERNAL_SERVER_ERROR, *log_data)
        raise exceptions.failed_to_delete_file
    if out == 3:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    await log_request(request, status.HTTP_200_OK, *log_data)
    return schemas.ApiResponse(detail="Archivo eliminado correctamente")
