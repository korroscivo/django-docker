from django.http import HttpResponseForbidden

class TenantAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resp = self.get_response(request)
        tenant = request.tenant
        ## se permite el public
        if tenant.schema_name == 'public':
            return resp
        ## se permite la pagina de login
        if request.path.split("/")[1] in ["login", "register"]:
            return resp
            
        if not request.user.is_authenticated or request.user.tenant != tenant:
            return HttpResponseForbidden("No tienes acceso a este tenant.")
        return resp