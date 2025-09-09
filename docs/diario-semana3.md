# Diario — Semana 3 _(08–12 sep 2025)_

> Ritmo: **4 mañanas/semana** (L–M backend, X–V datos)  
> Zona horaria: **America/Santiago**

---

## Estado general de la semana

- [x] **Día 1 (Lun 08/09):** Setup pytest + deps, fix deprecación CheckConstraint. — **completado**
- [ ] **Día 2 (Mar 09/09):** Fixtures + primer test Swagger.
- [ ] **Día 3 (Mié 10/09):** Tests Products (auth + paginación).
- [ ] **Día 4 (Vie 12/09):** Tests Orders (totales + stock).

---

## Día 1 — Lunes 08 sep 2025

### 🎯 Objetivo del día
- Instalar `pytest`, `pytest-django`, `pytest-cov`, `model-bakery`.
- Configurar `pytest.ini` en la raíz del proyecto.
- Corregir `CheckConstraint.check` → `.condition`.

### ✅ Lo conseguido
- Ejecución de `pytest -q` exitosa (sin errores, cobertura inicial 37%).
- Warning deprecado eliminado (`RemovedInDjango60Warning`).
- Commit `feat(S3D1): setup pytest config + deps`.
- Commit `fix(core): migrate CheckConstraint.check → .condition`.

### 🧪 Evidencia rápida
```powershell
pytest -q
# salida: collected 0 items
# coverage: 37%
---
## 🧱 Bloqueos y soluciones

- Error inicial: ModuleNotFoundError: No module named 'core'.
- Solución: actualizar INSTALLED_APPS y apps.py a orders_inventory_api.core.

- Warning: CheckConstraint.check deprecado.
- Solución: reemplazo por condition=.

## ▶️ Próximos pasos (para el Día 2)

- Crear tests/conftest.py con fixtures (api_client, auth_client, product).

- Agregar primer test de Swagger (/api/docs).

- Commit esperado: test(S3D2): add base fixtures + swagger ui test.