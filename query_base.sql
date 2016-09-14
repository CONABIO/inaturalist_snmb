-- Archivos por conglomerado
--  Imagen_referencia_sitio
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Imagen_referencia_sitio.archivo,
Imagen_referencia_sitio.archivo_nombre_original,
'Imagen_referencia_sitio' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Sitio_muestra
ON Conglomerado_muestra.id = Sitio_muestra.conglomerado_muestra_id
INNER JOIN Imagen_referencia_sitio
ON Sitio_muestra.id = Imagen_referencia_sitio.sitio_muestra_id
UNION
-- Imagen_referencia_camara
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Imagen_referencia_camara.archivo,
Imagen_referencia_camara.archivo_nombre_original,
'Imagen_referencia_camara' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Sitio_muestra
ON Conglomerado_muestra.id = Sitio_muestra.conglomerado_muestra_id
INNER JOIN Camara
ON Sitio_muestra.id = Camara.sitio_muestra_id
INNER JOIN Imagen_referencia_camara
ON Camara.id = Imagen_referencia_camara.camara_id
UNION
-- Archivo_camara
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_camara.archivo,
Archivo_camara.archivo_nombre_original,
'Archivo_camara' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Sitio_muestra
ON Conglomerado_muestra.id = Sitio_muestra.conglomerado_muestra_id
INNER JOIN Camara
ON Sitio_muestra.id = Camara.sitio_muestra_id
INNER JOIN Archivo_camara
ON Camara.id = Archivo_camara.camara_id
UNION
-- Imagen_referencia_grabadora
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Imagen_referencia_grabadora.archivo,
Imagen_referencia_grabadora.archivo_nombre_original,
'Imagen_referencia_grabadora' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Sitio_muestra
ON Conglomerado_muestra.id = Sitio_muestra.conglomerado_muestra_id
INNER JOIN Grabadora
ON Sitio_muestra.id = Grabadora.sitio_muestra_id
INNER JOIN Imagen_referencia_grabadora
ON Grabadora.id = Imagen_referencia_grabadora.grabadora_id
UNION
-- Imagen_referencia_microfonos
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Imagen_referencia_microfonos.archivo,
Imagen_referencia_microfonos.archivo_nombre_original,
'Imagen_referencia_microfonos' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Sitio_muestra
ON Conglomerado_muestra.id = Sitio_muestra.conglomerado_muestra_id
INNER JOIN Grabadora
ON Sitio_muestra.id = Grabadora.sitio_muestra_id
INNER JOIN Imagen_referencia_microfonos
ON Grabadora.id = Imagen_referencia_microfonos.grabadora_id
UNION
-- Archivo_referencia_grabadora
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_referencia_grabadora.archivo,
Archivo_referencia_grabadora.archivo_nombre_original,
'Archivo_referencia_grabadora' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Sitio_muestra
ON Conglomerado_muestra.id = Sitio_muestra.conglomerado_muestra_id
INNER JOIN Grabadora
ON Sitio_muestra.id = Grabadora.sitio_muestra_id
INNER JOIN Archivo_referencia_grabadora
ON Grabadora.id = Archivo_referencia_grabadora.grabadora_id
UNION
-- Archivo_grabadora
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_grabadora.archivo,
Archivo_grabadora.archivo_nombre_original,
'Archivo_grabadora' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Sitio_muestra
ON Conglomerado_muestra.id = Sitio_muestra.conglomerado_muestra_id
INNER JOIN Grabadora
ON Sitio_muestra.id = Grabadora.sitio_muestra_id
INNER JOIN Archivo_grabadora
ON Grabadora.id = Archivo_grabadora.grabadora_id
UNION
-- Archivo_especie_invasora
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_especie_invasora.archivo,
Archivo_especie_invasora.archivo_nombre_original,
'Archivo_especie_invasora' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Transecto_especies_invasoras_muestra
ON Conglomerado_muestra.id = Transecto_especies_invasoras_muestra.conglomerado_muestra_id
INNER JOIN Especie_invasora
ON Transecto_especies_invasoras_muestra.id = Especie_invasora.transecto_especies_invasoras_id
INNER JOIN Archivo_especie_invasora
ON Especie_invasora.id = Archivo_especie_invasora.especie_invasora_id
UNION
-- Archivo_huella_excreta
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_huella_excreta.archivo,
Archivo_huella_excreta.archivo_nombre_original,
'Archivo_huella_excreta' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Transecto_huellas_excretas_muestra
ON Conglomerado_muestra.id = Transecto_huellas_excretas_muestra.conglomerado_muestra_id
INNER JOIN Huella_excreta
ON Transecto_huellas_excretas_muestra.id = Huella_excreta.transecto_huellas_excretas_id
INNER JOIN Archivo_huella_excreta
ON Huella_excreta.id = Archivo_huella_excreta.huella_excreta_id
UNION
-- Archivo_especimen_restos_extra
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_especimen_restos_extra.archivo,
Archivo_especimen_restos_extra.archivo_nombre_original,
'Archivo_especimen_restos_extra' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Especimen_restos_extra
ON Conglomerado_muestra.id = Especimen_restos_extra.conglomerado_muestra_id
INNER JOIN Archivo_especimen_restos_extra
ON Especimen_restos_extra.id = Archivo_especimen_restos_extra.especimen_restos_extra_id
UNION
-- Archivo_especie_invasora_extra
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_especie_invasora_extra.archivo,
Archivo_especie_invasora_extra.archivo_nombre_original,
'Archivo_especie_invasora_extra' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Especie_invasora_extra
ON Conglomerado_muestra.id = Especie_invasora_extra.conglomerado_muestra_id
INNER JOIN Archivo_especie_invasora_extra
ON Especie_invasora_extra.id = Archivo_especie_invasora_extra.especie_invasora_extra_id
UNION
-- Archivo_huella_excreta_extra
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_huella_excreta_extra.archivo,
Archivo_huella_excreta_extra.archivo_nombre_original,
'Archivo_huella_excreta_extra' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Huella_excreta_extra
ON Conglomerado_muestra.id = Huella_excreta_extra.conglomerado_muestra_id
INNER JOIN Archivo_huella_excreta_extra
ON Huella_excreta_extra.id = Archivo_huella_excreta_extra.huella_excreta_extra_id
UNION
-- Archivo_conteo_ave
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_conteo_ave.archivo,
Archivo_conteo_ave.archivo_nombre_original,
'Archivo_conteo_ave' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Sitio_muestra
ON Conglomerado_muestra.id = Sitio_muestra.conglomerado_muestra_id
INNER JOIN Punto_conteo_aves
ON Sitio_muestra.id = Punto_conteo_aves.sitio_muestra_id
INNER JOIN Conteo_ave
ON Punto_conteo_aves.id = Conteo_ave.punto_conteo_aves_id
INNER JOIN Archivo_conteo_ave
ON Conteo_ave.id = Archivo_conteo_ave.conteo_ave_id
UNION
-- Archivo_incendio
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_incendio.archivo,
Archivo_incendio.archivo_nombre_original,
'Archivo_incendio' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Incendio
ON Conglomerado_muestra.id = Incendio.conglomerado_muestra_id
INNER JOIN Archivo_incendio
ON Incendio.id = Archivo_incendio.incendio_id
UNION
-- Archivo_plaga
SELECT Conglomerado_muestra.nombre, Conglomerado_muestra.fecha_visita,
Conglomerado_muestra.institucion, Archivo_plaga.archivo,
Archivo_plaga.archivo_nombre_original,
'Archivo_plaga' AS tipo_archivo
FROM Conglomerado_muestra
INNER JOIN Plaga
ON Conglomerado_muestra.id = Plaga.conglomerado_muestra_id
INNER JOIN Archivo_plaga
ON Plaga.id = Archivo_plaga.plaga_id;
