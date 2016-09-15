# -*- coding: utf-8 -*-

import datetime
import pandas as pd
import os
import re

from sqlite3 import connect
from os import walk
from os.path import isfile, join, splitext

class ReporteadorArchivos(object):
  """
  Esta clase crea los diversos reportes que tienen que ver con los archivos
  físicos y archivos registrados en la base de datos correspondientes a cada
  entrega. Estos reportes son:

  1. Archivos registrados en la base de datos y entregados completos.
  2. Archivos registrados en la base de datos y entregados incompletos (peso 0)
  3. Archivos registrados en la base de datos y no entregados
  4. Archivos anexos (no registrados en la base) y entregados incompletos
  5. Archivos anexos (no registrados en la base) y entregados completos
  """

  def __init__(self, ruta_sqlite, ruta_entrega, ruta_query_sql):
    super(ReporteadorArchivos, self).__init__()

    # extensiones aceptadas
    self.extensiones = ["wav","midi","mp3","jpg","jpeg","png","avi","mp4","txt","pdf"]

    # reporte de archivos registrados en la BD y entregados completos
    self.REPORTE_OK_NOMBRE = "ok"
    self.REPORTE_OK_TIPO = "csv"

    # reporte de archivos registrados en la BD y entregados incompletos
    self.REPORTE_INCOMPLETOS_NOMBRE = "incompletos"
    self.REPORTE_INCOMPLETOS_TIPO = "csv"

    # reporte de archivos registrados en la BD y no entregados
    self.REPORTE_FALTANTES_NOMBRE = "faltantes"
    self.REPORTE_FALTANTES_TIPO = "csv"

    # reporte de archivos entregados en "datos_anexos", completos y no registrados
    # en la BD (con su nombre original)
    self.REPORTE_ANEXOS_COMPLETOS_NOMBRE = "anexos_completos"
    self.REPORTE_ANEXOS_COMPLETOS_TIPO = "csv"

    # reporte de archivos entregados en "datos_anexos", incompletos y no registrados
    # en la BD (con su nombre original)
    self.REPORTE_ANEXOS_INCOMPLETOS_NOMBRE = "anexos_incompletos"
    self.REPORTE_ANEXOS_INCOMPLETOS_TIPO = "csv"

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

    # lista de archivos anexos y con peso > 0
    self.lista_archivos_anexos_completos = []

    # lista de archivos anexos y con peso 0
    self.lista_archivos_anexos_incompletos = []

    # reporte de archivos registrados en la base y entregados completos
    self.reporte_ok = []

    # reporte de archivos registrados en la base y entregados incompletos
    self.reporte_incompletos = []

    # reporte de archivos registrados en la base y no entregados
    self.reporte_no_entregados = []

    # reporte de archivos anexos no registrados en la base y entregados completos
    self.reporte_anexos_completos = []

    # reporte de archivos anexos no registrados en la base y entregados incompletos
    self.reporte_anexos_incompletos = []

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
  # "lista_archivos_anexos_completos" (si su ruta contiene "datos_anexos" y su peso es >0)
  # "lista_archivos_anexos_incompletos" (si su ruta contiene "datos_anexos" y su peso es =0)

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

          if os.stat(datos_archivo['ruta']).st_size > 0:
            self.lista_archivos_entregados_completos.append(datos_archivo)

            if bool(re.search('datos_anexos', datos_archivo['ruta'])):
              self.lista_archivos_anexos_completos.append(datos_archivo)
          else:
            self.lista_archivos_entregados_incompletos.append(datos_archivo)

            if bool(re.search('datos_anexos', datos_archivo['ruta'])):
              self.lista_archivos_anexos_incompletos.append(datos_archivo) 

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

# TODO: Cachar las excepciones en las listas vacias para los metodos que intersectan, unen y restan

  def intersectar_listas_registrados_entregados(self, lista_archivos_registrados,
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


  def unir_listas_entregados(self, lista_archivos_entregados_completos,
    lista_archivos_entregados_incompletos):

    data_frame_archivos_entregados_completos = pd.DataFrame(lista_archivos_entregados_completos)
    data_frame_archivos_entregados_incompletos = pd.DataFrame(lista_archivos_entregados_incompletos)

    union = data_frame_archivos_entregados_completos.append(
      data_frame_archivos_entregados_incompletos, ignore_index=True).drop_duplicates(
      subset = ['nombre'], keep = 'first').sort_values(
      ['nombre'])

    # Regresamos el resultado como una nueva lista de diccionarios.
    return union.T.to_dict().values()

  def restar_listas_registrados_entregados(self, lista_archivos_registrados,
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

  # La diferencia entre "restar_listas_registrados_entregados()" y
  # "restar_listas_anexos_registrados()" es:
  # 1. El orden de la diferencia
  # 2. La llave sobre la cuál se realiza esta: "nombre_web2py" vs "nombre_original"

  def restar_listas_anexos_registrados(self, lista_archivos_anexos,
      lista_archivos_registrados):

    data_frame_archivos_anexos = pd.DataFrame(lista_archivos_anexos)
    data_frame_archivos_registrados = pd.DataFrame(lista_archivos_registrados)

    diferencia_llaves = set(data_frame_archivos_anexos.nombre).difference(
      data_frame_archivos_registrados.nombre_original)

    indices_diferencia = data_frame_archivos_anexos.nombre.isin(
      diferencia_llaves)

    diferencia = data_frame_archivos_anexos[indices_diferencia].drop_duplicates(
      subset = ['nombre'], keep = 'first').sort_values(['nombre'])

    # Regresamos el resultado como una nueva lista de diccionarios.
    return diferencia.T.to_dict().values()

  def crear_reportes(self): #file,record,modo):

    # interseccion archivos registrados contra archivos entregados completos
    # = Archivos en db y entregados completos
    self.reporte_ok = self.intersectar_listas_registrados_entregados(
      self.lista_archivos_registrados, self.lista_archivos_entregados_completos)

    # intersección archivos registrados contra archivos entregados e incompletos
    # = Archivos en db y entregados incompletos
    self.reporte_incompletos = self.intersectar_listas_registrados_entregados(
      self.lista_archivos_registrados, self.lista_archivos_entregados_incompletos)

    # 'lista_archivos_entregados' es una variable auxiliar
    lista_archivos_entregados = self.unir_listas_entregados(
      self.lista_archivos_entregados_completos,
      self.lista_archivos_entregados_incompletos)

    # diferencia entre archivos registrados y entregados:
    # = Archivos registrados y no entregados
    self.reporte_no_entregados = self.restar_listas_registrados_entregados(
      self.lista_archivos_registrados, lista_archivos_entregados)

    # diferencia entre archivos anexos completos y archivos registrados:
    # = Archivos anexos no registrados y completos.

    self.reporte_anexos_completos = self.restar_listas_anexos_registrados(
      self.lista_archivos_anexos_completos, self.lista_archivos_registrados)

    # diferencia entre archivos anexos incompletos y archivos registrados:
    # = Archivos anexos no registrados e incompletos.

    self.reporte_anexos_incompletos = self.restar_listas_anexos_registrados(
      self.lista_archivos_anexos_incompletos, self.lista_archivos_registrados)
      
    #imprimiendo reportes:
    pd.DataFrame(self.reporte_ok).to_csv(
      self.REPORTE_OK_NOMBRE + "." + self.REPORTE_OK_TIPO, encoding='utf-8')

    pd.DataFrame(self.reporte_incompletos).to_csv(
      self.REPORTE_INCOMPLETOS_NOMBRE + "." + self.REPORTE_INCOMPLETOS_TIPO,
      encoding='utf-8')

    pd.DataFrame(self.reporte_no_entregados).to_csv(
      self.REPORTE_FALTANTES_NOMBRE + "." + self.REPORTE_FALTANTES_TIPO,
      encoding='utf-8')

    pd.DataFrame(self.reporte_anexos_completos).to_csv(
      self.REPORTE_ANEXOS_COMPLETOS_NOMBRE + "." + self.REPORTE_ANEXOS_COMPLETOS_TIPO,
      encoding='utf-8')

    pd.DataFrame(self.reporte_anexos_incompletos).to_csv(
      self.REPORTE_ANEXOS_INCOMPLETOS_NOMBRE + "." + self.REPORTE_ANEXOS_INCOMPLETOS_TIPO,
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

  def generar_insert_sql(self):
    # insert into ARCHIVO_CAMARA (id,camara_id,archivo_nombre_original,archivo,presencia,nombre_comun,nombre_cientifico,numero_individuo) VALUES ('conglomerado','fecha','gatito.jpg', 'd41d8cd98f00b204e9800998ecf8427e', NULL,NULL,NULL,1);
    inicio_tablas = "insert into ARCHIVO_CAMARA (camara_id,archivo_nombre_original,archivo,presencia,nombre_comun,nombre_cientifico,numero_individuos) VALUES ("
    fin_tablas = ");"


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


