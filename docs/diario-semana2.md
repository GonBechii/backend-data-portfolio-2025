# Diario — Semana 2 _(25–29 ago 2025)_

> Ritmo: **4 mañanas/semana** (L–M backend, X–V datos)  
> Zona horaria: **America/Santiago**

---

## Estado general de la semana

- [x] **Día 1 (Lun 25/08):** Integración de Swagger/OpenAPI (drf-spectacular). — **completado**
- [x] **Día 2 (Mar 26/08):** Generar colección Postman desde OpenAPI. **completado**
- [ ] **Día 3 (Mié 27/08):** JWT básico y pruebas de login/logout. — _pendiente_
- [ ] **Día 4 (Vie 29/08):** Permisos por rol + afinación de filtros/paginación. — _pendiente_
---
## Pendientes de la Semana 2
- [x] Generar y versionar colección Postman.
- [ ] Implementar JWT básico.
- [ ] Configurar permisos por rol.
- [ ] Afinar filtros y paginación de endpoints.
---

## Día 1 — Lunes 25 ago 2025

### 🎯 Objetivo del día
- Integrar **Swagger/OpenAPI** en el proyecto con `drf-spectacular`.
- Exponer documentación automática en `/api/docs` y `/api/redoc`.

### ✅ Lo conseguido
- Instalación de `drf-spectacular` y `drf-spectacular-sidecar`.
- Configuración en `settings.py`:
  - Corregido `DEFAULT_SCHEMA_CLASS` duplicado.
  - Añadido toggle `DOCS_PUBLIC` para definir acceso público o protegido.
- Configuración en `urls.py`:
  - `/api/schema/` → Esquema OpenAPI (JSON/YAML).
  - `/api/docs/` → Swagger UI.
  - `/api/redoc/` → Redoc.
- Ajustes en serializers:
  - `OrderSerializer.get_items_detail` anotado con `@extend_schema_field` para describir salida correctamente.
  - `OrderItemWriteSerializer.validate_quantity` corregido (ahora fuera de `Meta`).
- Verificación:
  - `/api/schema/?format=json` exporta el esquema.
  - `/api/docs/` y `/api/redoc/` muestran documentación navegable sin errores.
  - Warning de `get_items_detail` resuelto.

### 🧪 Evidencia rápida (comandos)
```powershell
# Instalar librerías
pip install drf-spectacular drf-spectacular-sidecar

# Levantar server
cd orders_inventory_api
.\.venv\Scripts\Activate.ps1
python manage.py runserver

# Probar esquema y docs
#  - http://127.0.0.1:8000/api/schema/?format=json
#  - http://127.0.0.1:8000/api/docs/
#  - http://127.0.0.1:8000/api/redoc/
```
### Capturas guardadas
- **01-swagger.png** → Swagger UI en `/api/docs`
- **02-redoc.png** → Redoc en `/api/redoc`

📸 Ver carpeta completa → [docs/capturas/semana2/](./capturas/semana2/)

### 🧱 Bloqueos y soluciones
- **Error:** `Incompatible AutoSchema used on View CustomerViewSet`.  
  **Solución:** había dos bloques `REST_FRAMEWORK`, se fusionaron en uno con `DEFAULT_SCHEMA_CLASS`.
- **Error:** `ImportError: rest_framework.permissions.ISAutenticated`.  
  **Solución:** corregido el typo → `IsAuthenticated`.
- **404 en /api/docs:** se debía a una coma extra en la ruta (`'api/docs/,'`).  
  **Solución:** corregido a `'api/docs/'`.
- **Warning en get_items_detail:** se añadió `@extend_schema_field(OrderItemReadSerializer(many=True))`.

### ▶️ Próximos pasos (para el Día 2)
- Exportar esquema OpenAPI en JSON.
- Importar en Postman para generar colección automáticamente.
- Versionar la colección en `docs/postman_collection.json`.

---
## Día 2 — Martes 26 ago 2025

### 🎯 Objetivo del día
- Generar y validar **colección Postman** desde OpenAPI.
- Probar **CRUD completo de Customers**.
- Documentar con **Examples** en la colección (200, 201, 204).

### ✅ Lo conseguido
- Requests creados en la colección:
  - `GET /api/customers/` → Example: **200 customers list**
  - `POST /api/customers/` → Example: **201 customer created**
  - `GET /api/customers/{id}/` → Example: **200 customer detail**
  - `DELETE /api/customers/{id}/` → Example: **204 no content**
- Tests Postman agregados en cada request (status codes, estructura JSON, variables env).
- Colección exportada a `docs/postman_collection.json`.

### 🧪 Evidencia rápida
- Ejecución de tests en verde (201 Created, 200 OK, 204 No Content).
- Variables de entorno (`customer_id`) gestionadas automáticamente.
- Examples visibles en la colección.

### Capturas guardadas
- **03-postman-get-customers.png** → Example 200 lista de clientes
- **04-postman-post-customer.png** → Example 201 cliente creado
- **05-postman-get-customer-detail.png** → Example 200 detalle cliente
- **06-postman-delete-customer.png** → Example 204 delete sin contenido
- **07-postman-examples.png** → (opcional) vista de todos los Examples en la colección

📸 Ver carpeta completa → [docs/capturas/semana2/](./capturas/semana2/)

### ▶️ Próximos pasos (Día 3)
- Implementar **JWT básico** con `djangorestframework-simplejwt`.
- Agregar endpoints `/api/token/` y `/api/token/refresh/`.
- Integrar tokens en Postman (env var `token`) y extender tests.
