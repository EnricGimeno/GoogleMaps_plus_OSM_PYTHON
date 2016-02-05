# -*- coding: UTF-8 -*-
import Tkinter
import tkFileDialog
import os
import shapefile
import tkMessageBox
from googlemaps import GoogleMaps
import math
import urllib
import cStringIO 
import Image
import Image, ImageTk

directorioImagen = "C://Users/Enric/Desktop/5Enric/Tecnicas_Graficas/Trabajo/"

def bbox (pol):
    """Returns the bounding rectangle or bounding box of polygon 'pol'."""

    xmin = pol[0][0]
    xmax = pol[0][0]
    ymin = pol[0][1]
    ymax = pol[0][1]

    for pnt in pol:
        if pnt[0] < xmin:
            xmin = pnt[0]
        elif pnt[0] > xmax:
            xmax = pnt[0]

        if pnt[1] < ymin:
            ymin = pnt[1]
        elif pnt[1] > ymax:
            ymax = pnt[1]

    return [xmin,ymin,xmax,ymax]


#Globals....
scr_w = 640
scr_h = 640
descripcion = []

horas = ''
minutos = ''
segundos = ''
contador = 0
origen_viejo = ''
destino_viejo =''

root = Tkinter.Tk()
root.title('CALCULO DE RUTAS')

def deg2num (lat_deg, lon_deg, zoom):

  lat_rad = math.radians(lat_deg)
  n = 2.0**zoom#** elevado

  xtile = int((lon_deg + 180)/360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1.0/math.cos(lat_rad))) / math.pi)/2.0*n)

  return (xtile,ytile)



def Calculo_Rutas(e):
  global Latmedia
  global Lonmedia
  global pol
  global horas
  global minutos
  global segundos
  global contador  
  
     
  try:
      

    origen_get = origen_text.get()
    destino_get = destino_text.get()
    origen_viejo

    
    if origen_get == '':
      tkMessageBox.showinfo("ERROR", "No has introducido el origen")
    if destino_get == '':
      tkMessageBox.showinfo("ERROR", "No has introducido el destino")
    if origen_get!= origen_viejo and origen_viejo !='':
        contador = 0;
    if destino_get!= destino_viejo and destino_viejo !='':
        contador = 0;
        
  #Creamos el objeto de GoogleMaps
    mapService = GoogleMaps()

  #Obtenemos las direcciones que da google
    directions = mapService.directions(origen_get, destino_get)
    print directions    

    Lat = []
    Lon = []
    pol = []
    duration = []

    ##BORRADO DEL LISTBOX PARA QUE ESTE VACIO CADA VEZ
    Listbox.delete(0, Tkinter.END)

    for step in directions['Directions']['Routes'][0]['Steps']:
        b = str(step['Duration'])
        duracion = b[13:17]
        dur = duracion.split(',')
        duration.append(dur)
        suma = 0              
                               
        a = str(step['Point'])
        borrado = a[18:len(a)]
       
        borrado = borrado.replace(', 0]}','').replace(' ','')
        coor = borrado.split(',')
        
        pol.append(coor)

        des = step['descriptionHtml']

        #LIMPIAMOS LA DESCRIPCION DE HTML

        des = des.replace('/','').replace('<b>','').replace('<wbr>',' hasta ').replace('<div>','').replace('<div class="google_note">',' ')
######## AÑADIMOS LOS CAMPOS A LA VENTANA DE INDICACIONES

        i = 0
        Listbox.insert(i, des)
        i = i + 1

    #Calculo de la duracion del viaje
    for tiempo in range(0,len(duration)):
        suma = int(duration[tiempo][0]) + suma
        
   
    horas = int(suma)/3600
    minutos = int(suma)/60
    segundos = suma%60
    print "El tiempo del trayecto es de:"
    print horas,minutos,segundos

  except:
    pass
  # CALCULO DEL BOUNDING BOX DE LA RUTA
  Lonmin,Latmin,Lonmax,Latmax = bbox(pol)
  print Lonmin,Latmin,Lonmax,Latmax
  # CALCULO DEL CENTRO DEL BOUNDING BOX - SERA EL CENTRO DEL MAPA
  Lonmedia = (float(Lonmin) + float(Lonmax))/2
  Latmedia = (float(Latmin) + float(Latmax))/2
  print Latmedia, Lonmedia
  mapa = mapa_google_map(Latmedia, Lonmedia)

 
    


  
## CREACION DEL MAPA
        
def mapa_google_map(Latmedia, Lonmedia):

  global pol
  global image1
  global src_w
  global src_h
  global desplazamiento
  global contador
  global xtile
  global ytile
  global zoom
  global ContIzq
  global ContDere
  global ContArrib
  global ContAbaj

  ContIzq = 0
  ContDere = 0
  ContArrib = 0
  ContAbaj = 0 

  
  ##MAPA DE GOOGLE MAPS
  if var3.get() == 1:
  
    
      ## RUTA EJEMPLO:
      ##http://maps.google.com/maps/api/staticmap?center=Empire+State+Building&zoom=18&size=500x500&format=jpeg&maptype=hybrid&sensor=false&
      ##http://maps.google.com/maps/api/staticmap?center=42.950827,-122.108974&zoom=12&size=500x500&format=jpg&maptype=terrain&sensor=false&
      
      #base URL faltaran añadir mas campos a la ruta

      ruta =  "http://maps.google.com/maps/api/staticmap?"

      #Sumamos el centro a la ruta
      ruta += "center="
      ruta += str(Latmedia)
      ruta += ","
      ruta += str(Lonmedia)
      ruta += "&"
      
      if contador>1:
          # Sumamos el ZOOM
          ruta +="zoom="
          ruta +=str(zoom)
          ruta +="&"
        
      contador = contador+1    
      #Sumamos el tamaño y formato de la imagen
      ruta += "size=640x640&format=jpeg&"

      #Sumamos el tipo de mapa escogido y sensor en FALSE 
      if var.get() == 0:
          print "Radiobutton: None selected"
      elif var.get() == 1:
          ruta += "maptype=terrain&sensor=false&"
          print "Terrain"
      elif var.get() == 2:
          ruta += "maptype=hybrid&sensor=false&"
          print "Hybrid"
      elif var.get() == 3:
          ruta += "maptype=satellite&sensor=false&"
          print "Satellite"
      elif var.get() == 4:
          ruta += "maptype=roadmap&sensor=false&"
          print "Roadmap"

      

        # Añadimos los Marker
        #Ejemplo
        #http://maps.google.com/maps/api/staticmap?center=39.4369485,-0.3924805&zoom=12&size=500x500&format=jpeg&maptype=roadmap&sensor=false&
        #markers=color:blue|label:A|39.404089,-0.403403&
        #markers=color:blue|label:B|39.469174,-0.376037
      
      ruta += "markers=color:blue|label:A|"
      ruta += str(pol[0][1])
      ruta += ","
      ruta += str(pol[0][0])
      ruta += "&markers=color:blue|label:B|"
      ruta += str(pol[-1][1])
      ruta += ","
      ruta += str(pol[-1][0])
      
            
        #Añadimos la ruta pintada
        #Ejemplo de ruta con la ruta
        #http://maps.google.com/maps/api/staticmap?center=39.4369485,-0.3924805&zoom=12&size=500x500&format=jpeg&maptype=roadmap&sensor=false&
        #path=color:0x0000ff|weight:5|39.404089,-0.403403|39.469174,-0.376037

      ruta += "&path=color:0x0000ff|weight:5|"

      for ss in range(0,len(pol)):
          
          ruta += str(pol[ss][1])
          ruta += ","
          ruta += str(pol[ss][0])
          if ss+1 != len(pol):
              ruta += "|" 
      
      
      ##GUARDADO DE LA IMAGEN
      urllib.urlretrieve(ruta, "mapa_google"+"."+"jpg")
      ##CARGA DE LA IMAGEN
      imageFile = "mapa_google.jpg"
      image1 = ImageTk.PhotoImage(Image.open(imageFile))
      #Obtencion de las dimensiones de la imagen
      scr_w = image1.width()
      scr_h = image1.height()
      print scr_w,scr_h
      ##
      x_ini = 0.0
      y_ini = 0.0
      #img = Tkinter.PhotoImage(imageFile)
      cnvs_rutas.create_image(x_ini,y_ini,image=image1, anchor='nw')

    ##MAPA DE OPEN_STREET_MAP
  elif var3.get() == 2:
      ##ruta = http://tile.openstreetmap.org/11/1021/779.png
      
        ##OBTENCION DE LAS LOS TILES CENTRALES DE OPENSTREETMAP
        xtile, ytile = deg2num(Latmedia, Lonmedia, zoom)
        print xtile, ytile
        print 'Bueno'
        osm = mapa_OSM(xtile, ytile)
        
        return xtile, ytile
        return ContIzq, ContDere, ContArrib, ContAbaj


def mapa_OSM(xtile, ytile):
    global imageCC
    global imageCR
    global imageCL
    global imageUL 
    global imageUC
    global imageUR 
    global imageDL
    global imageDC
    global imageDR
    cache = 'C://Cache'
    if not os.path.isdir(cache):
        directoryPath = 'C://Cache'
        os.mkdir(directoryPath)


    carp_zoom = 'C://Cache/' + str(zoom)
    if not os.path.isdir(carp_zoom):
        directoryPath = 'C://Cache/' + str(zoom)
        os.mkdir(directoryPath)

        
    carp_Xtile = str(carp_zoom)+ '/' + str(xtile)
    if not os.path.isdir(carp_Xtile):
        directoryPath = str(carp_zoom)+ '/' + str(xtile)
        os.mkdir(directoryPath)

    carp_Xtile_S1 = str(carp_zoom)+ '/' + str(xtile + 1)
    if not os.path.isdir(carp_Xtile_S1):
        directoryPath = str(carp_zoom)+ '/' + str(xtile + 1)
        os.mkdir(directoryPath)

    carp_Xtile_R1 = str(carp_zoom)+ '/' + str(xtile - 1)
    if not os.path.isdir(carp_Xtile_R1):
        directoryPath = str(carp_zoom)+ '/' + str(xtile - 1)
        os.mkdir(directoryPath)



    ## CC (Parte central)
    ruta = 'http://a.tile.openstreetmap.org/'
    ruta += str(zoom)
    ruta += '/'
    ruta += str(xtile)
    ruta += '/'
    ruta += str(ytile)
    ruta += '.png'

    
    if not os.path.isfile('C://Cache/' + str(zoom) + '/' + str(xtile) +  '/' + str(ytile) + '.png'):
      img = urllib.urlopen(ruta)
      f = open('C://Cache/' + str(zoom) + '/' + str(xtile) +  '/' + str(ytile) + '.png','wb')
      f.write(img.read())
      f.close()
    ##CARGA DE LA IMAGEN CC  
    imageFileCC = 'C://Cache/' + str(zoom) + '/' + str(xtile) +  '/' + str(ytile) + '.png'  
    imageCC = ImageTk.PhotoImage(Image.open(imageFileCC))
    cnvs_rutas.create_image(192.0, 192.0,image=imageCC, anchor='nw')

    ## CR (Parte central derecha)
    ruta = 'http://a.tile.openstreetmap.org/'
    ruta += str(zoom)
    ruta += '/'
    ruta += str(xtile + 1)
    ruta += '/'
    ruta += str(ytile)
    ruta += '.png'

    if not os.path.isfile('C://Cache/' + str(zoom) + '/' + str(xtile + 1) +  '/' + str(ytile) + '.png'):
      img = urllib.urlopen(ruta)
      f = open('C://Cache/' + str(zoom) + '/' + str(xtile + 1) +  '/' + str(ytile) + '.png','wb')
      f.write(img.read())
      f.close()
    ##CARGA DE LA IMAGEN CR  
    imageFileCR = 'C://Cache/' + str(zoom) + '/' + str(xtile + 1) +  '/' + str(ytile) + '.png'  
    imageCR = ImageTk.PhotoImage(Image.open(imageFileCR))
    cnvs_rutas.create_image(448.0, 192.0,image=imageCR, anchor='nw')
       
    
    ## CL (Parte central izquierda)
    ruta = 'http://a.tile.openstreetmap.org/'
    ruta += str(zoom)
    ruta += '/'
    ruta += str(xtile - 1)
    ruta += '/'
    ruta += str(ytile)
    ruta += '.png'

    if not os.path.isfile('C://Cache/' + str(zoom) + '/' + str(xtile - 1) +  '/' + str(ytile) + '.png'):
      img = urllib.urlopen(ruta)
      f = open('C://Cache/' + str(zoom) + '/' + str(xtile - 1) +  '/' + str(ytile) + '.png','wb')
      f.write(img.read())
      f.close()
    ##CARGA DE LA IMAGEN CL  
    imageFileCL = 'C://Cache/' + str(zoom) + '/' + str(xtile - 1) +  '/' + str(ytile) + '.png'  
    imageCL = ImageTk.PhotoImage(Image.open(imageFileCL))
    cnvs_rutas.create_image(-64.0, 192.0,image=imageCL, anchor='nw')  

    ## UL (Parte superior izquierda)
    ruta = 'http://a.tile.openstreetmap.org/'
    ruta += str(zoom)
    ruta += '/'
    ruta += str(xtile - 1)
    ruta += '/'
    ruta += str(ytile - 1)
    ruta += '.png'

    if not os.path.isfile('C://Cache/' + str(zoom) + '/' + str(xtile - 1) +  '/' + str(ytile - 1) + '.png'):
      img = urllib.urlopen(ruta)
      f = open('C://Cache/' + str(zoom) + '/' + str(xtile - 1) +  '/' + str(ytile - 1) + '.png','wb')
      f.write(img.read())
      f.close()
    ##CARGA DE LA IMAGEN UL  
    imageFileUL = 'C://Cache/' + str(zoom) + '/' + str(xtile - 1) +  '/' + str(ytile - 1) + '.png'  
    imageUL = ImageTk.PhotoImage(Image.open(imageFileUL))
    cnvs_rutas.create_image(-64.0, -64.0,image=imageUL, anchor='nw')  


     ## UC (Parte superior central)
    ruta = 'http://a.tile.openstreetmap.org/'
    ruta += str(zoom)
    ruta += '/'
    ruta += str(xtile)
    ruta += '/'
    ruta += str(ytile - 1)
    ruta += '.png'

    if not os.path.isfile('C://Cache/' + str(zoom) + '/' + str(xtile) +  '/' + str(ytile - 1) + '.png'):
      img = urllib.urlopen(ruta)
      f = open('C://Cache/' + str(zoom) + '/' + str(xtile) +  '/' + str(ytile - 1) + '.png','wb')
      f.write(img.read())
      f.close()
    ##CARGA DE LA IMAGEN UC 
    imageFileUC = 'C://Cache/' + str(zoom) + '/' + str(xtile) +  '/' + str(ytile - 1) + '.png' 
    imageUC = ImageTk.PhotoImage(Image.open(imageFileUC))
    cnvs_rutas.create_image(192.0, -64.0,image=imageUC, anchor='nw')  


     ## UR (Parte superior derecha)
    ruta = 'http://a.tile.openstreetmap.org/'
    ruta += str(zoom)
    ruta += '/'
    ruta += str(xtile + 1)
    ruta += '/'
    ruta += str(ytile - 1)
    ruta += '.png'

    if not os.path.isfile('C://Cache/' + str(zoom) + '/' + str(xtile + 1) +  '/' + str(ytile - 1) + '.png'):
      img = urllib.urlopen(ruta)
      f = open('C://Cache/' + str(zoom) + '/' + str(xtile + 1) +  '/' + str(ytile - 1) + '.png','wb')
      f.write(img.read())
      f.close()
    ##CARGA DE LA IMAGEN UR 
    imageFileUR = 'C://Cache/' + str(zoom) + '/' + str(xtile + 1) +  '/' + str(ytile - 1) + '.png' 
    imageUR = ImageTk.PhotoImage(Image.open(imageFileUR))
    cnvs_rutas.create_image(448.0, -64.0,image=imageUR, anchor='nw')

    ## DL (Parte inferior izquierda)
    ruta = 'http://a.tile.openstreetmap.org/'
    ruta += str(zoom)
    ruta += '/'
    ruta += str(xtile - 1)
    ruta += '/'
    ruta += str(ytile + 1)
    ruta += '.png'

    if not os.path.isfile('C://Cache/' + str(zoom) + '/' + str(xtile - 1) +  '/' + str(ytile + 1) + '.png'):
      img = urllib.urlopen(ruta)
      f = open('C://Cache/' + str(zoom) + '/' + str(xtile - 1) +  '/' + str(ytile + 1) + '.png','wb')
      f.write(img.read())
      f.close()

    ##CARGA DE LA IMAGEN DL 
    imageFileDL = 'C://Cache/' + str(zoom) + '/' + str(xtile - 1) +  '/' + str(ytile + 1) + '.png' 
    imageDL = ImageTk.PhotoImage(Image.open(imageFileDL))
    cnvs_rutas.create_image(-64.0, 448.0,image=imageDL, anchor='nw')

    ##  ## DC (Parte inferior central)
    ruta = 'http://a.tile.openstreetmap.org/'  
    ruta += str(zoom)
    ruta += '/'
    ruta += str(xtile)
    ruta += '/'
    ruta += str(ytile + 1)
    ruta += '.png'

    if not os.path.isfile('C://Cache/' + str(zoom) + '/' + str(xtile) +  '/' + str(ytile + 1) + '.png'):
      img = urllib.urlopen(ruta)
      f = open('C://Cache/' + str(zoom) + '/' + str(xtile) +  '/' + str(ytile + 1) + '.png','wb')
      f.write(img.read())
      f.close()
    ##CARGA DE LA IMAGEN DC 
    imageFileDC = 'C://Cache/' + str(zoom) + '/' + str(xtile) +  '/' + str(ytile + 1) + '.png' 
    imageDC = ImageTk.PhotoImage(Image.open(imageFileDC))
    cnvs_rutas.create_image(192.0, 448.0,image=imageDC, anchor='nw')

    ## DR (Parte inferior derecha)
    ruta = 'http://a.tile.openstreetmap.org/'
    ruta += str(zoom)
    ruta += '/'
    ruta += str(xtile + 1)
    ruta += '/'
    ruta += str(ytile + 1)
    ruta += '.png'

    if not os.path.isfile('C://Cache/' + str(zoom) + '/' + str(xtile + 1) +  '/' + str(ytile + 1) + '.png'):
      img = urllib.urlopen(ruta)
      f = open('C://Cache/' + str(zoom) + '/' + str(xtile + 1) +  '/' + str(ytile + 1) + '.png','wb')
      f.write(img.read())
      f.close()
    ##CARGA DE LA IMAGEN DR
    imageFileDR = 'C://Cache/' + str(zoom) + '/' + str(xtile + 1) +  '/' + str(ytile + 1) + '.png' 
    imageDR = ImageTk.PhotoImage(Image.open(imageFileDR))
    cnvs_rutas.create_image(448.0, 448.0,image=imageDR, anchor='nw')


def mov_izquierda(e):
    global Latmedia
    global Lonmedia
    global ContIzq
    global xtile
    global ytile
    
    
    
    if var3.get() == 1:
        if var2.get() == 0:
            print "Radiobutton: None selected"
        elif var2.get() == 3:
            Lonmedia = Lonmedia - 0.005
        elif var2.get() == 2:
            Lonmedia = Lonmedia - 0.015
        elif var2.get() == 1:
            Lonmedia = Lonmedia - 0.03

        izquierda = mapa_google_map(Latmedia, Lonmedia)

    if var3.get() == 2:
        
        ContIzq = ContIzq + 1
        #xtile, ytile = deg2num(Latmedia, Lonmedia, zoom)
        xtile = xtile -  ContIzq
        ytile = ytile
        osm = mapa_OSM(xtile, ytile)
        return xtile, ytile
    
        
                               

def mov_derecha(e):
    global Latmedia
    global Lonmedia
    global ContDere
    global xtile
    global ytile
    global ContDere
    
    if var3.get() == 1:
        if var2.get() == 0:
            print "Radiobutton: None selected"
        elif var2.get() == 3:
            Lonmedia = Lonmedia + 0.005
        elif var2.get() == 2:
            Lonmedia = Lonmedia + 0.015
        elif var2.get() == 1:
            Lonmedia = Lonmedia + 0.03

        derecha = mapa_google_map(Latmedia, Lonmedia)
        
    if var3.get() == 2:
        
        ContDere = ContDere + 1
        #xtile, ytile = deg2num(Latmedia, Lonmedia, zoom)
        xtile = xtile +  ContDere
        ytile = ytile
        osm = mapa_OSM(xtile, ytile)
        return xtile, ytile
        

def mov_arriba(e):
    global Latmedia
    global Lonmedia
    global ContArrib
    global xtile
    global ytile
    global ContArrib 
  
    
    if var3.get() == 1:
        if var2.get() == 0:
            print "Radiobutton: None selected"
        elif var2.get() == 3:
            Latmedia = Latmedia + 0.005
        elif var2.get() == 2:
            Latmedia = Latmedia + 0.015
        elif var2.get() == 1:
            Latmedia = Latmedia + 0.03

        arriba = mapa_google_map(Latmedia, Lonmedia)
        
    if var3.get() == 2:

        ContArrib = ContArrib - 1        
        #xtile, ytile = deg2num(Latmedia, Lonmedia, zoom)
        xtile = xtile
        ytile = ytile +  ContArrib
        osm = mapa_OSM(xtile, ytile)
        return xtile, ytile
        
 
def mov_abajo(e):
    global Latmedia
    global Lonmedia
    global ContAbaj
    global xtile
    global ytile
    global ContAbaj
    
    if var3.get() == 1:    
        if var2.get() == 0:
            print "Radiobutton: None selected"
        elif var2.get() == 3:
            Latmedia = Latmedia - 0.005
        elif var2.get() == 2:
            Latmedia = Latmedia - 0.015
        elif var2.get() == 1:
            Latmedia = Latmedia - 0.03
    

        abajo = mapa_google_map(Latmedia, Lonmedia)
        
    if var3.get() == 2:
         
        ContAbaj = ContAbaj + 1
        #xtile, ytile = deg2num(Latmedia, Lonmedia, zoom)
        xtile = xtile
        ytile = ytile + ContAbaj
        osm = mapa_OSM(xtile, ytile)
        return xtile, ytile
    
def zoom_in (e):
  global zoom
  global zoom_str
  
  if zoom < 22:
    zoom = zoom + 1

  zoom_str.set('Zoom: '+ str(zoom))  

def zoom_out (e):
  global zoom
  global zoom_str
  
  if zoom > 0:
    zoom = zoom - 1
    
  zoom_str.set('Zoom: '+ str(zoom)) 


def stop_prog(e):
  root.destroy()


##ZOOM..inicializamos las cosas

zoom = 14
zoom_str = Tkinter.StringVar()
zoom_str.set('Zoom: ' + str(zoom))

####CREACION DEL LISTBOX - VENTANA DE INDICACIONES     
Listbox = Tkinter.Listbox(root,height=39,width=40)
Listbox.grid(row=2,column=8)

Scrollbar1 = Tkinter.Scrollbar(root)
Scrollbar1.grid(row=2,column=9,sticky='nsew')

Scrollbar1.config(command=Listbox.yview)
Listbox.config(yscrollcommand=Scrollbar1.set)

Scrollbar2 = Tkinter.Scrollbar(root,orient=Tkinter.HORIZONTAL)
Scrollbar2.grid(row=3,column=8,sticky='nsew')

Scrollbar2.config(command=Listbox.xview)
Listbox.config(xscrollcommand=Scrollbar2.set)


#LABEL ORIGEN Y DESTINO + DURACION + MOVIMIENTO
origen = Tkinter.StringVar()
origen.set('Origen: ')

destino = Tkinter.StringVar()
destino.set('Destino: ')

duracion = Tkinter.StringVar()
duracion.set('La duracion de la ruta es de: ')

horas = Tkinter.StringVar()
horas.set(str(horas) + ' Horas')

minutos = Tkinter.StringVar()
minutos.set(str(minutos) + ' Minutos')

segundos = Tkinter.StringVar()
segundos.set(str(segundos) + ' Segundos')

Desplazamiento =  Tkinter.StringVar()
Desplazamiento.set('Desplazamiento: ')

Tipo_mapa = Tkinter.StringVar()
Tipo_mapa.set('Clase de mapa: ')


#GUI...

cnvs_rutas = Tkinter.Canvas(root, width=scr_w, height= scr_h, bg='grey')
cnvs_rutas.pack()


#CREAMOS LOS BOTONES

btn_ruta = Tkinter.Button(root, text = 'Calcular Ruta',width=10)
btn_exit = Tkinter.Button(root, text = 'Exit',width=8)

btn_zoomin = Tkinter.Button(root, text = 'Zoom in',width=8)
btn_zoomout = Tkinter.Button(root, text = 'Zoom out',width=8)



btn_izquierda= Tkinter.Button(root, text = '˂',width=8)
btn_izquierda.place(x = 650, y = 250)
btn_derecha = Tkinter.Button(root, text = '˃',width=8)
btn_derecha.place(x = 720, y = 250)
btn_arriba = Tkinter.Button(root, text = '˄',width=8)
btn_arriba.place(x = 685, y = 220)
btn_abajo = Tkinter.Button(root, text = '˅',width=8)
btn_abajo.place(x = 685, y = 280)



# Label De Origen y Destino y de la duracion de la ruta

lbl_origen = Tkinter.Label(root, textvariable = origen)
lbl_destino = Tkinter.Label(root, textvariable = destino)

lbl_duracion = Tkinter.Label(root, textvariable = duracion)
lbl_horas = Tkinter.Label(root, textvariable = horas)
lbl_minutos = Tkinter.Label(root, textvariable = minutos)
lbl_segundos = Tkinter.Label(root, textvariable = segundos)

lbl_desplazamiento = Tkinter.Label(root, textvariable = Desplazamiento)

lbl_mapa = Tkinter.Label(root, textvariable = Tipo_mapa)

# Label del ZOOM  - Arriba esta inicializado el zoom
lbl_zoom = Tkinter.Label(root, textvariable = zoom_str)

## Creamos el texto de entrada de origen y destino

var_str = str()
origen_text = Tkinter.Entry(root,textvariable=var_str)
origen_text.grid(row=6,column=1)


var_str2 = str()
destino_text = Tkinter.Entry(root,textvariable=var_str2)
destino_text.grid(row=6,column=3)


##CREACION DE LOS CHECKBUTTON DEL TIPO DE MAPA
    
    
var = Tkinter.IntVar()

roadmap = Tkinter.Radiobutton(root, text="Roadmap", variable=var, value=4)
roadmap.grid(row=7,column=0)


Satellite = Tkinter.Radiobutton(root, text="Satellite", variable=var, value=3)
Satellite.grid(row=7,column=1)


Hybrid = Tkinter.Radiobutton(root, text="Hybrid", variable=var, value=2)
Hybrid.grid(row=7,column=2)


Terrain = Tkinter.Radiobutton(root, text="Terrain", variable=var, value=1)
Terrain.grid(row=7,column=3)

##CREACION DE LOS CHECKBUTTON DEL TIPO DE DESPLAZAMIENTO

var2 = Tkinter.IntVar()

desp1 = Tkinter.Radiobutton(root, text="Pequeño", variable=var2, value=3)
desp1.place(x = 675, y = 350)


desp2 = Tkinter.Radiobutton(root, text="Mediano", variable=var2, value=2)
desp2.place(x =  675, y = 380)


desp3 = Tkinter.Radiobutton(root, text="Grande", variable=var2, value=1)
desp3.place(x =  675, y = 410)

##CREACION DE LOS CHECKBUTTON DEL TIPO DE MAPA A EMPLEAR

var3 = Tkinter.IntVar()

OSM = Tkinter.Radiobutton(root, text="OpenStreetMap", variable=var3, value=2)
OSM.place(x =  675, y = 470)


GM = Tkinter.Radiobutton(root, text="GooogleMaps", variable=var3, value=1)
GM.place(x =  675, y = 500)


### Packaging

cnvs_rutas.grid(row = 0, columnspan= 5, rowspan = 5)

btn_ruta.grid(row=6,column=5)
lbl_origen.grid(row=6,column=0)
lbl_destino.grid(row=6,column=2)
btn_exit.grid(row=6,column=8)

lbl_duracion.grid(row=8,column=1)
lbl_horas.grid(row=8,column=2)
lbl_minutos.grid(row=8,column=3)
lbl_segundos.grid(row=8,column=4)

btn_zoomin.grid(row=7,column=4)
btn_zoomout.grid(row=7,column=6)
lbl_zoom.grid(row=7,column=5)

lbl_desplazamiento.place(x = 650, y = 320)
lbl_mapa.place(x = 650, y = 440)

## FUNCION DE LOS BOTONES
btn_zoomin.bind('<Button-1>',zoom_in)
btn_zoomout.bind('<Button-1>',zoom_out)
btn_exit.bind('<Button-1>',stop_prog)
btn_ruta.bind('<Button-1>',Calculo_Rutas)


btn_izquierda.bind('<Button-1>',mov_izquierda)
btn_derecha.bind('<Button-1>',mov_derecha)
btn_arriba.bind('<Button-1>',mov_arriba)
btn_abajo.bind('<Button-1>',mov_abajo)

root.mainloop()
