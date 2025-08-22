# Diario — Semana 1 _(18–22 ago 2025)_

> Ritmo: **4 mañanas/semana** (L–M backend, X–V datos)  
> Zona horaria: **America/Santiago**

---

## Estado general de la semana

- [x] **Día 1 (Lun 18/08):** Setup del repo, Django conectado a DB, seeds.  
- [x] **Día 2 (Mar 19/08):** Docker (MariaDB + Adminer) estable, admin funcional con órdenes e ítems.  
- [ ] **Día 3 (Mié 20/08):** CRUD DRF (orders con ítems anidados) — _planificado_.  
- [ ] **Día 4 (Vie 22/08):** Documentación final S1 + mini demo — _planificado_.  

---

## Día 1 — Lunes 18 ago 2025

### 🎯 Objetivo del día
- Estructura base del **monorepo** y **proyecto Django** conectado a base de datos.
- **Modelo `Product`** con administración y **seeds** para pruebas.

### ✅ Lo conseguido
- Monorepo `backend-data-portfolio-2025/` con subcarpetas:
  - `orders_inventory_api/`, `seeds/`, `docs/`.
- Proyecto **Django** operativo y **conectado a MariaDB** usando `.env` (python-dotenv).
- **Modelo `Product` + admin**: listado, búsqueda por SKU/nombre.
- **Seeds**: `seeds/products_fixture.json` (20 productos en español: SKU, nombre, precio, stock).
- **Git/GitHub** configurado: remoto, commits iniciales, `.gitignore` y `.gitattributes`.

### 🧪 Evidencia rápida (comandos)

```powershell
# Entorno
cd orders_inventory_api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Django
python manage.py migrate
python manage.py loaddata ../seeds/products_fixture.json
python manage.py runserver
```

- **Admin:** http://127.0.0.1:8000/admin

### 🧱 Bloqueos y soluciones
- _(Sin bloqueos mayores en el Día 1.)_

### ▶️ Próximos pasos (para el Día 2)
- Dejar base de datos en **Docker** (opcional/profesional).
- Preparar modelos **`Customer`**, **`Order`**, **`OrderItem`** para la API.

---

## Día 2 — Martes 19 ago 2025

### 🎯 Objetivo del día
- Dejar **Docker** listo para la base de datos (**MariaDB + Adminer**).
- Validar flujo completo en **Django Admin** (crear órdenes con ítems).

### ✅ Lo conseguido
- **WSL2 + Docker Desktop** habilitados en Windows.
- `docker-compose.yml` en la raíz:
  - Servicio **MariaDB** (puerto host **3307**) + **Adminer** (http://localhost:8080).
  - **Dentro de Docker:** host `db`.
  - **Desde Windows/HeidiSQL:** `127.0.0.1:3307` (usuario `app`, clave `app`, DB `portfolio`).
- **Django** lee `.env` y conecta a `127.0.0.1:3307` correctamente.
- **Modelado**:
  - Nuevos modelos: **`Customer`**, **`Order`**, **`OrderItem`**.
  - `OrderItem`:
    - `unit_price` **opcional** en el form (si falta, se toma de `Product.price`).
    - `line_total` calculado automáticamente (**solo lectura** en admin).
    - Restricciones: `quantity > 0` y `unique_together (order, product)`.
  - `Order.recompute_totals()` actualiza **subtotal** y **total** al guardar.
- **Admin**:
  - Inline de `OrderItem` dentro de `Order`.
  - Recalculo de totales en `save_related()`.

---

## Día 3 — Miércoles 20 ago 2025

### 🎯 Objetivo del día
Exponer **API REST** con **Django REST Framework**:
- `GET /api/products/` (read-only, búsqueda/ordenación)
- `CRUD /api/customers/`
- `CRUD /api/orders/` con **ítems anidados** y **descuento de stock** al crear

### ✅ Lo conseguido
- **Routers DRF** activos en `/api/` (products, customers, orders).
- **Serializadores**:
  - `OrderItemWriteSerializer` para entrada; `items_detail` para salida.
  - `customer = PrimaryKeyRelatedField(queryset=Customer.objects.all())` (fix del error de queryset).
- **Lógica de creación de órdenes**:
  - `transaction.atomic()` + `select_for_update()` para descontar stock de forma segura.
  - `unit_price`: si viene vacío, se toma de `Product.price`.
  - `line_total = quantity * unit_price`.
  - Re-cálculo de `subtotal`/`total` al guardar.
- **Búsqueda/ordenación** en productos (`?search=`, `?ordering=`) y **paginación** DRF.
- **Admin** sigue operativo; al crear desde API o admin, los totales coinciden.

### 🧪 Cómo probar (rápido)
# Levantar el server
  - cd orders_inventory_api
  - .\.venv\Scripts\Activate.ps1
  - python manage.py runserver

# Crear Cliente
- curl -X POST http://127.0.0.1:8000/api/customers/ \
  - H "Content-Type: application/json" \
  - d '{"name":"Cliente Demo","email":"cliente.demo@example.com","phone":"+56 9 1234 5678"}'

# Crear orden (descuenta stock)

- curl -X POST http://127.0.0.1:8000/api/orders/ \
    - H "Content-Type: application/json" \
    - d '{
       "customer": 1,
       "status": "PENDIENTE",
       "items": [
         { "product": 1, "quantity": 2 },
         { "product": 3, "quantity": 1, "unit_price": 3790 }
        ]
      }'

# Verificar

  - GET /api/orders/ → ver items_detail, subtotal, total.

  - GET /api/products/?search=CAF → búsqueda.

  - Revisar en admin que el stock bajó.

### 🧱 Bloqueos y soluciones

- 404 en /api/customers/ → el router estaba en singular (customer/), se cambió a plural.

- AssertionError (PrimaryKeyRelatedField sin queryset) → se añadió queryset=Customer.objects.all() en el serializer.

### ▶️ Próximos pasos (Día 4)

  - Documento final S1: capturas de Admin y API, README con ejemplos cURL, mini demo en video (2–3 min).

  - Preparar Swagger/OpenAPI y colección Postman para iniciar Semana 2.

---

### 🧪 Evidencia rápida (comandos)
```powershell
# Levantar
cd orders_inventory_api
.\.venv\Scripts\Activate.ps1
python manage.py runserver

# Django
cd orders_inventory_api
.\.venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py runserver
```

- En **Admin**: crear **Order** y agregar **OrderItems** (deja `unit_price` vacío si quieres → se autocompleta).  
- Ver **subtotal/total** actualizados tras guardar.

---

### 🧱 Bloqueos y soluciones
- **No se podía descargar `mariadb:11.4` / error de Engine**  
  → Reinicio de Docker Desktop + `wsl --shutdown`, update y reintento.  
- **Contenedor MariaDB “unhealthy”**  
  → `docker compose down -v` + `up -d`, healthcheck más paciente.  
- **Adminer “Connection refused”**  
  → Usar **Servidor = `db`** (conexión interna entre contenedores).  
- **`IntegrityError: unit_price cannot be null` en admin**  
  → `unit_price` con `null=True, blank=True` + **ModelForm** que completa precio desde `Product.price`; `line_total` **solo lectura**.  
- **Pylance no encontraba `dotenv`**  
  → Seleccionar intérprete del **venv** en VS Code y `pip install python-dotenv`.  
- **Conflicto al hacer push**  
  → `git pull --rebase`, resolver `README.md` y **push** final.



---

## Pendientes de la Semana 1

- [ ] **ER** simple en `docs/er.md` (Mermaid) con relaciones principales.  
- [ ] **Capturas** del admin (productos y una orden con ítems) para el README.  
- [ ] Seguir completando este **diario** con capturas y comandos clave.  

---

## Comandos útiles (resumen)

```powershell
# Docker DB
docker compose --env-file .env.db up -d
docker compose ps
docker compose down -v

# Adminer
# Navegador → http://localhost:8080
# Servidor = db | Usuario = app | Clave = app | DB = portfolio

# Django
cd orders_inventory_api
.\.venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py loaddata ../seeds/products_fixture.json
python manage.py runserver
```
