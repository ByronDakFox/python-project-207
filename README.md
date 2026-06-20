### Hexlet tests and linter status:
[![Actions Status](https://github.com/ByronDakFox/python-project-207/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ByronDakFox/python-project-207/actions)

# 🔍 Page Analyzer

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Aplicación web desarrollada con **Flask** y **PostgreSQL** para analizar páginas web y verificar algunos elementos importantes para el SEO, como:

- Código de respuesta HTTP.
- Etiqueta `<title>`.
- Encabezado `<h1>`.
- Meta descripción (`description`).
- Historial de verificaciones de cada sitio.

El proyecto está inspirado en herramientas de análisis SEO y permite almacenar sitios web y realizar múltiples verificaciones sobre ellos.

---

# 📸 Vista previa

## Página principal

- Agregar nuevas URLs.
- Validación de direcciones web.
- Mensajes de éxito y error.

## Lista de URLs

- Historial de sitios agregados.
- Fecha de creación.
- Última verificación realizada.

## Página de una URL

- Información del sitio.
- Historial de verificaciones.
- Estado HTTP.
- Datos SEO extraídos.

---

# 🚀 Demo

Aplicación desplegada en Render:

```text
https://TU-APP.onrender.com
```

---

# 🛠 Tecnologías utilizadas

- Python 3.12
- Flask
- PostgreSQL
- Psycopg2
- Requests
- BeautifulSoup4
- Bootstrap 5
- Gunicorn
- Jinja2
- Python-dotenv
- Validators

---

# 📂 Estructura del proyecto

```text
page_analyzer/
│
├── app.py
├── __init__.py
│
├── templates/
│   ├── index.html
│   ├── urls.html
│   └── url.html
│
├── static/
│
database.sql
build.sh
Makefile
README.md
pyproject.toml
.env
```

---

# ⚙️ Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/page-analyzer.git
cd page-analyzer
```

---

## 2. Crear entorno virtual

```bash
uv venv
source .venv/bin/activate
```

En Windows:

```powershell
.venv\Scripts\activate
```

---

## 3. Instalar dependencias

```bash
make install
```

o

```bash
uv sync
```

---

# 🐘 Configuración de PostgreSQL

Crear la base de datos:

```sql
CREATE DATABASE page_analyzer;
```

---

# 🔐 Variables de entorno

Crear un archivo `.env`:

```env
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/page_analyzer
SECRET_KEY=supersecretkey
```

Agregar `.env` al archivo `.gitignore`.

---

# 🗄 Crear las tablas

Ejecutar:

```bash
psql -U postgres -d page_analyzer -f database.sql
```

---

# 📋 database.sql

```sql
DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE IF NOT EXISTS urls (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS url_checks (
    id BIGSERIAL PRIMARY KEY,
    url_id BIGINT REFERENCES urls(id) ON DELETE CASCADE,
    status_code INTEGER,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

# ▶️ Ejecutar en desarrollo

```bash
make dev
```

o

```bash
uv run flask --debug --app page_analyzer:app run
```

La aplicación estará disponible en:

```text
http://127.0.0.1:5000
```

---

# 🚀 Ejecutar en producción

```bash
make start
```

o

```bash
gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app
```

---

# 🌐 Despliegue en Render

## Build Command

```bash
make build
```

## Start Command

```bash
make render-start
```

---

# build.sh

```bash
#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install
psql $DATABASE_URL -f database.sql
```

Dar permisos:

```bash
chmod +x build.sh
```

---

# 🔎 Funcionalidades

## Gestión de URLs

- Agregar nuevos sitios.
- Evitar URLs duplicadas.
- Validación de URLs.

## Verificaciones

- Código HTTP.
- Historial de verificaciones.
- Fecha de la última revisión.

## SEO

- Extracción de:

```html
<title>
<h1>
<meta name="description">
```

---

# 📚 API interna

## Agregar URL

```http
POST /urls
```

## Ver todas las URLs

```http
GET /urls
```

## Ver una URL

```http
GET /urls/<id>
```

## Realizar una verificación

```http
POST /urls/<id>/checks
```

---

# 📦 Dependencias principales

```text
Flask
psycopg2-binary
requests
beautifulsoup4
validators
python-dotenv
gunicorn
```

---

# 🧪 Ejemplo de uso

1. Agregar:

```text
https://python.org
```

2. Presionar:

```text
Verificar
```

3. Resultado:

```text
Status Code: 200
Title: Welcome to Python.org
H1: Welcome to Python.org
Description: The official home of the Python Programming Language.
```

---

# 🛡 Manejo de errores

La aplicación controla:

- URLs inválidas.
- URLs duplicadas.
- Sitios inaccesibles.
- Errores de conexión.
- Errores de base de datos.

---

# 👨‍💻 Autor

**Byron Ramirez**

- GitHub: https://github.com/ByronDakFox
- LinkedIn: https://www.linkedin.com/in/byronramirez95/

---

# 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

# ⭐ Si este proyecto te fue útil

No olvides dejar una estrella ⭐ en el repositorio.