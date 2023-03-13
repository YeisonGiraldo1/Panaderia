from django.db import models

class Empleado(models.Model):
    NombreCompleto = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    Celular = models.CharField(max_length=255)
    Direccion = models.CharField(max_length=255)
    class Meta:
      db_table = 'empleado'
      
class Proveedor(models.Model):
  Nombre = models.CharField(max_length=150)
  DireccionP = models.CharField(max_length=150)
  empleado = models.ForeignKey(Empleado,on_delete=models.PROTECT)
  class Meta:
    db_table = 'proveedor'