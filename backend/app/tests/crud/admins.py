from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password

from app.tests.utils.utils import random_document, random_password
from app.tests.utils.user import create_random_user
from app.tests.utils.hospitalizations import create_random_hospitalization
from app.tests.utils.user import non_existent_document

from app import schemas
from app.crud import crud_admin


def test_create_user(db: Session) -> None:
    rol = 'admin'
    name, surname = 'Jhon', 'Doe'
    new_user = schemas.UserCreate(num_document=settings.FIRST_SUPERUSER,
                                  rol=rol,
                                  password=settings.FIRST_SUPERUSER_PASSWORD)

    out = crud_admin.create_user(new_user, db)
    assert out == 1

    out = crud_admin.create_user(new_user, db, True)
    assert out == 2

    num_document = random_document()
    password = random_password(10)
    new_user = schemas.UserCreate(num_document=num_document,
                                  rol=rol,
                                  password=password,
                                  name=name,
                                  surname=surname)
    
    # Puede darse el caso improbable de que sin querer se cree un usuario ya existente
    out = crud_admin.create_user(new_user, db, True)
    assert out == 0 or out == 2
    
    user_search = schemas.UserSearch(num_document=num_document, rol=rol)
    # Verificar que los parametros que se tomaron estén bien definidos
    user_rol_in = crud_admin.get_user_rol(user_search, db)
    user_info_in = crud_admin.get_user_info(num_document, db)
    assert verify_password(password, user_rol_in.password)
    assert num_document == user_rol_in.num_document
    assert rol == user_rol_in.rol
    assert user_info_in.name == name
    assert user_info_in.surname == surname

    # Comprobar si se restaura el estado de actividad del usuario cuando se crea nuevamente
    crud_admin.delete_user(user_search, db, True)
    
    user_rol_in = crud_admin.get_user_rol(user_search, db, False)
    assert user_rol_in.is_active == False

    out = crud_admin.create_user(new_user, db, True)
    user_rol_in = crud_admin.get_user_rol(user_search, db, False)
    assert user_rol_in.is_active == True


def test_update_basic_info(db: Session) -> None:
    rol = 'admin'
    num_document = create_random_user(rol, db, 10).num_document
    
    new_password = 'supersecure123'
    new_email = 'randomemail@test.com'

    user_search = schemas.UserSearch(num_document=num_document, rol=rol)
    updated_info = schemas.UserUpdate(password=new_password, email=new_email)

    out = crud_admin.update_basic_info(user_search, updated_info, db)
    assert out == 0

    user_rol_in = crud_admin.get_user_rol(user_search, db)
    user_info_in = crud_admin.get_user_info(num_document, db)
    assert verify_password(new_password, user_rol_in.password)
    assert user_info_in.email == new_email

    user_search = schemas.UserSearch(num_document=non_existent_document, rol=rol)
    updated_info = schemas.UserUpdate(password=new_password, email=new_email)

    out = crud_admin.update_basic_info(user_search, updated_info, db)
    assert out == 0


def test_update_user(db: Session) -> None:
    rol = 'admin'
    num_document = create_random_user(rol, db, 10).num_document
    new_document = 'new_document'
    new_password = 'supersecure123'
    new_email = 'randomemail@test.com'

    user_search = schemas.UserSearch(num_document=non_existent_document, rol=rol)
    updated_info = schemas.UserUpdateAll(password=new_password, num_document=settings.FIRST_SUPERUSER)

    out = crud_admin.update_user(user_search, updated_info, db)
    assert out == 1

    user_search = schemas.UserSearch(num_document=num_document, rol=rol)
    out = crud_admin.update_user(user_search, updated_info, db)
    assert out == 2

    out = crud_admin.update_user(user_search, updated_info, db, True)
    assert out == 3

    new_document = random_document()
    updated_info = schemas.UserUpdateAll(password=new_password, num_document=new_document, email=new_email)
    out = crud_admin.update_user(user_search, updated_info, db, True)
    assert out == 0
    
    user_info_in = crud_admin.get_user_info(num_document, db)
    user_rol_in = crud_admin.get_user_rol(user_search, db)
    assert user_info_in.num_document == new_document
    assert user_info_in.email == new_email
    assert verify_password(new_password, user_rol_in.password)


def test_authenticate_user(db: Session) -> None:
    # Verificar si sí existe el superusuario
    num_document = settings.FIRST_SUPERUSER
    password = settings.FIRST_SUPERUSER_PASSWORD
    rol = 'admin'

    user_login = schemas.UserLogin(num_document=num_document, password=password, rol=rol)
    user_in = crud_admin.authenticate_user(user_login, db)

    assert user_in is not None
    assert user_in.num_document == num_document
    assert user_in.rol == 'admin'

    # Crear 3 usuarios diferentes en cada posible rol
    for rol in ('admin', 'doctor', 'patient'):
        new_user = create_random_user(rol, db, 10)
        num_document, password = new_user.num_document, new_user.password
        
        user_login = schemas.UserLogin(num_document=num_document, password=password, rol=rol)
        user_in = crud_admin.authenticate_user(user_login, db)

        assert user_in is not None
        assert user_in.num_document == num_document
        assert user_in.rol == 'admin'


def test_get_user(db: Session) -> None:
    rol = 'admin'
    num_document = create_random_user(rol, db, 10).num_document

    user_in = crud_admin.get_user(num_document, db)
    assert isinstance(user_in, schemas.UserBase)
    assert num_document == user_in.num_document

    user_in = crud_admin.get_user(num_document, db, rol=True)
    assert isinstance(user_in, schemas.UserAll)
    assert num_document == user_in.num_document

    user_search = schemas.UserSearch(num_document=num_document, rol=rol)
    crud_admin.delete_user(user_search, db, True)
    user_in = crud_admin.get_user(num_document, db)
    assert user_in is None

    user_in = crud_admin.get_user(non_existent_document, db)
    assert user_in is None


def test_delete_user(db: Session) -> None:
    rol = 'admin'
    num_document = settings.FIRST_SUPERUSER
    
    user_search = schemas.UserSearch(num_document=non_existent_document, rol=rol)
    out = crud_admin.delete_user(user_search, db)
    assert out == 1
    
    user_search = schemas.UserSearch(num_document=num_document, rol=rol)
    out = crud_admin.delete_user(user_search, db)
    assert out == 2

    hospitalization = create_random_hospitalization(db)
    user_search = schemas.UserSearch(num_document=num_document, rol='patient')

    out = crud_admin.delete_user(user_search, db)
    assert out == 3

    user_search = schemas.UserSearch(num_document=hospitalization.num_doc_doctor, rol='doctor')
    out = crud_admin.delete_user(user_search, db)
    assert out == 0

    num_document = create_random_user(rol, db, 10).num_document
    user_search = schemas.UserSearch(num_document=num_document, rol=rol)
    out = crud_admin.delete_user(user_search, db, True)
    assert out == 0
