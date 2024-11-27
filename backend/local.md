# Local

Hasta el momento, la información que contendrá este README es acerca de cómo se puede ejecutar la API.

Hay una cosa que debe estar clara, y es que la versión de Python que se está utilizando es la 3.12.7, lo menciono para evitar tener problemas a futuro.

Para saber qué versión de Python están utilizando, pueden ejecutar estos comandos:

```bash
$ python3 -V
Python 3.12.7
```

## Ejecutar

Lo primero que se tiene que realizar es instalar todas las librerias para así asegurar que todo se ejecute sin problemas, para eso, ver [aquí](#entorno-virtual). Una vez instaladas las librerias, es necesario ubicar la consola en esta carpeta, esto lo hacemos con el siguiente comando:

```bash
$ cd backend/
backend$ 
```

Ya una vez ubicados, dentro del archivo [main.py](./app/main.py) hay un apartado donde se está recopilando toda la API. Entonces, la manera en la que se puede ejecutar ese archivo sin que haya problemas con las librerias es así:

```bash
(.venv) backend$ uvicorn app.main:app --host=0.0.0.0 --port=8001 --reload
INFO:     Started server process [16200]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

Aquí yo estoy utilizando bash, puesto que se está utilizando Ubuntu, pero la manera en que la que trabaja en Windows es igual, ya sea usando CMD o PowerShell, no depende de la terminal que tengan.

## Entorno virtual

### Instalar el modulo para entornos virtuales

Si ya se tiene instalado el modulo necesario para los entornos virtuales, se puede saltar directamente a la siguiente sección [aquí](#activar-entorno-virtual). En caso contrario de no se tener instalado el módulo de Python encargado de los entornos virtuales, toca ejecutar el comando de a continuación (así se ve en mi caso)

```bash
pip install virtualenv
```

### Activar entorno virtual

Suponiendo que ya se tienen instalado todas las librerias necesarias, pero en el caso de que no, aquí también les hago una pequeña guía de cómo podrían instalar un entorno virtual fácilmente.

Al igual que antes, requieren estar ubicados en esta carpeta, por tanto, volvemos a ejecutar las siguientes lineas

```bash
$cd backend
backend$ python -m venv .venv
backend$
```

Aquí lo que se está creando es un entorno virtual de Python donde el nombre de la carpeta es `/.venv`, aunque el nombre la carpeta está en cada quién, recomiendo colocar el mismo, porque es ese nombre quien sale en el [.gitignore](./.gitignore). Aun así, en caso de que quieran colocar otro nombre para la carpeta, pueden hacerlo sin problemas, solo se necesitará actualizar el [.gitignore](./.gitignore)

Ahora, para activar el entorno virtual sí depende del sistema operativo que se esté utilizando, al menos en bash se hace así

```bash
backend$ source .venv/bin/activate
(.venv) backend$
```

Nótese que, cuando se activa el entorno virtual sale el prefijo en consola `(.venv)`, indicando que el entorno virtual se está utilizando correctamente

En Windows es similar, pero con unas ligeras diferencias, así se ve en el caso de que la terminal que se esté utilizando sea PowerShell (es la terminal que viene por defecto)

```powershell
PS C:.\GestionHospitalaria\backend> .\.venv\Scripts\activate
```

### Instalar modulos

Una vez activado el entorno virtual, toca instalar todas las librerias necesarias para que todos funcione sin problemas, y eso se hace con

```bash
(.venv) ./GestionHospitalaria/backend$ pip install -r requirements.txt
```
