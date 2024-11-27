# README - Backend

## Estructura

``` bash
.
├── Dockerfile
├── README.md
├── alembic.ini
├── app  # Desarrollo backend de la aplicación
│   ├── __init__.py
│   ├── alembic  # Carpeta para las migraciones a la base de datos
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── a698f22123fe_agregar_tablas_a_la_base_de_datos.py
│   ├── api  # Desarrollo de la api
│   │   ├── __init__.py
│   │   ├── deps.py  # Dependencias de la API
│   │   ├── exceptions  # Excepciones de la API
│   │   │   ├── __init__.py
│   │   │   └── exceptions.py
│   │   ├── main.py
│   │   └── routes  # Rutas y endpoints de la API
│   │       ├── __init__.py
│   │       ├── admins.py
│   │       ├── beds.py
│   │       ├── consultations.py
│   │       ├── doctors.py
│   │       ├── documents.py
│   │       ├── hospitalizations.py
│   │       ├── login.py
│   │       ├── patients.py
│   │       ├── specialities.py
│   │       └── users.py
│   ├── backend_pre_start.py
│   ├── core  # Configuraciones iniciales del backend
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── init_db.py
│   │   └── security.py
│   ├── crud  # Operaciones CRUD
│   │   ├── __init__.py
│   │   ├── admins.py
│   │   ├── base.py
│   │   ├── beds.py
│   │   ├── consultations.py
│   │   ├── doctors.py
│   │   ├── documents.py
│   │   ├── hospitalizations.py
│   │   ├── patients.py
│   │   └── users.py
│   ├── initial_data.py
│   ├── main.py
│   ├── models  # Modelos de la base de datos
│   │   ├── __init__.py
│   │   ├── beds.py
│   │   ├── beds_used.py
│   │   ├── doctor_specialities.py
│   │   ├── hospitalizations.py
│   │   ├── medical_consults.py
│   │   ├── patient_info.py
│   │   ├── specialities.py
│   │   ├── user_roles.py
│   │   └── users_info.py
│   ├── schemas  # Esquemas de la API
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── beds.py
│   │   ├── consults.py
│   │   ├── doctors.py
│   │   ├── documents.py
│   │   ├── models.py
│   │   ├── patient.py
│   │   ├── token.py
│   │   └── users.py
│   ├── stats.py
│   └── tests  # Pruebas unitarias
│       ├── __init__.py
│       ├── api  # Pruebas unitarias en la API
│       │   ├── __init__.py
│       │   └── routes
│       │       ├── __init__.py
│       │       ├── test_admins.py
│       │       ├── test_beds.py
│       │       ├── test_consultations.py
│       │       ├── test_doctors.py
│       │       ├── test_documents.py
│       │       ├── test_hospitalizations.py
│       │       ├── test_login.py
│       │       ├── test_patients.py
│       │       └── test_users.py
│       ├── conftest.py
│       ├── crud  # Pruebas unitarias en las operaciones CRUD
│       │   ├── __init__.py
│       │   ├── admins.py
│       │   ├── beds.py
│       │   ├── consultations.py
│       │   ├── doctors.py
│       │   ├── hospitalizations.py
│       │   └── patients.py
│       └── utils  # Utilidades para las pruebas unitarias
│           ├── __init__.py
│           ├── bed.py
│           ├── doctor.py
│           ├── hospitalizations.py
│           ├── patient.py
│           ├── user.py
│           └── utils.py
├── requirements.txt  # Requerimientos del backend
└── scripts  # Algunos scripts para facilitar algunos procesos
    ├── lint.sh
    ├── prestart.sh
    └── test.sh
```

En resumidas cuentas, dentro de [`models`](./app/models/) se manejan los datos y tablas en la base de datos, para los endpoints de la API está en [`api`](./app/api/), operaciones CRUD en [`crud`](./app/crud/).

## Requerimientos

Para ejecutar la parte backend del proyecto, es necesario instalar las dependencias que se encuentra en el archivo [`requirements.txt`](./requirements.txt), utilizando el comando `pip install -r requirements.txt`. Realmente, no es necesario realizarlo de manera local, puesto que para eso mismo se está utilizando Docker, pero en caso de ser necesario, se también se pueden crear entornos virtuales si así se desea. En caso de querer ejecutarse de manera local, ver [local.md](./local.md).

## Tests

Para ejecutar las pruebas unitarias del backend, está el archivo [`test.sh`](./scripts/test.sh), que en conjunto a docker, las pruebas unitarias se podrían ejecutar de la siguiente forma

``` bash
docker exec -it ag-gestionhospitalaria-backend-1 bash scripts/test.sh
```

Para ello, esto ocasionaría que se generen los archivos html y xml dentro del contenedor de docker, pero ejecutando los siguiente comandos se pueden extraer los archivos y carpetas necesarias

``` bash
backend$docker cp ag-gestionhospitalaria-backend-1:./app/htmlcov .
backend$docker cp ag-gestionhospitalaria-backend-1:./app/coverage.xml .
```

Luego, en los archivos copiados se puede abrir desde el navegador al archivo `htmlcov/index.html`, y ahí se podrá ver un recopilatorio del coverage en cada uno de los archivos.
