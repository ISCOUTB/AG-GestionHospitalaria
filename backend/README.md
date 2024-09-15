# README - BACKEND

Hasta el momento, la información que contendrá este README es acerca de cómo se puede ejecutar la API.

Hay una cosa que debe estar clara, y es que la versión de Python que se está utilizando es la 3.12.5, lo menciono para evitar tener problemas a futuro.

Para saber qué versión de Python están utilizando, pueden ejecutar estos comandos:

```bash
$ python3 -V
Python 3.12.5
```

O este (así sale en mi caso)

``` bash
pip -V
pip 24.2 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

## Ejecutar

Lo primero que se tiene que realizar es instalar todas las librerias para así asegurar que todo se ejecute sin problemas, para eso, ver [aquí](#entorno-virtual).Una vez instaladas las librerias, es necesario ubicar la consola en esta carpeta, esto lo hacemos con el siguiente comando:

``` bash
./GestionHospitalaria$ cd backend/
./GestionHospitalaria/backend$ 
```

Ya una vez ubicados, dentro del archivo [main.py](./app/main.py) hay un apartado donde se está ejecutando con uvicorn la API. Entonces, la manera en la que se puede ejecutar ese archivo sin que haya problemas con las librerias es así:

``` bash
./GestionHospitalaria/backend$ python3 -m app.main
INFO:     Will watch for changes in these directories: ['./GestionHospitalaria/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [101373] using WatchFiles
INFO:     Started server process [101375]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Aquí yo estoy utilizando bash, puesto que mi sistema operativo es Ubuntu, pero la manera en que la que trabaja en Windows es igual, ya sea usando CMD o PowerShell, todo depende de la terminal que hayan escogido.

## Entorno virtual

### Instalar el modulo para entornos virtuales

Si ya se tiene instalado el modulo necesario para los entornos virtuales, se puede saltar directamente a la siguiente sección [aquí](#activar-entorno-virtual). En caso contrario de no se tener instalado el módulo de Python encargado de los entornos virtuales, toca ejecutar el comando de a continuación (así se ve en mi caso)

```bash
/GestionHospitalaria/backend$ pip install virtualenv
Defaulting to user installation because normal site-packages is not writeable
Collecting virtualenv
  Using cached virtualenv-20.26.4-py3-none-any.whl.metadata (4.5 kB)
Requirement already satisfied: distlib<1,>=0.3.7 in /home/juand/.local/lib/python3.12/site-packages (from virtualenv) (0.3.8)
Requirement already satisfied: filelock<4,>=3.12.2 in /home/juand/.local/lib/python3.12/site-packages (from virtualenv) (3.16.0)
Requirement already satisfied: platformdirs<5,>=3.9.1 in /home/juand/.local/lib/python3.12/site-packages (from virtualenv) (4.3.2)
Using cached virtualenv-20.26.4-py3-none-any.whl (6.0 MB)
Installing collected packages: virtualenv
Successfully installed virtualenv-20.26.4
```

### Activar entorno virtual

Estoy suponiendo que ya tienen instalado todas las librerias necesarias, pero en el caso de que no, aquí también les hago una pequeña guía de cómo podrían instalar un entorno virtual fácilmente.

Al igual que antes, requieren estar ubicados en esta carpeta, por tanto, volvemos a ejecutar la misma línea de código

```bash
./GestionHospitalaria$ cd backend/
./GestionHospitalaria/backend$ 
```

Una vez ubicados, podrán ejecutar el siguiente comando:

```bash
./GestionHospitalaria/backend$ python3 -m venv .venv
./GestionHospitalaria/backend$
```

Aquí lo que se está creando es un entorno virtual de Python donde el nombre de la carpeta es `/.venv`, aunque el nombre la carpeta está en cada quién, recomiendo colocar esa misma porque es ese nombre quien sale en el [.gitignore](./.gitignore). Aun así, en caso de que quieran colocar otro nombre para la carpeta, pueden hacerlo sin problemas, solo recuerden actualizar el [.gitignore](./.gitignore)

Ahora, para activar el entorno virtual sí depende del sistema operativo que se esté utilizando, al menos en bash se hace así

```bash
./GestionHospitalaria/backend$ source .venv/bin/activate
(.venv) ./GestionHospitalaria/backend$
```

Nótese que, cuando se activa el entorno virtual sale el prefijo en consola `(.venv)`, indicando que el entorno virtual se está utilizando correctamente

En Windows es similar, pero con unas ligeras diferencias, así se ve en el caso de que la terminal que se esté utilizando sea PowerShell (es la terminal que viene por defecto)

```powershell
PS C:.\GestionHospitalaria\backend> .\.venv\Scripts\activate
```

o

```powershell
PS C:.\GestionHospitalaria\backend> .\.venv\Scripts\activate.bat
```

Si nunca antes se ha configurado entornos virtuales en Windows, es probable que salga un error ejecutando el anterior comando (me pasó ejecutando el primer comando en PowerShell), para el cual les tocará buscar en internet muchachos, lastimosamente no recuerdo qué tuve que hacer para que funcionara.

### Instalar modulos

Una vez activado el entorno virtual, toca instalar todas las librerias necesarias para que todos funcione sin problemas, y eso se hace con

```bash
(.venv) ./GestionHospitalaria/backend$ pip install -r requirements.txt
```

Y así quedó todo perfectamente preparado para ejecutar el backend sin problemas!!
