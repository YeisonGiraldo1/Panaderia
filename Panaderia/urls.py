"""Panaderia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Panaderia.views import insertarempleado,listadoempleado,borrarempleado,actualizarempleado
from Panaderia.views import insertarproveedor,listadoproveedor,borrarproveedor,actualizarproveedor
from Panaderia.views import insertarusuario,loginusuario,logoutusuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Empleado/listado', listadoempleado),
    path('Empleado/insertar',insertarempleado),
    path('Empleado/borrar/<int:idempleado>',borrarempleado),
    path('Empleado/actualizar/<int:idempleado>',actualizarempleado),

    path('Proveedor/insertar',insertarproveedor),
    path('Proveedor/listado',listadoproveedor),
    path('Proveedor/borrar/<int:id>',borrarproveedor),
    path('Proveedor/actualizar/<str:idproveedor>',actualizarproveedor),

    path('Usuario/insertar',insertarusuario),
    path('Usuario/login',loginusuario),
    path('Usuario/logout',logoutusuario)
    
]
