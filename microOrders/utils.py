import consul
import os
import socket

def get_service_url(service_name):
    """Busca un servicio en Consul y devuelve su URL."""
    # Asume que Consul está en un host llamado 'consul'
    c = consul.Consul(host='consul')
    index, services = c.health.service(service_name, passing=True)
    if services:
        service = services[0]['Service']
        return f"http://{service['Address']}:{service['Port']}"
    return None

def register_service(service_name, port):
    """Registra el servicio actual en Consul."""
    c = consul.Consul(host='consul')
    
    # Obtiene la IP del contenedor, no localhost
    address = socket.gethostbyname(socket.gethostname())

    # Define un health check. Consul llamará a esta ruta para ver si el servicio está vivo
    check = consul.Check.http(f"http://{address}:{port}/health", "10s")
    
    print(f"Registrando servicio {service_name} en {address}:{port}")
    c.agent.service.register(
        service_name,
        service_id=f"{service_name}-{address}-{port}",
        address=address,
        port=port,
        check=check
    )
