from classSnmbReporte import CrearReporte

ruta_entrega="2016_02_23_conanp"
ruta_sqlite="2016_03_04_conanp_2016_02_23_v10_v12.sqlite"
ruta_query_sql="query_base.sql"

x = CrearReporte(ruta_sqlite,ruta_entrega,ruta_query_sql)

x.enlistar_archivos()
x.enlistar_archivos_registrados_bd()
print x.intersectar_listas(x.lista_archivos_registrados, x.lista_archivos_entregados_completos)
lista_union = x.unir_listas(x.lista_archivos_entregados_completos, x.lista_archivos_entregados_incompletos)
print "\n"
print len(x.lista_archivos_registrados)
print len(x.restar_listas(x.lista_archivos_registrados, lista_union))
