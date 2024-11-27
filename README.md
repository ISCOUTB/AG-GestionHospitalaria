# AG-GestionHospitalaria ![Coverage](https://img.shields.io/badge/Coverage-77%25-brightgreen.svg)

## Contexto del caso

Un hospital cuenta con una capacidad de más de 300 camas (en constante expansión) y atiende alrededor de 1.000 pacientes al día.Actualmente,el hospital almacena las historias clínicas de los pacientes en archivos físicos que se guardan en el área de Archivo. Cuando un médico necesita consultar la historia de un paciente, debe solicitar el archivo al área de Archivo y esperar a que le sea entregado.Esto genera una serie de problemas, tales como. Demoras en la atención, ya que se debe esperar la entrega física de la historia clínica. En promedio se tarda 20 minutos. Riesgos de extravío de historias clínicas, lo cual sucede aproximadamente en el 5% de las solicitudes. Dificultades para compartir en tiempo real información de un paciente entre médicos de diferentes especialidades. Imposibilidad de generar reportes y estadísticas a partir de los datos de las historias clínicas.

El hospital desea desarrollar un sistema de información que permita digitalizar y centralizar las historias clínicas de los pacientes, de forma que estén disponibles en línea para los médicos autorizados y se pueda obtener información para la gestión hospitalaria. El producto mínimo viable que se requiere es; gestionar historia clínica electrónica de cada paciente, generar reportes de indicadores como: porcentaje de ocupación hospitalaria, promedios de estancia por servicio, cantidad de admisiones y altas por servicio.

Los beneficios que se logran con dicha aplicación son tales como el acceso rápido a la información de los pacientes, mejor coordinación entre especialidades médicas, reducción del riesgo de pérdida de historias clínicas y toma de decisiones gerenciales basada en datos.

## Tecnologías

Las tecnologias utilizadas para el desarrollo del proyecto fueron las siguientes:

- [FastAPI](https://fastapi.tiangolo.com). Para el desarrollo de la API en Python.
  - [Pydantic](https://docs.pydantic.dev). Para las validaciones de datos y manejo de las configuraciones del sistema.
  - [Sqlalchemy](https://www.sqlalchemy.org). Para la interacción de la base de datos en SQL.
  - [Alembic](https://alembic.sqlalchemy.org/en/latest/). Para las migraciones a la base de datos.
  - [Postgres](https://www.postgresql.org). Base de datos en SQL para almacenar la información esencial del hospital (usuarios, camas, etc.)
  - [Mongo](https://www.mongodb.com/es). Base de datos noSQL para almacenar el historial de movimientos de la API.
- [Docker Compose](https://www.docker.com). Para el desarrollo y producción de la aplicación.
- Encriptación de contraseñas de usuarios por defecto, utilizando bcrypt.
- JWT. Para la autenticación de credenciales.
- [Pytest](https://docs.pytest.org/en/stable/). Para las pruebas unitarias.

## Docker

Para ejecutar el proyecto se necesita tener instalado Docker previamente en el equipo. Una vez instalado, se puede ejecutar los siguientes comandos para construir los contenedores:

```bash
docker compose build
docker compose up
```

O en una sola línea:

```bash
docker compose up --build
```

### Networks

Dentro de [`docker-compose.yml`](./docker-compose.yml) se está utilizando las redes `ag`, por lo tanto, se deben crear la red `ag` antes de ejecutar los comandos anteriores.

```bash
docker network create ag
```

Este comando se debe ejecutar una vez para crear la red `ag`, no hace falta volver a ejecutarlo si ya se ha creado.

### Terminación de líneas LF

Se debe tener en cuenta sobre todo el sistema operativo que se está usando, puesto que, para el desarrollo del backend se está utilizando Ubuntu como sistema operativo, lo que implica que para sistemas basados en UNIX no existe ninguna diferencia en la ejecución de los comandos anteriores. No obstante, en Windows, se debe tener en cuenta el detalle de que los sistemas basados en UNIX tienen diferentes terminaciones de línea, con ayuda de editores de texto avanzados como Visual Studio Code, se puede solucionar este error tan fácilmente como cambiando la terminación de línea a LF en el archivo [`prestart.sh`](./backend/scripts/prestart.sh) principalmente, porque esto influye en la construcción de los contenedores, pero si llegan a ver errores ejecutando otros scripts, es posible que esté fallando por el mismo motivo.
