from classSnmbReporte import ReporteadorArchivos

ruta_entrega="/LUSTRE/users/omaranda/sacmod/respaldos/conanp/2016_02_23_conanp"
ruta_sqlite="/opt/snmb-sqlite/sqliteDBs/2016_03_04_conanp_2016_02_23_v10_v12.sqlite"
ruta_query_sql="/LUSTRE/users/omaranda/bin/snmb/query_base.sql"

x = ReporteadorArchivos(ruta_sqlite,ruta_entrega,ruta_query_sql)

# Enlistar archivos

x.enlistar_archivos()

print "Enlistar archivos\n"
print x.lista_archivos_entregados_completos
print x.lista_archivos_entregados_incompletos
print x.lista_archivos_anexos_completos
print x.lista_archivos_anexos_incompletos

# Enlistar archivos registrados en la base de datos

x.enlistar_archivos_registrados_bd()

print "Enlistar archivos registrados BD\n"
print x.lista_archivos_registrados

# Crear reportes:
x.crear_reportes()

print "Reporte ok: archivos registrados en BD y entregados completos (en uploads)\n"
print x.reporte_ok

print "Reporte de archivos registrados en BD y entregados incompletos (en uploads)\n"
print x.reporte_incompletos

print "Reporte de archivos registrados en BD y no entregados (en uploads)\n"
print x.reporte_no_entregados

print "Reporte de archivos anexos no registrados en BD y completos\n"
print x.reporte_anexos_completos

print "Reporte de archivos anexos no registrados en BD y incompletos\n"
print x.reporte_anexos_incompletos
