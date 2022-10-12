from flask import Flask, render_template, request
import hashlib
import controller
from datetime import datetime
import envioemail

app = Flask(__name__)
origen=""

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/verifciarUsuario",methods=["GET","POST"])
def verifciarUsuario():
    
    correo=request.form["txtusuario"]
    correo=correo.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
    password=request.form["txtpass"]
    password=password.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
    password2=password.encode()
    password2=hashlib.sha384(password2).hexdigest()
    
    global origen
    
    respuesta=controller.consultar_usuario(correo, password2)
    
    if len(respuesta)==0:
       origen=""
       mensajes= "Error de autenticacion, veririfique su usuario y contraseña."
       return render_template("informacion.html",data=mensajes)
    
    else:
        origen=correo
        resp2=controller.lista_destinatarios(correo)
        return render_template("principal.html",listaD=resp2,usuario=respuesta)
    
    
    
@app.route("/registrarUsuario",methods=["GET","POST"])
def registrarUsuario():
    
    nombre=request.form["txtnombre"]
    nombre=nombre.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
    correo=request.form["txtusuarioregistro"]
    correo=correo.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
    password=request.form["txtpassregistro"]
    password=password.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
    password2=password.encode()
    password2=hashlib.sha384(password2).hexdigest()
    
    codigo=datetime.now()
    codigo2=str(codigo)
    codigo2=codigo2.replace("-","")
    codigo2=codigo2.replace(":","")
    codigo2=codigo2.replace(".","")
    codigo2=codigo2.replace(" ","")
    
    resp=controller.regisUsuario(nombre,correo,password2,codigo2)
    if resp=="1":
        asunto="Codigo de activacion"
        mensaje="su codigo de activacion es "+codigo2
        envioemail.enviar(correo,asunto,mensaje)
        mensajes= "Usuario registrado satisfactoriamente...El código de validación es: " + codigo2
    else:
        mensajes="Error, no es posible realizar el registro, el usuario y/o correo ya existe.El código de validación es" + codigo2
    return render_template("informacion.html",data=mensajes)


@app.route("/ActivarUsuario",methods=["GET","POST"])
def ActivarUsuario():
    
    codigo=request.form["txtcodigo"]
    codigo=codigo.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
    respuesta=controller.activarU(codigo)
    if len(respuesta)==0:
        mensajes= "El codigo es incorrecto"
        return render_template("informacion.html",data=mensajes)
    else:
        mensajes= "Usuario Activado con EXITO"
        return render_template("informacion.html",data=mensajes)
    
    
@app.route("/enviarEE",methods=["GET","POST"])
def enviarEE():
    
    asunto=request.form["asunto"]
    asunto=asunto.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
    mensaje=request.form["mensaje"]
    mensaje=mensaje.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
    destino=request.form["destino"]
    destino=destino.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
    clave=request.form["clave"]
    mensaje2=mensaje
    alfabeto ="ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    cifrado =""
    for letra in mensaje2.upper():
        if letra in alfabeto:
            indice =alfabeto.find(letra)
            indice += (int)(clave)
            if indice >=27:
                indice -=27
            cifrado += alfabeto[indice%27]
        else:
            cifrado+=letra
    controller.registroEMail(asunto,cifrado,origen,destino,clave)
    
    asunto2="Nuevo Mensaje"
    mensaje2="Usted recibio un nuevo mensaje por favor ingrese a la plataforma para observarlo."
    
    envioemail.enviar(destino,asunto2,mensaje2)
    
    return "Email Enviado Satisfactoriamente"


@app.route("/correosEnviados",methods=["GET","POST"])
def correosEnviados():
    
    respuesta=controller.enviados(origen)
    return render_template("historial.html",listaCorreos=respuesta)



@app.route("/correosRecibidos",methods=["GET","POST"])
def correosRecibidos():
    
    respuesta=controller.recibidos(origen)
    return render_template("historial2.html",listaCorreos=respuesta, fun=desen)


@app.route("/actualizarPa",methods=["GET","POST"])
def actualizarPa():
    password=request.form["password"]
    password=password.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
    password2=password.encode()
    password2=hashlib.sha384(password2).hexdigest()
    
    controller.actualziarPassW(password2,origen)
    
    return "La contraseña se ha actualizado correctamente"
@app.route("/desen",methods=["GET","POST"])    
def desen():
    clave=request.form["clave"]
    cifrado=request.form["mensaje"]
    print(clave,cifrado)
    
    alfabeto ="ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    #clave="50"
    mensaje =""
    for letra in cifrado.upper():
        if letra in alfabeto:
            indice =alfabeto.find(letra)
            indice -= int(clave)
            if indice <0:
                indice +=27
            mensaje += alfabeto[indice%27]
            
        else:
            mensaje+=letra
    return mensaje 
         
    