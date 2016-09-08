# -*- coding: utf-8 -*-

import datetime
import pandas as pd
import os

from sqlite3 import connect
from os import walk
from os.path import isfile, join, splitext

class CrearReporte(object):
  """docstring for CreateReport"""

  def __init__(self, ruta_sqlite, ruta_entrega, ruta_query_sql):
    super(CrearReporte, self).__init__()

    # extensiones aceptadas
    self.extensiones = ["wav","midi","mp3","jpg","jpeg","png","avi","mp4","txt","pdf"]

    # cada archivo registrado en la BD tendrá una de tres posibles etiquetas
    self.OK_TAG = ["OK","En BD y en archivos, con peso > 0"]
    self.INCOMPLETOS_TAG = ["I","En BD y en archivos, pero con peso 0"]
    self.FALTANTES_TAG = ["F", "En BD, pero no en archivos"]

    # reporte de archivos con etiqueta OK
    self.REPORTE_OK_NOMBRE = "ok"
    self.REPORTE_OK_TIPO = "csv"

    # reporte de archivos con etiqueta de incompletos
    self.REPORTE_INCOMPLETOS_NOMBRE = "incompletos"
    self.REPORTE_INCOMPLETOS_TIPO = "csv"

    # reporte de archivos con etiqueta de faltantes
    self.REPORTE_FALTANTES_NOMBRE = "faltantes"
    self.REPORTE_FALTANTES_TIPO = "csv"


    #self.AUDIO_TAG = "audios"
    #self.IMAGE_TAG = "imagenes"
    #self.VIDEO_TAG = "videos"

    #self.file_col_name = "archivo"

    # path a la base de datos fusionada correspondiente a la entrega (para
    # obtener los archivos registrados en la base de datos)
    self.ruta_sqlite = ruta_sqlite

    # path hacia el query (archivo SQL) para obtener la lista de archivos de la
    # base de datos
    self.ruta_query_sql = ruta_query_sql
    # El query debe regresar los siguientes campos en orden:
    # 0. Número de conglomerado
    # 1. Fecha de visita del conglomerado
    # 2. Institución (CONAFOR, CONANP, FMCN)
    # 3. Nombre Web2py del archivo (por ejemplo, para buscarlo en la carpeta de Uploads)
    # 4. Nombre original del archivo
    # 5. Tipo de archivo (tabla de la que proviene). Por ejemplo: "Imagen_referencia_sitio"

    # path hacia el directorio de la entrega (para enlistar los archivos
    # entregados físicamente)
    self.ruta_entrega = ruta_entrega

    # lista de archivos entregados físicamente y con peso > 0
    self.lista_archivos_entregados_completos = []

    # lista de archivos entregados físicamente y con peso 0
    self.lista_archivos_entregados_incompletos = []

    # lista de archivos registrados en la BD
    self.lista_archivos_registrados = []

    # reporte OK
    self.reporte_ok = []

    # reporte de archivos incompletos
    self.reporte_incompletos = []

    # reporte de archivos no entregados
    self.reporte_no_entregados = []

    self.fecha = datetime.date.today()

    #self.audio_files = []
    #self.image_files = []
    #self.video_files = []

    #self.audio_dbrecord = []
    #self.image_dbrecord = []
    #self.video_dbrecord = []

    #self.audio_str_report = []
    #self.image_str_report = []
    #self.video_str_report = []

    #self.audio_num_report = []
    #self.image_num_report = []
    #self.video_num_report = []

    # self.all_files_str_report = []
    # self.all_files_num_report = []

    # alist, blist, clist, dlist, elist = ([] for i in range(5))

  # enlistar_archivos() sirve para leer cada archivo en la entrega, y si su
  # extensión está entre las consideradas, ponerlo en la lista correspondiente:
  # "lista_archivos_entregados_completos"
  # "lista_archivos_entregados_incompletos"
  # dependiendo si su peso es 0 o mayor que 0.

  def enlistar_archivos(self):
    for path, subdirs, archivos in walk(self.ruta_entrega):
      for nombre_archivo in archivos:

        # Por eficiencia, no creo el diccionario con la información del archivo
        # hasta que sea estríctamente necesario
        extension = splitext(nombre_archivo)[1][1:].strip().lower()

        if extension in self.extensiones:

          datos_archivo = {
            "nombre": nombre_archivo,
            "ruta": os.path.join(path, nombre_archivo),
            "extension": extension
          }

    	  #print datos_archivo

          if os.stat(datos_archivo['ruta']).st_size > 0:
            self.lista_archivos_entregados_completos.append(datos_archivo)
          else:
            self.lista_archivos_entregados_incompletos.append(datos_archivo)
    print self.lista_archivos_entregados_completos
    print self.lista_archivos_entregados_incompletos

  def enlistar_archivos_registrados_bd(self):
    cursor = connect(self.ruta_sqlite).cursor()
    query = self.obtener_query()

    cursor.execute(query)
    registros = cursor.fetchall()

    # Cada registro es un arreglo (2,3, etc) de datos. Por ello, conviene estandarizar
    # las columnas que regresarán los queries, así como el orden de éstas:
    # El query debe regresar los siguientes campos en orden:
    # 0. Número de conglomerado
    # 1. Fecha de visita del conglomerado
    # 2. Institución (CONAFOR, CONANP, FMCN)
    # 3. Nombre Web2py del archivo (por ejemplo, para buscarlo en la carpeta de Uploads)
    # 4. Nombre original del archivo
    # 5. Tipo de archivo (tabla de la que proviene). Por ejemplo: "Imagen_referencia_sitio"

    for registro in registros:

      if registro:
        extension = splitext(registro[3])[1][1:].strip().lower()

        if extension in self.extensiones:

          datos_archivo = {
            "conglomerado": registro[0],
            "fecha_visita": registro[1],
            "institucion": registro[2],
            "nombre_web2py": registro[3],
            "nombre_original": registro[4],
            "tabla": registro[5],
            "extension": extension
          }

          self.lista_archivos_registrados.append(datos_archivo)
    #print self.lista_archivos_registrados

  def intersectar_listas(self, lista_archivos_registrados,
    lista_archivos_entregados):

    data_frame_archivos_registrados = pd.DataFrame(lista_archivos_registrados)
    data_frame_archivos_entregados = pd.DataFrame(lista_archivos_entregados)

    # merge es un join.
    interseccion = data_frame_archivos_registrados.merge(
      data_frame_archivos_entregados, how='inner',
      left_on=['nombre_web2py'], right_on=['nombre']).drop_duplicates(
      subset = ['nombre_web2py'], keep = 'first').sort_values(
      ['conglomerado', 'fecha_visita'])

    # Regresamos el resultado como una nueva lista de diccionarios.
    return interseccion.T.to_dict().values()


  def unir_listas(self, lista_archivos_entregados_completos,
    lista_archivos_entregados_incompletos):

    data_frame_archivos_entregados_completos = pd.DataFrame(lista_archivos_entregados_completos)
    data_frame_archivos_entregados_incompletos = pd.DataFrame(lista_archivos_entregados_incompletos)

    union = data_frame_archivos_entregados_completos.append(
      data_frame_archivos_entregados_incompletos, ignore_index=True).drop_duplicates(
      subset = ['nombre'], keep = 'first').sort_values(
      ['nombre'])

    # Regresamos el resultado como una nueva lista de diccionarios.
    return union.T.to_dict().values()

  def restar_listas(self, lista_archivos_registrados,
    lista_archivos_entregados):

    data_frame_archivos_registrados = pd.DataFrame(lista_archivos_registrados)
    data_frame_archivos_entregados = pd.DataFrame(lista_archivos_entregados)

    diferencia_llaves = set(data_frame_archivos_registrados.nombre_web2py).difference(
      data_frame_archivos_entregados.nombre)

    indices_diferencia = data_frame_archivos_registrados.nombre_web2py.isin(
      diferencia_llaves)

    diferencia = data_frame_archivos_registrados[indices_diferencia].drop_duplicates(
      subset = ['nombre_web2py'], keep = 'first').sort_values(
      ['conglomerado', 'fecha_visita'])

    # Regresamos el resultado como una nueva lista de diccionarios.
    return diferencia.T.to_dict().values()

  def crear_reportes(self,file,record,modo):

    # interseccion archivos registrados contra archivos entregados completos
    # = Archivos en db y entregados completos
    self.reporte_ok = intersectar_listas(self.lista_archivos_registrados,
      self.lista_archivos_entregados_completos)

    # intersección archivos registrados contra archivos entregados e incompletos
    # = Archivos en db y entregados incompletos
    self.reporte_incompletos = intersectar_listas(self.lista_archivos_registrados,
      self.lista_archivos_entregados_incompletos)

    # 'lista_archivos_entregados' es una variable auxiliar
    lista_archivos_entregados = unir_listas(self.lista_archivos_entregados_completos,
      self.lista_archivos_entregados_incompletos)

    # diferencia entre archivos registrados y entregados:
    # = Archivos registrados y no entregados
    self.reporte_no_entregados = restar_listas(self.lista_archivos_registrados,
      lista_archivos_entregados)
      
    #imprimiendo reportes:
    pd.DataFrame(self.reporte_ok).to_csv("reporte_ok.csv", encoding='utf-8')
    pd.DataFrame(self.reporte_incompletos).to_csv("reporte_incompletos.csv",
      encoding='utf-8')
    pd.DataFrame(self.reporte_incompletos).to_csv("reporte_no_entregados.csv",
      encoding='utf-8')

    #if modo:
      #return [len(self.reporte_ok),len(self.reporte_incompletos),len(in_file_not_db)]
    #else:
      #return [in_file_in_db,in_db_not_file,in_file_not_db]

  # def generate_data(self):
  #   # needs list files and db
  #   # self.list_dbrecord()
  #   # self.list_files()

  #   self.audio_str_report = self.analize_documents(self.get_audio_files(),self.get_audio_dbrecord(),False)
  #   self.image_str_report = self.analize_documents(self.get_image_files(),self.get_image_dbrecord(),False)
  #   self.video_str_report = self.analize_documents(self.get_video_files(),self.get_video_dbrecord(),False)

  #   self.audio_num_report = self.analize_documents(self.get_audio_files(),self.get_audio_dbrecord(),True)
  #   self.image_num_report = self.analize_documents(self.get_image_files(),self.get_image_dbrecord(),True)
  #   self.video_num_report = self.analize_documents(self.get_video_files(),self.get_video_dbrecord(),True)

  def generar_archivos_reportes(self,files,records,tag):
    
    

    ofile = open(self.FILES_TAG + "_" + tag + "_" + str(self.date) +"." + self.FILES_TYPE, 'w')

    data = [
    "[ "+ self.OK_TAG[0] + " = " + self.OK_TAG[1] + " ]\n",
    "[ "+ self.MISSING_ON_DB_TAG[0] + " = " + self.MISSING_ON_DB_TAG[1] + " ]\n",
    "[ "+ self.MISSING_ON_FILES_TAG[0] + " = " + self.MISSING_ON_FILES_TAG[1] + " ]\n",
    "\n"
    ]

    if tag == self.AUDIO_TAG:
      report = self.audio_str_report
    elif tag == self.IMAGE_TAG:
      report = self.image_str_report
    elif tag == self.VIDEO_TAG:
      report = self.video_str_report

    for record in records:
      if record in report[1]:
        # si esta en db pero no en fisico
        data.append(self.MISSING_ON_FILES_TAG[0] +" " + record + "\n")

    for file in files:
      if file in report[0]:
        # si esta en db y en fisico
        data.append(self.OK_TAG[0] +" " + file + "\n")
      elif file in report[2]:
        # si esta en fisico pero no en db
        data.append(self.MISSING_ON_DB_TAG[0] +" " + file + "\n")

    ofile.write(''.join(l for l in data))
    ofile.close()

  def generate_report_files(self):
     self.generate_crude_file(self.get_audio_files(), self.get_audio_dbrecord(), self.AUDIO_TAG)
     self.generate_crude_file(self.get_image_files(), self.get_image_dbrecord(), self.IMAGE_TAG)
     self.generate_crude_file(self.get_video_files(), self.get_video_dbrecord(), self.VIDEO_TAG)

  def obtener_query(self):
    with open(self.ruta_query_sql, 'r') as archivo:
      query = archivo.read()
      return query

    return ["SELECT "+ self.file_col_name +" FROM "+t[0] for t in self.tables]

  def get_supported_files(self):
    return self.audio_ext + self.image_ext + self.video_ext

  def get_files(self):
    return self.audio_files + self.image_files + self.video_files

  def get_audio_files(self):
    return self.audio_files

  def get_image_files(self):
    return self.image_files

  def get_video_files(self):
    return self.video_files

  def get_dbrecord(self):
    return self.audio_dbrecord + self.image_dbrecord + self.video_dbrecord

  def get_audio_dbrecord(self):
    return self.audio_dbrecord

  def get_image_dbrecord(self):
    return self.image_dbrecord

  def get_video_dbrecord(self):
    return self.video_dbrecord

  def get_audio_report(self,mode):
    if mode:
      return self.audio_num_report
    else:
      return self.audio_str_report

  def get_image_report(self,mode):
    if mode:
      return self.image_num_report
    else:
      return self.image_str_report

  def get_video_report(self,mode):
    if mode:
      return self.video_num_report
    else:
      return self.video_str_report

