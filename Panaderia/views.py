from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render,redirect
from Panaderia.models import Empleado,Proveedor
from django.db import connection
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout



#region Empleado

def listadoempleado(request):
    if not request.user.is_authenticated:
        return redirect('/Usuario/login')
    paginalistado = open('Panaderia/Templates/Empleado/listado.html')
    lectura = Template(paginalistado.read())
    paginalistado.close()
    empleado = Empleado.objects.all()
    parametros = Context({'empleado':empleado})
    paginafinal = lectura.render(parametros)
    return HttpResponse(paginafinal)

def insertarempleado(request):
    if not request.user.is_authenticated:
        return redirect('/Usuario/login') 
    if request.method == "POST":
     if request.POST.get('nombrecompleto') and request.POST.get('email') and request.POST.get('direccion') and request.POST.get('celular'):
        empleado = Empleado()
        empleado.NombreCompleto = request.POST.get('nombrecompleto')
        empleado.Email = request.POST.get('email')
        empleado.Direccion = request.POST.get('direccion')
        empleado.Celular= request.POST.get('celular')
        empleado.save()
        return redirect('/Empleado/listado')
    else:
        return render(request,'Empleado/insertar.html')


def borrarempleado(request,idempleado):
    empleado = Empleado.objects.get(id=idempleado)
    empleado.delete()
    return redirect('/Empleado/listado')



def actualizarempleado(request,idempleado):
    if request.method == "POST":
     if request.POST.get('nombrecompleto') and request.POST.get('email') and request.POST.get('direccion') and request.POST.get('celular'):
        empleado = Empleado.objects.get(id=idempleado)
        empleado.NombreCompleto = request.POST.get('nombrecompleto')
        empleado.Email = request.POST.get('email')
        empleado.Direccion = request.POST.get('direccion')
        empleado.Celular= request.POST.get('celular')
        empleado.save()
        return redirect('/Empleado/listado')
    else:
        empleado = Empleado.objects.filter(id=idempleado)
        return render(request,'Empleado/actualizar.html',{'empleado':empleado})

  #endregion
  
  
  


  
  #region Proveedor
  
def insertarproveedor(request):
    if not request.user.is_authenticated:
        return redirect('/Usuario/login') 
    if request.method == "POST":
     if request.POST.get('nombreproveedor') and request.POST.get('direccion') and request.POST.get('empleado_id'):
        proveedor = Proveedor()
        empleado = Empleado.objects.get(id=request.POST.get('empleado_id'))
        proveedor.Nombre = request.POST.get('nombreproveedor')
        proveedor.DireccionP = request.POST.get('direccion')
        proveedor.empleado = empleado
        proveedor.save()
        return redirect('/Proveedor/listado')
        
    else:
        empleados = Empleado.objects.all()
        return render(request,'Proveedor/insertar.html',{'empleados':empleados})
  

def listadoproveedor(request):
    if not request.user.is_authenticated:
        return redirect('/Usuario/login') 
    #with connection.cursor() as cursor:
        #cursor.callproc('listadoproveedor')
        #results = cursor.fetchall()
    #proveedor = [{'Nombre': row[1], 'DireccionP': row[2],'empleado_id': row[3]} for row in results]
    #return render(request, 'Proveedor/listado.html', {'proveedor':proveedor})

    


    listado = connection.cursor()
    listado.execute("call listadoproveedor")
    return render(request, 'Proveedor/listado.html', {'proveedor': listado})
    
    #paginalistado = open('Panaderia/Templates/Proveedor/listado.html')
    #lectura = Template(paginalistado.read())
    #paginalistado.close()
    #proveedor = Proveedor.objects.all()
    #parametros = Context({'proveedor':proveedor})
    #paginafinal = lectura.render(parametros)
    #return HttpResponse(paginafinal)
    
    


def borrarproveedor(request,id):
    with connection.cursor() as cursor:
        cursor.callproc('borrarproveedor', [id])

  
    return redirect('/Proveedor/listado')
  


def actualizarproveedor(request,idproveedor):
     if request.method =="POST":
        if request.POST.get('nombreproveedor') and request.POST.get('direccion') and request.POST.get('empleado_id'):
            proveedor = Proveedor.objects.get(id=idproveedor)
            actualizar = connection.cursor()
            actualizar.execute("call actualizarproveedor('" + idproveedor +"', '"+ request.POST.get('nombreproveedor')  +"','"
            +  request.POST.get('direccion') +"','" + request.POST.get('empleado_id') +"') ")
            return redirect('/Proveedor/listado')
     else:
        empleados = Empleado.objects.all()
        proveedor = Proveedor.objects.filter(id=idproveedor)
        return render(request, 'Proveedor/actualizar.html', {'proveedor' : proveedor, 'empleado' : empleados})





  #endregion




  #region Usuario


def insertarusuario(request):
    if request.method == "POST":
     if request.POST.get('username') and request.POST.get('password') and request.POST.get('nombres') and request.POST.get('apellidos') and request.POST.get('email') :
        
        usuario = User.objects.create_user(username=request.POST.get('username'),email=request.POST.get('email'),password=request.POST.get('password'),first_name= request.POST.get('nombres'),last_name=request.POST.get('apellidos') )
      
         
        usuario.save()
        return redirect('/Usuario/login')
    else:
        return render(request,'Usuario/insertar.html')
    


def loginusuario(request):
    if request.method == "POST":
     if request.POST.get('username') and request.POST.get('password'):
        user = authenticate(username= request.POST.get('username'),password= request.POST.get('password'))  
        if user is not None:
           login(request,user)
           return redirect('/Empleado/listado')
        else:
           mensaje = "Usuario  o Cotraseña incorrecta,Intenta de Nuevo"
           return render(request,'Usuario/login.html',{'mensaje':mensaje})
    else:
        return render(request,'Usuario/login.html')



def logoutusuario(request):
    logout(request)
    return redirect('/Usuario/login')
 
#endregion



