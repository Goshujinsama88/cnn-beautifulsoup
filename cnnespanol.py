# -----------------------------------------------------------------------------------------------------------
#
#               CNN en español web scrapping script para Ucrania
#
# Este script hace web scrapping en la página de CNN en español para la busqueda del termino Ucrania.
# Lo anterior es debido a que se me hace un tema de interés actual en todo el mundo, por
# lo que se me ocurrió realizar una pequeño script que recopilara datos sobre el tema.
# Este script también puede ser utilizado con urls de otras busquedas en CNN en español.
#
# Script creado por: Guadalupe Fernando Escutia Rodríguez.
# Página web: https://ferplace.site
# GitHub: https://github.com/Goshujinsama88
#
# ------------------------------------------------------------------------------------------------------------

#Importamos las librerías necesarias
import pandas as pd
import requests
from bs4 import BeautifulSoup as bso

#Definimos nuestra URL con la que trabajaremos en un principio
url = 'https://cnnespanol.cnn.com/?s=ucrania'

#Hacemos petición a URL y creamos nuestra "sopa"
print('Tratando de realizar la petición a la URL...\n')
try:
    r = requests.get(url, verify=True)
    soup = bso(r.text, 'lxml')
except:
    print('No se ha podido obtener la URL de la búsqueda o información de la misma.\n')
    exit()
    
#Creamos un dataframe con solo los nombres de columnas
cNames = ['Título', 'Autor', 'Fecha', 'Texto', 'URL']

df = pd.DataFrame(columns=cNames)

#Definimos algunas variables para hacer loops
i = 0
j = 0

print('Intentando obtener el número total de páginas relacionadas a la búsqueda...\n')
try:
    tPages = int(soup.find_all("a", class_="page-numbers")[-2].get_text()) - 1
except:
    print('No se ha podido obtener el número de páginas.\n')
    exit()

#Iniciamos el loop para las páginas
while i <= tPages:
    
    #Recargamos los datos de petición si el loop ya hizo su primer bucle
    if i > 0:
        print('Intentando hacer petición a la URL de la siguiente página...\n')
        try:
            r = requests.get(url, verify=True)
            soup = bso(r.text, 'lxml')
        except:
            print('No se ha podido completar la solicitud a la URL.\n')
            exit()
        
    #Comenzamos bucle por los artículos de la página
    for j in soup.find_all('h2', class_='news__title'):
        
        #Hacemos petición a la página del artículo
        print('Intentando realizar petición a página de artículo...\n')
        urld = j.find('a')['href']
        
        try:
            r1 = requests.get(urld, verify=True)
            soup1 = bso(r1.text, 'lxml')
        except:
            print('No se ha podido realizar la petición al artículo.\n')
            exit()
            
        #Revisamos que el artículo no sea un vídeo
        print('Revisando que no se trate de un artículo de vídeo...\n')
        if not "video" in urld:
            
            print('Extrayendo datos...\n')
            try:
                #Obtenemos tanto el titulo del articulo como el autor de dicho articulo
                title = soup1.find_all('h1', class_='storyfull__title')[0].get_text()
                autor = soup1.find_all('p', class_='storyfull__authors')[0].find('a').get_text()
            
                #Obtenemos y damos formato a la fecha
                fech = soup1.find_all('time', class_='storyfull__time')[0].get_text()
                fech0 = fech.split(") ", 1)[1]
                fecha = fech0.replace(',','')
            
                #Definimos variables para el loop para extraer el texto
                k = 0
                n = 0
            
                #Iniciamos con el loop para la extracción del texto
                for k in soup1.find_all('p'):
                
                    if n == 0:
                        text = k.get_text()
                        n = 1
                    else:
                        text = text + '\n' + k.get_text()
                    
                #Añadimos una nueva fila al dataframe con los datos extraidos de la pagina
                df.loc[df.shape[0]] = [title, autor, fecha, text, urld]
            
            except:
                print('No se ha podido obtener datos del articulo.\n')
                exit()
    
    print('Intentando obtener URL de la siguiente página...\n')
    #Actualizamos la url
    try:
        url = soup.find_all('a', class_="page-numbers")[-1]["href"]
    except:
        print('No se ha podido obtener la nueva URL...\n')
        
        print("Intentando escribir archivo de Excel con los datos que se pudieron obtener...\n")
        if df.shape[0] >= 1:
            df.to_excel("cnn_ucrania.xlsx")
        
        exit()
    
    i = i+1

#Escribimos los datos a un archivo de excel 
print("Intentando escribir archivo de excel con los datos...\n")   
df.to_excel("cnn_ucrania.xlsx")