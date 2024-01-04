from flask import Flask, request
import random
import threading
import requests
from bs4 import BeautifulSoup
import urllib
import os
import math
from os.path import exists
import time
app = Flask(__name__)
idownloads = []

def dividir_archivo(ruta_archivo, tamano_parte_mb, ide):
    tamano_parte_bytes = tamano_parte_mb * 1024 * 1024
    lista_archivos_divididos = []
    
    tamano_archivo = os.path.getsize(ruta_archivo)
    if tamano_archivo < tamano_parte_bytes:
        lista_archivos_divididos.append(ruta_archivo)
    else:
        with open("./"+ruta_archivo, 'rb') as archivo_original:
            numero_parte = 1
            while True:
                contenido_parte = archivo_original.read(tamano_parte_bytes)
                if not contenido_parte:
                    break
                nombre_parte = f"{ruta_archivo}_parte_{numero_parte}"
                with open("./"+nombre_parte, 'wb') as archivo_parte:
                    archivo_parte.write(contenido_parte)
                lista_archivos_divididos.append(nombre_parte)
                numero_parte += 1
                
    return lista_archivos_divididos
def upload(filename,host, username, password, repository):
    proxy = ""
    spypng = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf6\x178U\x00\x00\x00\x00IEND\xaeB`\x82'
    open(filename+".td", "wb").write(spypng+open(filename,"rb").read())
    print(filename+".td")
    filename = filename+".td"
    inforhab = requests.session()
    logindata = {"username":username,"password":password}
    login = inforhab.post(host+"/login/signIn",data=logindata,allow_redirects=True,stream=True,proxies=dict(http=proxy,https=proxy))
    if "Cerrar sesión" in login.text:
    	print("Sesión Iniciada")
    	try:
    		data = {"articleId":repository,"from":"","title[es_ES]":random.randint(100000,999999),"creator[es_ES]":"TechDev","subject[es_ES]":"","type":"Herramienta de investigación","typeOther[es_ES]":"","description[es_ES]":"Subido por TechDev","publisher[es_ES]":"","sponsor[es_ES]":"TechDev","dateCreated":"","source[es_ES]":"","language":"es"}
    	except:
    		print("No se pudo crear los datos necesarios")
    	try:
    		filek = {"uploadSuppFile": open(filename,"rb")}
    	except:
    		print("No se pudo importar el archivo")
    	upFile = inforhab.post(host+"/author/saveSuppFile?path=",data=data,files=filek,allow_redirects=True,stream=True,proxies=dict(http=proxy,https=proxy), headers={"MimeType":"Image/png"})
    	getLink = inforhab.get(host+"/author/submission/"+repository,proxies=dict(http=proxy,https=proxy))
    	soup = BeautifulSoup(getLink.text, "html.parser")
    	entradas = soup.find_all('a',{'class':'file'})
    	regex1 = str(entradas).split(",")
    	regex2 = regex1[-1]
    	regex3 = regex2.replace("]","")
    	regex4 = regex3.split("-")[1]
    	url = host+"/author/download/"+repository+"/"+regex4
    	os.unlink(filename)
    	return url
    else:
    	print("NO SE PUDO INICIAR SESIÓN")
def download_file(url, ide):
	           		timed = time.time()
	           		global idownloads
	           		open("./ides/"+str(ide),"w").write("0")
	           		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
	           		uplo = requests.Session()
	           		response = uplo.get(url,headers=headers, stream=True)
	           		if "Content-Disposition" in uplo.headers and "filename=" in uplo.headers["Content-Disposition"]:
	           		    nombre_archivo = uplo.headers["Content-Disposition"].split("filename=")[1].strip("'\"")
	           		else:
	           		    nombre_archivo = urllib.parse.unquote(url.split("/")[-1].split("?")[0]).replace('+',' ')
	           		    filename = nombre_archivo
	           		    for down in idownloads:
	           		        if str(down["ide"]) == str(ide):
	           		            down["filename"] = filename
	           		with open(nombre_archivo, 'wb') as archivo:
	           			ant_per = 1
	           			total_tamanio = int(response.headers.get('content-length', 0))
	           			descargado = 0
	           			for fragmento in response.iter_content(chunk_size=1024):
	           			     if fragmento:
	           			     	archivo.write(fragmento)
	           			     	descargado += 1024
	           			     	dstr = str(descargado)+" Bps"
	           			     	if descargado > 1073741824:
	           			     	    dstr = str(round(descargado/1073741824,1))+" GB"
	           			     	elif descargado > 1048576:
	           			     	    dstr = str(round(descargado/1048576,1))+" MB"
	           			     	elif descargado > 1024:
	           			     	    dstr = str(round(descargado/1024,1))+" KB"
	           			     	tstr = str(total_tamanio)+" Bps"
	           			     	if total_tamanio > 1073741824:
	           			     	    tstr = str(round(total_tamanio/1073741824,1))+" GB"
	           			     	elif total_tamanio > 1048576:
	           			     	    tstr = str(round(total_tamanio/1048576,1))+" MB"
	           			     	elif total_tamanio > 1024:
	           			     	    tstr = str(round(total_tamanio/1024,1))+" KB"
	           			     	porcentaje = round(((descargado / total_tamanio) * 50),1)
	           			     	if time.time()-timed > 1:
	           			     	    timed = time.time()
	           			     	    open("./ides/"+str(ide),"w").write(str(porcentaje))
	           		open("./ides/"+str(ide),"w").write("50")
	           		zipes = dividir_archivo(filename, 500, ide)
	           		print(zipes)
	           		open("./ides/"+str(ide),"w").write("60")
	           		hash = "1780--"
	           		count = 1
	           		total=len(zipes)
	           		for fi in zipes:
	           		    link = upload(fi,"https://revsaludpublica.sld.cu/index.php/spu/","techdev2","@A1a2a3mo","26674")
	           		    open("./ides/"+str(ide),"w").write(str(round(((count/total)*40)+60)))
	           		    print(("SUBIDO "+fi+"\n"))
	           		    count+=1
	           		    hash += link.split("/")[-1]+"/"
	           		open("./ides/"+str(ide),"w").write("100")
	           		hash += "--"
	           		hash = hash.replace("/--","--")
	           		os.unlink("./"+filename)
	           		for down in idownloads:
	           		    if str(down['ide']) == str(ide):
	           		        down['hash'] = hash
if not exists("./ides"):
    os.mkdir("./ides")
@app.route('/')
def index():
    global idownloads
    print(idownloads)
    downdiv = ""
    for down in idownloads:
        downdiv += '''<div style="background:linear-gradient(to bottom right, #bfeaff, #ffffff, #ffffff, #ffffff, #ffffff, #ffffff, #f4d5ff); margin:5%; padding:20px; border-radius:20px;">
        <div>
<div style="display: flex;">
  <div style="flex:1; display: flex; flex-direction: column; padding-left:5%;">
    <div style="flex: 1;"><h2 id="name_'''+str(down["ide"])+'''">'''+down["filename"]+'''</h2></div>
    <div style="flex: 1; display:flex; align-items:center;"><h3 style="flex: 0; margin:15px;" id="portext_'''+str(down["ide"])+'''">'''+open("./ides/"+str(down["ide"]),"r").read()+'''%</h3><progress id="prog_'''+str(down["ide"])+'''" style="flex:1; height:50px;" value="'''+open("./ides/"+str(down["ide"]),"r").read()+'''" max="100"></progress></div>
    <script>var interval'''+str(down["ide"])+''' = setInterval(function(){
var xhr = new XMLHttpRequest();
var url = "./getide";
var data = "ide='''+str(down["ide"])+'''";

xhr.open("POST", url, true);
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

xhr.onreadystatechange = function () {
  if (xhr.readyState === 4 && xhr.status === 200) {
    var response = JSON.parse(xhr.responseText);
    document.getElementById("name_'''+str(down["ide"])+'''").innerHTML = response.filename;
    document.getElementById("prog_'''+str(down["ide"])+'''").value = response.porcentaje;
    document.getElementById("portext_'''+str(down["ide"])+'''").innerHTML = response.porcentaje+"%";
    document.getElementById("hash_'''+str(down["ide"])+'''").value = response.hash;
    if (response.porcentaje === "100") {
    clearInterval(interval'''+str(down["ide"])+''');
    } else {
    
   }
  }
};
xhr.send(data);
    },1500);</script>
  </div>
  <div style="flex: 0 0 100px; display: flex; flex-direction: column;">
    <div style="flex: 1; padding-right:15%;"><h1 class="bi bi-clipboard" id="iconbutt_'''+str(down["ide"])+'''" onclick="copyhash('''+str(down["ide"])+''')" style="width:100%; text-align:right; font-size:2.5em;"></h1></div>
    <div style="flex: 1; padding-right:15%;"></div><input type="text" style="display:none; width:80%; padding:20px; border-radius:20px;" id="hash_'''+str(down["ide"])+'''" value='''+str(down["hash"])+'''>
  </div>
</div>
        </div>
    </div>'''
    return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>QvaNET</title>
    <style>
        
    </style>
    <link rel="stylesheet" href="./css/bootstrap.min.css">
    <link rel="stylesheet" href="./css/bootstrap.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
    <script>
    function copyhash(ide) {
    butt = document.getElementById("iconbutt_"+ide);
    hash = document.getElementById("hash_"+ide);
    hash.style.display = "block";
    hash.select();
    document.execCommand("copy");
    alert("Se copió su hash al portapapeles, lea la documentación para poder descargar su archivo.");
    butt.classList.remove("bi-clipboard");
    butt.classList.add("bi-clipboard-check")
    hash.style.display = "none";
    }
    function upscreen() {
        const screen2 = document.getElementById("screen2");
        screen2.style.display = "block";
        }
    function desupload() {
        var screen2 = document.getElementById("screen2");
        screen2.style.display = "none";
    }
    function sendURI() {
        var sender = document.getElementById("sendURL");
        sender.click();
    }
</script>
</head>
<body style="margin:0px; padding:0px; background: linear-gradient(to bottom right,#ffd5f4, #EEEEEE,#EEEEEE,#EEEEEE, #aadfff); background-size:100%; background-attachment:fixed;">
    <div id="screen2" style="display:none; position:fixed; top:0px; left:0px; right:0px; bottom:0px; background:#EEEEEE; z-index:5; padding:50px;"><div style="background: linear-gradient(to bottom right, #80d6ff, #ff95fc); color:white; margin:5%; border-radius:50px; border:solid 5px; border-color:#EEEEEE; box-shadow:3px 2px 10px #f4d5ff; padding:10px; display:inline-block; padding-left:40px; padding-right:40px; position:fixed; bottom:20px; right:20px;" onclick="desupload()">
            <h1><span class="bi bi-x-circle-fill"></span> CERRAR</h1>
        </div><center><form action="./addurl" method="POST"><input name="url" type="text" style="width:80%; font-size:2.5em; padding:20px; background: linear-gradient(to bottom right,#ffd5f4, #EEEEEE,#EEEEEE,#EEEEEE, #aadfff); border:solid 5px; border-color:#ffbfff; border-radius:20px; color:#888888;" placeholder="URL --------------------------"><input type="submit" id="sendURL" style="display:none;"></form><div style="background: linear-gradient(to bottom right, #80d6ff, #ff95fc); color:white; margin:5%; border-radius:50px; border:solid 5px; border-color:#EEEEEE; box-shadow:3px 2px 10px #f4d5ff; padding:10px; padding-left:40px; padding-right:40px; width:80%;" onclick="sendURI()">
            <h1><span class="bi bi-folder-plus"></span> AÑADIR</h1>
        </div></center></div>
    <div style="font-size:5em; text-align:center; display:inline-block; position:fixed; left:100px; bottom:-35px; padding-left:35px; border-radius:20px;"><h3 style="color:#AAAAAA;" class="bi bi-menu-up"></h3></div>
    <center>
        <div style="background: linear-gradient(to bottom right, #80d6ff, #ff95fc); color:white; margin:5%; border-radius:50px; border:solid 5px; border-color:#EEEEEE; box-shadow:3px 2px 10px #f4d5ff; padding:10px; display:inline-block; padding-left:40px; padding-right:40px; position:fixed; bottom:20px; right:20px;" onclick="upscreen()">
            <h1><span class="bi bi-cloud-plus-fill"></span> SUBIR ARCHIVO</h1>
        </div>
    </center>
    <!-- DESCARGAS -->
</body>
<script src="./js/bootstrap.min.js" ></script>
<script src="./js/bootstrap.js" ></script>
</html>
'''.replace("<!-- DESCARGAS -->",downdiv)
@app.route('/addurl', methods=['POST'])
def addURL():
    global idownloads
    url = request.form['url']
    ide = random.randint(10000,99999)
    idownloads.append({"url":url, "filename":"cargando","ide":ide,"porcentaje":0,"hash":""})
    open("./ides/"+str(ide),"w").write("0")
    threading.Thread(target=download_file, args=(url,ide)).start()
    return '''<script>window.location.href = "./";</script>'''
@app.route('/getide', methods=['POST'])
def getIDE():
    global idownloads
    ide = request.form["ide"]
    current = 0
    print(ide)
    for down in idownloads:
        if str(down["ide"]) == str(ide):
            down["porcentaje"] = open("./ides/"+str(down["ide"]),"r").read()
            return idownloads[current]
        else:
            current += 1

if __name__ == '__main__':  
     app.run()