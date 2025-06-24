# Fact checkig automatizado con prensa mediante uso de LLMs

## 📁 Estructura del proyecto

El proyecto cuenta con dos carpetas, la de API y la de Notebooks. 
En la carpeta de API se puede encontrar el código necesario para ejecutarla.
En la carpeta notebooks se pueden encontrar los distintos jupyter notebooks en los que se ha entranado y probado los distintos modelos de los que hace uso el sistema

```bash
.               
├── API/                 # Código de la API
│   └── main.py          # Archivo con el lanzamiento de la API            
├── notebooks/           # Notebooks de experimentación
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Este archivo
```

## Uso de LMStudio para su ejecución

Para poder ejecutar correctamente, se debe instalar el prograla LMStudio, y, a su vez, descargar y desplegar en este uno de los LLMs disponibles. Las pruebas del proyecto se han realizado con ``Google Gemma 3-12B``.
La razón de uso de esta herrmienta es para desplegar una API local con endpoint http://localhost:1234/v1/chat/completions contra el que se lanzan distintos tipos de consultas para que se hagan contra el asistente elegido al desplegar dicho servicio.

## Ejecución del proyecto

Primero, se deben instalar todas las dependencias

```bash
pip install -r requirements.txt
```

Para la ejecuciónd del proyecto, situarse en la carpeta API/ y ejecutar:

```bash
uvicorn main:app --reload
```
## Cambios en la configuración del sistema

Para cambiar los parámetros de ejecución, se debe consultar el archivo ``appsettings.ini``, donde se encuentran todos los campos configurables del proyecto


## Uso del proyecto

Una vez lanzada la API, llamar a http://127.0.0.1:8000/news con en el body:

```JSON
{
    "text":"España ha ganado el mundial de futbol"
}
```
y la respuesta seguirá el siguiente formato:

```JSON
{
  "content_veredict": "string",        
  "content_score": "float",            
  "semantic_veredict": "string",       
  "semantic_score": "float",          
  "general_veredict": "string"         
}
```


