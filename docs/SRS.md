# Software Requirements Specification
## For App Gestión Hospitalaria
Version 0.1
Universidad Tecnologica de Bolivar
26/08/2024

# Table of Contents
- Revision History
 - 1 Introduction
 - 1.1 Document Purpose
 - 1.2 Product Scope
 - 1.3 Definitions, Acronyms and Abbreviations
 - 1.4 Document Overview
- 2 Product Overview
 - 2.1 Product Perspective
 - 2.2 Product Functions
 - 2.3 Product Constraints
 - 2.4 User Characteristics
 - 2.5 Assumptions and Dependencies
 - 2.6 Apportioning of Requirements
- 3 Requirements
 - 3.1 External Interfaces
  - 3.1.1 User Interfaces
  - 3.1.2 Hardware Interfaces
  - 3.1.3 Software Interfaces
 - 3.2 Functional

## 1. Introduction
### 1.1 Document Purpose
Este documento detalla los requisitos funcionales y no funcionales para el sistema de gestión hospitalaria "App Gestión Hospitalaria". Su objetivo es proporcionar una referencia clara para el desarrollo, mantenimiento y mejora del sistema.

### 1.2 Product Scope
El sistema "App Gestión Hospitalaria" tiene como propósito principal gestionar las operaciones diarias de un hospital, permitiendo la administración eficiente de camas, historias clínicas, y otros aspectos clave del funcionamiento hospitalario.

### 1.3 Definitions, Acronyms and Abbreviations
SRS: Software Requirements Specification
EHR: Electronic Health Record
HIS: Hospital Information System


### 1.4 Document Overview
Este documento está organizado en secciones que cubren desde la visión general del sistema hasta los detalles específicos de los requisitos funcionales y no funcionales para nuestra aplicacion web centrada en la gestion de un sistema hospitalario.

## 2. Product Overview
### 2.1 Product Perspective
El sistema es una aplicación independiente que formará parte de la infraestructura tecnológica del hospital, integrándose con otros sistemas existentes.

### 2.2 Product Functions
Las principales funcionalidades del sistema incluyen la gestión de camas, historias clínicas, programación de citas, facturación y reportes médicos.

### 2.3 Product Constraints
Cumplimiento con las normativas de privacidad de datos de salud.
La necesidad de alta disponibilidad y escalabilidad.
### 2.4 User Characteristics
Los usuarios incluyen administradores, personal médico y de soporte, con diferentes niveles de acceso y responsabilidades.

### 2.5 Assumptions and Dependencies
Se asume que los usuarios tendrán un conocimiento básico en el uso de computadoras y software hospitalario.
El sistema dependerá de una infraestructura de red segura y confiable.
### 2.6 Apportioning of Requirements
Algunos requisitos, como los relacionados con la seguridad y la escalabilidad, podrán ser implementados en fases posteriores dependiendo de las prioridades y necesidades del hospital.

## 3. Requirements
### 3.1 External Interfaces
#### 3.1.1 User Interfaces
El sistema ofrecerá interfaces gráficas accesibles desde cualquier navegador web moderno, con diseño intuitivo y responsivo.

#### 3.1.2 Hardware Interfaces
El sistema interactuará con los comptadores del hospital y hardware de red existentes en el hospital.

#### 3.1.3 Software Interfaces
Se integrará con otros sistemas de información hospitalaria (HIS) y registros electrónicos de salud (EHR).

## 3.2 Functional
### Gestión de camas
**ID:** REQ-001

**Descripción:** El sistema debe permitir gestionar las camas disponibles dentro del hospital.

**Requisitos funcionales:**

- REQ-001.1: El sistema debe permitir que se puedan agregar nuevas camas.
- REQ-001.2: El sistema debe permitir que se puedan actualizar el estado de la cama de los pacientes hospitalizados: ocupado o desocupado.
- REQ-001.3: El sistema debe permitir que se puedan eliminar camas.
- REQ-001.4: El sistema debe ser capaz de obtener el estado de todas las camas dentro del hospital.

**Prioridad:** Alta

**Dependencias:** Ninguna

**Notas:** Este requerimiento es esencial para el correcto funcionamiento del hospital y debe implementarse desde la fase inicial de desarrollo.

### Gestión de historias clínicas
**ID:** REQ-002

**Descripción:** El sistema es capaz de gestionar la historia clínica de los pacientes, almacenando a través del tiempo toda su información de visitas y procedimientos de forma organizada y accesible.

**Requisitos funcionales:**

- REQ-002.1: El sistema debe ser capaz de crear nuevas historias clínicas a los nuevos pacientes del sistema.
- REQ-002.2: El sistema debe permitir que los doctores sean capaces de actualizar la historia clínica de los pacientes ya existentes en el sistema.
- REQ-002.3: El sistema debe permitir que los doctores puedan obtener las historias clínicas de sus pacientes. Además, los pacientes también pueden acceder a sus propias historias clínicas.
- REQ-002.4: El sistema debe ser capaz de almacenar las historias clínicas de los pacientes del hospital sin riesgo de pérdidas.
- REQ-002.5: El sistema debe permitir la consulta de las historias clínicas por medio de diversos criterios (número de documento de identidad del paciente, tipo de documento de identidad, nombre del paciente, última fecha de consulta, etc.).

**Prioridad:** Alta

**Dependencias:** Ninguna

**Notas:** Es crucial garantizar la seguridad y disponibilidad de la información clínica en todo momento.
### Reporte de indicadores

**ID:** REQ-003

**Descripción:** El sistema debe emitir un reporte de los indicadores del hospital, como su ocupación, días con mayor flujo de pacientes en el año, horas con mayor flujo de pacientes en un dia, etc.

**Requisitos funcionales:**

- REQ-003.1: El sistema debe mantener un registro del flujo del hospital, lo cual incluye mantener registro del uso de las camas en tiempo real y durante periodos de tiempo especificos.
- REQ-003.2: El sistema debe identificar los días con mayor flujo de pacientes en el año.
- REQ-003.3: El sistema debe generar reportes de la estancia promedio por servicio.
- REQ-003.4: El sistema debe dar informes de la cantidad de admisiones y altas por día.

**Prioridad:** Media

**Dependencias:** El usuario debe ser un administrador (REQ-006)

**Notas:** Este requerimiento es esencial para la toma de decisiones basada en los reportes estadísticos del hospital.

### Diferenciación de pacientes

**ID:** REQ-004

**Descripción:** El sistema debe ser capaz de diferenciar el motivo por el cual un paciente puede ser ingresado al hospital, ya sea consulta o urgencia, donde las consultas no requieren el uso de una cama del hospital.

**Requisitos funcionales:**

- REQ-004.1: El sistema permite clasificar a los pacientes como "consulta" o "urgencia" al momento de su ingreso al hospital.
- REQ-004.2: El sistema no debe asignar cama a los pacientes ingresados como "consulta".
- REQ-004.3: El sistema debe asignar cama a los pacientes ingresados como "urgencia".
- REQ-004.4: El sistema debe permitir el cambio de clasificación de un paciente de "consulta" a "urgencia" si el doctor lo ve necesario.

**Prioridad:** Alta

**Dependencias:** Depende del correcto funcionamiento de la gestión de cama dentro del hospital (REQ-001)

**Notas:** Este requerimiento es crucial para la gestión eficiente de los recursos hospitalarios y la priorización adecuada de la atención médica.

### Gestión de usuarios

**ID:** REQ-005

**Descripción:** El sistema debe ser capaz de realizar operaciones CRUD sobre los usuarios del sistema, asegurando la privacidad y seguridad de los datos privados. Además, debe diferenciar entre administradores, personal médico y pacientes.

**Requisitos funcionales:**

- REQ-005.1: El sistema debe permitir a los administradores la creación de nuevos usuarios en el sistema, especificando la información esencial (número de documento de identificación, tipo de documento de identificación, nombre completo, fecha de nacimiento y sexo), rol, contraseña, teléfono de contacto y email.
- REQ-005.2: El sistema debe permitir a los usuarios la actualización de su información no esencial (a excepción del rol).
- REQ-005.3: El sistema no debe eliminar a los usuarios de manera inmediata, debe mantener a los usuarios durante cierto periodo de tiempo como "inactivos"
- REQ-005.4: El sistema debe implementar mecanismos de seguridad para el almacenamiento de contraseñas dentro de la base de datos.
- REQ-005.5: El sistema debe mantener un registro de acciones realizadas por cada usuario.
- REQ-005.6: El sistema debe asegurar el correcto almacenamiento de los usuarios del sistemas.

**Prioridad:** Alta

**Dependencias:** Ninguna

**Notas:** Este requerimiento es fundamental para garantizar la seguridad y la privacidad de los datos en el sistema. Debe implementarse en las primeras etapas del desarrollo. Además, el sistema no debe permitir a los usuarios actualizar toda su información, puesto que se podrían generar problemas de integridad en un futuro.

### Permisos según el rol

**ID:** REQ-006

**Descripción:** El sistema debe ser capaz de asignar diferentes permisos a los usuarios del sistema dependiendo de su rol (administradores, personal médico y pacientes).

**Requisitos funcionales:**

- REQ-006.1: El sistema debe restringir el acceso a funcionalidades específicas basándose en el rol del usuario autenticado.
- REQ-006.2: El sistema debe permitir a los administradores acceder a todas las funcionalidades de la gestión de usuarios, a la generación de reportes y a las modificaciones de la cantidad de camas dentro del hospital.
- REQ-006.3: El sistema debe permitir al personal médico gestionar los documentos médicos de los pacientes (historias clínicas, ordenes médicas y resultados de exámenes médicos). Además, podrá ingresar a los pacientes y decidir si estos necesitan cama o no.
- REQ-006.4: El sistema debe permitir al paciente acceder a sus documentos médicos.

**Prioridad:** Alta

**Dependencias:** Depende del correcto funcionamiento de la gestión de usuarios dentro del sistema (REQ-005)

**Notas:** Este requerimiento es esencial para mantener la confidencialidad de la información y asegurar que cada usuario solo tenga acceso a las funcionalidades necesarias para su rol. El personal médico no podrá eliminar ninguno de estos documentos, solo podrá obtenerlos del sistemos, subirlos al sistema y podrá subir las actualizaciones de las historias clínicas.

### Generación de alertas

**ID:** REQ-007

**Descripción:** El sistema generará alertas de manera automática cuando los niveles de ocupación de las camas supere cierto umbral, que puede ser determinado por los administradores del sistema.

**Requisitos funcionales:**

- REQ-007.1: El sistema debe permitir a los administradores definir el valor umbral.
- REQ-007.2: El sistema debe generar alertas automáticas cuando los niveles de ocupación de las camas supere el valor umbral.
- REQ-007.3: El sistema debe mostrar la alerta en la interfaz a todas las sesiones de los administradores cuando estos entren a la plataforma.
- REQ-007.4: El sistema debe permitir a los administradores avisar al personal médico para que utilicen mejor los recursos del hospital.

**Prioridad:** Media

**Dependencias:** Depende del correcto funcionamiento de la gestión de usuarios (REQ-005), de los permisos según el rol (REQ-006) y de la gestión de camas (REQ-001)

**Notas:** Este requerimiento es importante para la gestión de los recursos hospitalarios y la respuesta rápida a situaciones críticas.

### Almacenamiento de datos

**ID:** REQ-008

**Descripción:** El sistema debe implementar un sistema robusto para el almacenamiento a largo plazo de toda la información del hospital (incluyendo usuarios, documentos médicos del paciente, etc.).

**Requisitos funcionales:**

- REQ-008.1: El sistema debe utilizar PostgreSQL como sistema gestor de bases de datos para mantener un registro de los usuarios.
- REQ-008.2: El sistema debe implementar una servicio de archivos para mantener persistencia de los documentos médicos de los pacientes.
- REQ-008.3: El sistema debe garantizar la integridad referencial entre todas las tablas y bases de datos utilizadas
- REQ-008.4: El sistema debe permitir la exportación de datos en formatos estándar.
- REQ-008.5: El sistema debe mantener un registro de todas las consultas y modificaciones a la base de datos.
- REQ-008.6: El sistema debe trabajar de manera armónica entre diferentes bases de datos, puesto que se está utilizando una arquitectura de microservicios.

**Prioridad:** Alta

**Dependencias:** Ninguna

**Notas:** Este requerimiento es fundamental para la persistencia y seguridad de los datos del sistema

## Requerimientos no funcionales

### Lenguaje de desarrollo backend

**ID:** RNF-001

**Descripción:** El lenguaje de programación que se utilizará para desarrollar el backend del sistema será en Python

**Especificaciones:**

- RNF-001.1: Todo el código backend será escrito en la versión más reciente y estable de Python 3.12 hasta la fecha.
- RNF-001.2: Para la implementación de APIs dentro del backend, se utilizará el framework de FastAPI, junto a otras bibliotecas que permitan una buena integración, como SQLAlchemy para la integración con bases de datos SQL.
- RNF-001.3: El código debe seguir con las mejores prácticas y convenciones de Python, como las PEP8

**Criterios de aceptación:**

- Todo el código backend debe pasar la validación de SonarCloud.

**Prioridad:** Alta

### Lenguaje de desarrollo frontend

**ID:** RNF-002

**Descripción:** Para el desarrollo frontend del sistema se utilizará JavaScript con el framework de Next.js y Tailwind CSS para los estilos

**Especificaciones:**

- RNF-002.1: El frontend debe ser desarrollado utilizando JavaScript moderno, con Next.js como framework principal.
- RNF-002.2: Tailwind CSS debe ser utilizado como el framework de CSS para el diseño y el estilo de la interfaz de usuario.
- RNF-002.3: El código debe seguir con las mejores prácticas y patrones de diseño recomendado para aplicaciones Next.js
- RNF-002.4: Se debe asegurar la compatibilidad de Prisma para la interacción con las bases de datos.

**Criterios de aceptación:**

- Todo el código backend debe pasar la validacion de SonarCloud.
- La aplicación debe funcionar correctamente en los navegadores web modernos más utilizados actualmente
- La plataforma debe presentar rápidos tiempos de respuesta en la interacción con el usuario.

**Prioridad:** Alta

### Seguridad y privacidad de datos

**ID:** RNF-003

**Descripción:** El sistema debe implementar medidas robustas de seguridad y privacidad para proteger la información sensible de los pacientes y cumplir con las regulaciones de protección de datos personales en salud.

**Especificaciones:**

- RNF-003.1: El sistema debe implementar autenticación segura para todos los usuarios que tengan acceso a los datos sensibles.
- RNF-003.2: Se debe mantener un registro de auditoría detallado de todos los accesos y modificaciones a los datos de los pacientes.
- RNF-003.3: Se deben implementar mecanismos de control de acceso basados en roles para asegurar que los usuarios solo puedan acceder a la información necesaria para su función.
- RNF-003.4: Las contraseñas de los usuarios deben ser almacenandas utilizando funciones hash.

**Criterios de aceptación:**

- El sistema debe aprobar una evaluación de seguridad realizada por el equipo de desarrollo.
- Los registros de auditoría deben estar completos y ser inalterables.

**Prioridad:** Alta

### Rendimiento y escalabilidad

**ID:** RNF-006

**Descripción:** El sistema debe ser capaz de manejar altos volúmenes de usuarios concurrentes, manteniendo tiempos de respuesta rápidos y siendo escalable para futuro crecimiento.

**Especificaciones:**

- RNF-006.1: El sistema debe ser capaz de manejar al menos 1000 usuarios concurrentes sin degradación significativa del rendimiento.
- RNF-006.2: Los tiempos de respuesta no deben exceder los 2 segundos bajo carga normal.
- RNF-006.3: Las bases de datos debe ser capaz de manejar cientos de miles de registros en pacientes sin impacto significativo en el rendimiento.

**Criterios de aceptación:**

- Se deben realizar pruebas de estrés y de carga que demuestren que el sistema es capaz de soportar el volumen de usuarios especificado.
- Se debe tener un monitoreo de los tiempos de respuesta para comprobar que se cumplan los tiempos de respuesta especificados.

**Prioridad:** Alta

### Disponibilidad y Fiabilidad

**ID:** RNF-007

**Descripción:** El sistema debe mantener un alto nivel de disponibilidad y fiabilidad, minimizando el tiempo de inactividad y asegurando la integridad de los datos

**Especificaciones:**

- RNF-007.1: El sistema debe tener una buena disponilidad de al menos 95% de las horas de operación normales. 
- RNF-007.2: Se debe contar implementar un sistema de respaldo y recuperación que permita realizar una restauración completa de los datos.
- RNF-007.3: Se deben realizar copias de seguridad incrementales diarias y copias de seguridad completas de todos los datos semanales.

**Criterios de aceptación:**

- Los registros de tiempo de actividad deben demostrar el cumplimiento del objetivo de disponibilidad.
- No debe haber perdida de datos debido a fallos del sistema.

**Prioridad:** Alta



