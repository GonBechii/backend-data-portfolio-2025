# Diario — Semana 2 _(25–29 ago 2025)_

> Ritmo: **4 mañanas/semana** (L–M backend, X–V datos)  
> Zona horaria: **America/Santiago**

---

## Estado general de la semana

- [x] **Día 1 (Lun 25/08):** Integración de Swagger/OpenAPI (drf-spectacular). — **completado**
- [ ] **Día 2 (Mar 26/08):** Generar colección Postman desde OpenAPI. — _pendiente_
- [ ] **Día 3 (Mié 27/08):** JWT básico y pruebas de login/logout. — _pendiente_
- [ ] **Día 4 (Vie 29/08):** Permisos por rol + afinación de filtros/paginación. — _pendiente_

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

## Pendientes de la Semana 2
- [ ] Generar y versionar colección Postman.
- [ ] Implementar JWT básico.
- [ ] Configurar permisos por rol.
- [ ] Afinar filtros y paginación de endpoints.
