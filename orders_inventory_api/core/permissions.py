from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReadOnly(BasePermission):
    """
    Permite lectura (GET/HEAD/OPTIONS) a cualquiera.
    Para escribir (POST/PUT/PATCH/DELETE) exige usuraio autenticado
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
