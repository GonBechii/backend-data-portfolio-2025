# 🧰 Backend & Data Portfolio 2025 — Orders & Inventory API

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.x-A30000)](https://www.django-rest-framework.org/)
[![MariaDB](https://img.shields.io/badge/MariaDB/MySQL-8.x-003545?logo=mariadb&logoColor=white)](https://mariadb.org/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Objetivo:** construir un portafolio profesional combinando **Backend (Django/DRF + MariaDB)** y **Datos (ETL con Pandas + Power BI)**.  
Este repo contiene el **Proyecto 1 — Orders & Inventory API** y, más adelante, se integrará con el **Proyecto 2 — FruitOps Data Pipeline**.

---

## 👩‍💼 Para RR.HH. (resumen ejecutivo)
- 🔧 **API REST** con creación de órdenes, items anidados y validación de **stock**.
- 🔐 Preparado para **JWT** y permisos por rol (se agrega en Semanas 2–3).
- ✅ **Pruebas** automatizadas y **CI/CD** (a configurar en Semanas 3 y 8).
- 🧾 **Documentación** clara (este README) + ejemplos con cURL/Postman.
- 📊 Integración con **Power BI** (semana 6) para métricas de negocio.
- 🚀 Despliegue público (semana 8) y post de avances en LinkedIn.

---

## 👨‍💻 Para desarrolladores (inicio rápido)

### Requisitos
- Python 3.12+/3.13
- MariaDB/MySQL en local (DB: `portfolio`, usuario: `app`/`app` para DEV)
- Pip y venv

### 1) Clonar y preparar entorno
```bash
git clone https://github.com/<tu_usuario>/backend-data-portfolio-2025.git
cd backend-data-portfolio-2025/orders_inventory_api
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt  # (opcional) o instala: django djangorestframework mysqlclient python-dotenv
```

> Si `mysqlclient` falla en Windows, usa **PyMySQL**: `pip install pymysql` y agrega en `config/__init__.py`:
> ```python
> import pymysql
> pymysql.install_as_MySQLdb()
> ```

### 2) Variables de entorno
Crea `orders_inventory_api/.env`:
```
SECRET_KEY=dev-secret
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=portfolio
DB_USER=app
DB_PASS=app
```

### 3) Migraciones y (opcional) datos de ejemplo
```bash
python manage.py migrate
# (opcional) carga productos de ejemplo
python manage.py loaddata ../seeds/products_fixture.json
python manage.py runserver
```

Admin: http://127.0.0.1:8000/admin/  
API: http://127.0.0.1:8000/api/

---

## 🧱 Modelo de datos (Proyecto 1)

```mermaid
erDiagram
    PRODUCT ||--o{ ORDER_ITEM : incluye
    ORDER ||--o{ ORDER_ITEM : tiene
    CUSTOMER ||--o{ ORDER : realiza

    PRODUCT {
      int id PK
      string sku
      string name
      decimal price
      int stock
    }
    CUSTOMER {
      int id PK
      string name
      string email
      string phone
    }
    ORDER {
      int id PK
      enum status
      decimal subtotal
      decimal total
      datetime created_at
    }
    ORDER_ITEM {
      int id PK
      int quantity
      decimal unit_price
      decimal line_total
    }
```

---

## 🔌 Endpoints principales (DRF)

- `GET /api/products/` — lista de productos (búsqueda por `sku` o `name`).
- `POST /api/customers/` — crea cliente.
- `POST /api/orders/` — crea orden con items anidados.

**Crear cliente**
```http
POST /api/customers/
Content-Type: application/json

{
  "name": "Cliente Demo",
  "email": "cliente.demo@example.com",
  "phone": "+56 9 1234 5678"
}
```

**Crear orden** (descuenta stock y calcula totales)
```http
POST /api/orders/
Content-Type: application/json

{
  "customer": 1,
  "items": [
    {"product": 1, "quantity": 2},
    {"product": 3, "quantity": 1, "unit_price": 3500}
  ]
}
```

Respuesta (ejemplo):
```json
{
  "id": 12,
  "customer": 1,
  "status": "PENDING",
  "subtotal": "9470.00",
  "total": "9470.00",
  "created_at": "2025-08-18T14:32:01Z",
  "items_detail": [
    {"id": 21, "product": {"id": 1, "sku":"ALM-CAF-500","name":"Café molido 500 g","price":"3990.00","stock":78}, "quantity": 2, "unit_price": "3990.00", "line_total": "7980.00"},
    {"id": 22, "product": {"id": 3, "sku":"ALI-AZU-1K","name":"Azúcar blanca 1 kg","price":"1490.00","stock":94}, "quantity": 1, "unit_price": "3500.00", "line_total": "3500.00"}
  ]
}
```

---

## 🗂️ Estructura del repo
```
backend-data-portfolio-2025/
├─ orders_inventory_api/        ← Proyecto 1 (Django + DRF + MariaDB)
│  ├─ config/                   ← settings/urls
│  ├─ core/                     ← modelos, serializers, views
│  ├─ manage.py
│  └─ .env.example (sugerido)
├─ fruitops_pipeline/           ← Proyecto 2 (ETL + Power BI) — Semanas 5–7
├─ dashboards/                  ← Power BI .pbix
├─ seeds/                       ← datos de ejemplo (fixtures/CSV)
│  └─ products_fixture.json
└─ docs/                        ← bitácora y diagramas
```

---

## 📦 Seeds incluidos
- `seeds/products_fixture.json` — 20 productos en español (SKU, nombre, precio, stock).
```bash
python manage.py loaddata ../seeds/products_fixture.json
```

> Para datos de la **Semana 5 (FruitOps)**, se usarán CSV simulados con: `orchards`, `harvests`, `batches`, `sensors`, `defects`, `shipments`. (Se documentará en `/fruitops_pipeline` al avanzar).

---

## 🧭 Roadmap (10 semanas)
- [x] Semana 1: Setup, modelo `Product`, admin, seeds
- [ ] Semana 2: `Customer`, `Order`, `OrderItem` + CRUD DRF
- [ ] Semana 3: Tests, performance (select_related, índices), manejo de errores
- [ ] Semana 4: Tareas asíncronas (Celery), exportación CSV, correo
- [ ] Semana 5: ETL (Pandas) con datos simulados → MySQL
- [ ] Semana 6: Esquema estrella + Dashboard Power BI
- [ ] Semana 7: Orquestación + API de KPIs
- [ ] Semana 8: Docker + CI/CD + Deploy público
- [ ] Semana 9: Documentación completa + métricas
- [ ] Semana 10: Entrevista + posts y demos públicas

---

## 🤝 Contribuir
- Commits con **Conventional Commits** (`feat:`, `fix:`, `chore:`, `docs:`…).  
- Issues/PRs con descripción clara y pasos para reproducir.

---

## 📄 Licencia
MIT. Libre para uso educativo y demostrativo.

---

## 📬 Contacto
**Diego Gárate** — *Open to Work (Backend Jr & Trainee de Datos)*  
LinkedIn: https://www.linkedin.com/in/diegogarate/  
Email: garatediego.1@gmail.com
