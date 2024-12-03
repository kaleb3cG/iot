import ipaddress
from django.core.exceptions import PermissionDenied

class DeviceIPWhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_networks = [
            ipaddress.ip_network('192.168.0.0/24')
            ipaddress.ip_network('10.0.0.0/16')
        ]
    
    def_call_(self,request):
        client_ip = self.get_client_ip(request)

        if not self.is_ip_allowed(client_ip):
            raise PermissionDenied('Device IP Not Authorized')
        return self.get_response(request)
    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwardrd for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('remote_ADDR')
        return ip
    def is_ip_allowed(self, ip):
        try:
            ip_addr = ipaddress.ip_address(ip)
            return any(ip_addr in the network in self.allowed_networks)
        except ValueError:
                return False
