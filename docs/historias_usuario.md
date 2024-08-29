# Historias de usuario

## Historia de usuario N°1

### Descripción

Como Administrador, quiero poder observar los indicadores de ocupación y flujo de pacientes para tomar decisiones administrativas con base a información real y actualizada del hospital. 

### Criterios de aceptación

* Es posible observar los indicadores de ocupación del hospital, tales como la cantidad de camas utilizadas y disponibles. 
* Se puede consultar el flujo de pacientes (cantidad de visitantes) de cada día y mes dentro del hospital.
* Es posible consultar el promedio de estancia interna por servicio, la cantidad de admisiones y la cantidad de altas por servicio. 

## Historia de usuario N°2

### Descripción

Como Administrador, quiero poder gestionar los usuarios (crear, actualizar y enviar a desuso) para registrar dentro de la plataforma a todos los individuos que utilizan nuestros servicios. 

### Criterios de aceptación

* Es posible la creación, actualización de datos y el cambio de estado (activo - inactivo) de nuevos usuarios de clientes y doctores por parte de los usuarios administradores.
* Es posible reconocer a cada usuario conociendo su identificador y contraseña.
* A la hora de crear un usuario, es posible personalizarlo ingresando los datos personales de un individuo. 

## Historia de usuario N°3

### Descripción

Como Administrador, quiero poder gestionar las camas disponibles dentro del hospital, para mantener actualizada la plataforma con respecto a las condiciones reales de la institución. 

### Criterios de aceptación

* Los usuarios administradores son capaces de aumentar y disminuir la cantidad de camas existentes en la plataforma.
* Los usuarios administradores pueden acceder a la información de las camas.
* Los usuarios administradores no pueden eliminar las camas que están en uso.

## Historia de usuario N°4

### Descripción

Como Doctor, me gustaría ser capaz de ingresar a los pacientes según su tipo de cita para evitar confusiones dentro de las historias clínicas y el uso innecesario de camas hospitalarias. 

### Criterios de aceptación

* Los usuarios doctores son capaces de registrar visitas de pacientes como citas u emergencias.
* Las citas no ocuparán camas hospitalarias.

## Historia de usuario N°5

### Descripción

Como Doctor, me gustaría poder consultar y actualizar las historias médicas de los pacientes para estar al tanto de su información personal y evolución médica. 

### Criterios de aceptación

* Los usuarios doctores son capaces de consultar y actualizar las historias clínicas de los clientes.
* Las actualizaciones de historias clínicas permanecen en el sistema.

## Historia de usuario N°6

### Descripción 

Como doctor, me gustaría poder consultar los exámenes de los pacientes almacenados en el sistema y ser capaz de cargar nuevos para tener información actualizada de los resultados de los exámenes realizados. 

### Criterios de aceptación

* Los usuarios doctores son capaces de consultar y almacenar nuevos exámenes dentro de la plataforma.
* Los exámenes de cada usuario deben estar diferenciados entre sí, de tal forma que sea posible consultar de forma aislada todos los exámenes de un único usuario.
* Los exámenes de cada usuario deben permanecer en el sistema a través del tiempo.

## Historia de usuario N°7

### Descripción

Como doctor, me gustaría poder consultar y crear nuevas órdenes médicas asociadas a mis pacientes para facilitar las recomendaciones de medicamentos y exámenes previas y futuras. 

### Criterios de aceptación

* Los usuarios doctores son capaces de crear y consultar las órdenes médicas asociadas a cada paciente.
* Las órdenes médicas deben estar relacionadas a un y solo un paciente, de forma que puedan ser consultadas de forma individual.
* Las órdenes médicas de cada usuario deben permanecer en el sistema a través del tiempo.

## Historia de usuario N°8

### Descripción

Como paciente, me gustaría poder acceder a mi usuario y ver mis exámenes e historia médica dentro de la plataforma para estar consciente de mis resultados y las recomendaciones de los doctores. 

### Criterios de aceptación

* Los usuarios catalogados como pacientes son capaces de acceder a su usuario privado mediante su identificación y contraseña.
* Al acceder a un usuario de paciente deben ser accesible tanto la historia médica como los exámenes registrados en la plataforma correspondientes a él.

## Historia de usuario N°9

### Descripción

Como paciente, me gustaría que mis datos no sean accesibles para otros pacientes, con el objetivo de mantener mi privacidad y seguridad. 

### Criterios de aceptación

* Las historias médicas, órdenes y exámenes solo son consultables por los doctores, administrativos y el paciente al que corresponden. Es imposible para un cliente acceder a un examen, órden o historia que no es suyo.
