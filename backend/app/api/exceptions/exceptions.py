from fastapi import HTTPException, status


create_speciality = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Especialidad no encontrada. Provea una descripción para crearla",
)

bad_date_formatting = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Mal formato de fecha"
)

patient_cannot_be_his_responsable = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Paciente no puede ser su propio responsable",
)

unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autorizado"
)

credentials_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No se pudieron validar las credenciales",
    headers={"WWW-Authenticate": "bearer"},
)

non_superuser = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No tienes los permisos para manipular a un administrador",
)

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
)

doctor_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Doctor no encontrado"
)

patient_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
)

bed_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Cama no encontrada"
)

speciality_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Especialidad no encontrada"
)

responsable_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Información previa del responsable no existente",
)

responsable_found = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Información del responsable ya existente",
)

patient_already_hospitalized = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Paciente ya hospitalizado previamente"
)

bed_already_used = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Cama en uso"
)

room_already_with_bed = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Cama en el cuarto ya especificado"
)

speciality_doctor_not_found = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Relación entre doctor y especialidad no existente",
)

speciality_doctor_found = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Relación existente entre el doctor y la especialidad",
)

patient_cannot_be_responsable = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Responsable no puede ser un paciente activo en el hospital",
)

patient_doctor_same_document = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Paciente y doctor con el mismo documento",
)

num_document_used = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Número de documento en uso"
)

user_found = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Usuario ya registrado en el sistema"
)

patient_in_bed = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="No se puede eliminar a un paciente que esté utilizado en una cama",
)

invalid_email = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email no válido",
)

existent_phone = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="El número de teléfono ya existe en el sistema",
)

failed_to_save_historial = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Error al guardar en el historial de historias clínicas",
)

failed_to_save_file = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Error al guardar el archivo",
)

failed_to_delete_file = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Error al eliminar el archivo",
)

failed_to_found_file = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Archivo no encontrado",
)

file_extention_not_allowed = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="La extensión del archivo no está permitida",
)
