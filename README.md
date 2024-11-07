# AG-GestionHospitalaria

## Contexto del caso

Un hospital cuenta con una capacidad de más de 300 camas (en constante expansión) y atiende alrededor de 1.000 pacientes al día.Actualmente,el hospital almacena las historias clínicas de los pacientes en archivos físicos que se guardan en el área de Archivo. Cuando un médico necesita consultar la historia de un paciente, debe solicitar el archivo al área de Archivo y esperar a que le sea entregado.Esto genera una serie de problemas, tales como. Demoras en la atención, ya que se debe esperar la entrega física de la historia clínica. En promedio se tarda 20 minutos. Riesgos de extravío de historias clínicas, lo cual sucede aproximadamente en el 5% de las solicitudes. Dificultades para compartir en tiempo real información de un paciente entre médicos de diferentes especialidades. Imposibilidad de generar reportes y estadísticas a partir de los datos de las historias clínicas.

El hospital desea desarrollar un sistema de información que permita digitalizar y centralizar las historias clínicas de los pacientes, de forma que estén disponibles en línea para los médicos autorizados y se pueda obtener información para la gestión hospitalaria. El producto mínimo viable que se requiere es; gestionar historia clínica electrónica de cada paciente, generar reportes de indicadores como: porcentaje de ocupación hospitalaria, promedios de estancia por servicio, cantidad de admisiones y altas por servicio.

Los datos que se le solicitarán a los pacientes son los siguiente:

- Datos del paciente (documento, nombre, sexo, fecha nacimiento)
- Signos vitales (presión arterial, temperatura, saturación O2, frecuencia respiratoria)
- Notas de evolución
- Imágenes diagnósticas
- Resultados de exámenes de laboratorio

Los beneficios que se logran con dicha aplicación son tales como el acceso rápido a la información de los pacientes, mejor coordinación entre especialidades médicas, reducción del riesgo de pérdida de historias clínicas y toma de decisiones gerenciales basada en datos.

## Docker

Para ejecutar el proyecto se necesita tener instalado Docker previamente en el equipo. Una vez instalado, se puede ejecutar el siguiente comando para construir el contenedor:

```bash
docker compose build
docker compose up
```

O en una sola línea:

```bash
docker compose up --build
```

Sin embargo, hay que tener en cuenta sobre todo el sistema operativo que se está usando. Puesto que, para el desarrollo del backend se está utilizando como sistema operativo Ubuntu, entonces para sistemas basados en UNIX no hay ninguna diferencia en la ejecución de los comandos anteriores. No obstante, en Windows, se debe tener en cuenta el detalle de que los sistemas basados en UNIX tienen diferentes terminaciones de línea, con ayuda de editores de texto avanzados como Visual Studio Code, se puede solucionar este error tan fácilmente como cambiando la terminación de línea a LF en el archivo [`prestart.sh`](./backend/scripts/prestart.sh).
