CREATE TABLE cali.total_forecast (
    anio int8 NULL,
    comuna varchar(15) NULL,
    sexo varchar(9) NULL,
    asx int8 NULL,
    hom int8 NULL,
    hur int8 NULL,
    lep int8 NULL,
    ter int8 NULL,
    hur_otros int8 NULL,
    c_asx int8 NULL,
    c_hom int8 NULL,
    c_hur int8 NULL,
    c_lep int8 NULL,
    c_ter int8 NULL
);

CREATE TABLE targeting.dim_barrios (
    "index" int8 NULL,
    id_barrio text NULL,
    barrio text NULL,
    comuna text NULL,
    estra_moda int8 NULL,
    area float8 NULL,
    perimetro float8 NULL,
    zona varchar(50) NULL
);
CREATE INDEX ix_targeting_dim_barrios_index ON targeting.dim_barrios USING btree (index);

CREATE TABLE targeting.dim_comunas (
    comuna varchar(12) NULL,
    genero varchar(12) NULL,
    anio int8 NULL,
    cantidad int8 NULL
);

CREATE TABLE targeting.dim_diccionario (
    cod_etiqueta text NULL,
    des_etiqueta text NULL
);

CREATE TABLE targeting.dim_etiqueta (
    "index" int8 NULL,
    "year" int8 NULL,
    cod_valor text NULL,
    cod_etiqueta_homo text NULL,
    nom_valor text NULL
);
CREATE INDEX ix_targeting_dim_etiqueta_index ON targeting.dim_etiqueta USING btree (index);

CREATE TABLE targeting.fct_act_criminal (
    fechahora timestamp NULL,
    anio varchar(5) NULL,
    dia_semana varchar(12) NULL,
    departamento varchar(56) NULL,
    municipio varchar(27) NULL,
    zona varchar(20) NULL,
    barrio varchar(100) NULL,
    id_barrio varchar(4) NULL,
    comuna varchar(5) NULL,
    clase_sitio varchar(100) NULL,
    tipo_crimen varchar(100) NULL,
    capitulo varchar(100) NULL,
    arma_empleada varchar(100) NULL,
    movil_agresor varchar(100) NULL,
    movil_victima varchar(100) NULL,
    edad int8 NULL,
    sexo varchar(12) NULL,
    estado_civil varchar(100) NULL,
    pais_nacimiento varchar(100) NULL,
    clase_empleado varchar(100) NULL,
    profesion varchar(255) NULL,
    escolaridad varchar(255) NULL,
    clase_empresa varchar(100) NULL,
    clase_vehiculo varchar(100) NULL,
    marca_vehiculo varchar(100) NULL,
    linea_vehiculo varchar(100) NULL,
    modelo_vehiculo varchar(100) NULL,
    cantidad int8 NULL,
    rango_edad varchar(12) NULL
);

CREATE TABLE targeting.fct_capturas (
    fechahora timestamp NULL,
    anio text NULL,
    mes varchar(20) NULL,
    dia_semana varchar(12) NULL,
    departamento varchar(56) NULL,
    municipio varchar(27) NULL,
    zona varchar(20) NULL,
    barrio varchar(40) NULL,
    id_barrio varchar(4) NULL,
    clase_sitio varchar(100) NULL,
    delito varchar(255) NULL,
    edad int8 NULL,
    sexo varchar(12) NULL,
    estado_civil varchar(100) NULL,
    clase_empleado varchar(100) NULL,
    profesion varchar(255) NULL,
    cantidad int8 NULL,
    capitulo varchar(100) NULL,
    comuna varchar(5) NULL,
    rango_edad varchar(20) NULL
);

CREATE TABLE targeting.fct_encuestas (
    level_0 int8 NULL,
    "CC2" text NULL,
    "CS4" text NULL,
    "CV1" text NULL,
    "CS2_CODES" text NULL,
    "GG7" text NULL,
    "AG1" text NULL,
    "LOCALIDAD_COMUNA" text NULL,
    "VS15" text NULL,
    "VS16" text NULL,
    "VS17" text NULL,
    "VS18" text NULL,
    "SEXO" text NULL,
    "GG1" text NULL,
    "MV18_15" text NULL,
    "MV19_8" text NULL,
    "VS0" text NULL,
    "VS8" text NULL,
    "CV4" text NULL,
    "CS2_C_1" int8 NULL,
    "ZONAS" text NULL,
    "year" text NULL,
    "COD_COMUNA" text NULL,
    "CC2_cat" int8 NULL,
    "CS4_cat" int4 NULL,
    "CV1_cat" int8 NULL,
    "CS2_CODES_cat" int4 NULL,
    "GG7_cat" int8 NULL,
    "AG1_cat" text NULL,
    "VS15_cat" int8 NULL,
    "VS16_cat" text NULL,
    "VS17_cat" text NULL,
    "VS18_cat" int8 NULL,
    "SEXO_cat" text NULL,
    "GG1_cat" int4 NULL,
    "MV18_15_cat" int8 NULL,
    "MV19_8_cat" int8 NULL,
    "VS0_cat" int8 NULL,
    "VS8_cat" int8 NULL,
    "CV4_cat" int8 NULL,
    "ZONAS_cat" text NULL,
    escolaridad int8 NULL,
    edad text NULL,
    seguridad_bin int8 NULL,
    seguridad_barrio_bin int8 NULL,
    percepcion_alcalde_bin int8 NULL,
    satisfaccion_ciudad_bin int8 NULL,
    satisfaccion_barrio_bin int8 NULL,
    vs9_label_asaltos_a_casas_o_apartamentos float8 NULL,
    vs9_label_atracos_a_tiendas_o_negocios_del_barrio float8 NULL,
    vs9_label_drogadiccion float8 NULL,
    vs9_label_falta_de_policias float8 NULL,
    vs9_label_fronteras_invisibles float8 NULL,
    vs9_label_indigencia float8 NULL,
    vs9_label_las_pandillas float8 NULL,
    vs9_label_ninguna float8 NULL,
    vs9_label_otro_cual float8 NULL,
    vs9_label_presencia_de_paramilitarismo_y_milicias_guerrilla float8 NULL,
    vs9_label_rinas_peleas float8 NULL,
    vs9_label_se_presentan_casos_de_homicidio float8 NULL,
    vs9_label_se_presentan_casos_de_violaciones float8 NULL,
    vs9_label_se_presentan_muchos_atracos_callejeros float8 NULL,
    vs9_label_se_roban_muchos_carros_o_partes float8 NULL,
    vs9_label_trafico_de_drogas float8 NULL,
    vs9_label_vandalismo_contra_edificaciones_parques_y_otros float8 NULL,
    corrupcion_bin int8 NULL,
    punidad_bin int8 NULL
);

CREATE TABLE targeting.forecast_apprehension (
    periodo varchar(7) NULL,
    anio text NULL,
    mes int8 NULL,
    comuna text NULL,
    tipo_crimen varchar(5) NULL,
    valor int8 NULL
);

CREATE TABLE targeting.forecast_crimes (
    periodo varchar(7) NULL,
    anio text NULL,
    mes int8 NULL,
    comuna text NULL,
    sexo text NULL,
    tipo_crimen varchar(20) NULL,
    valor int8 NULL
);

CREATE TABLE targeting.prediccion (
    anio text NULL,
    comuna text NULL,
    estrato int4 NULL,
    sexo text NULL,
    escolaridad int4 NULL,
    edad text NULL,
    perc_segura float8 NULL,
    perc_insegura float8 NULL,
    perc_segura_barrio float8 NULL,
    perc_insegura_barrio float8 NULL,
    perc_pos_alcalde float8 NULL,
    perc_neg_alcalde float8 NULL,
    vs9_1 numeric NULL,
    vs9_2 numeric NULL,
    vs9_3 numeric NULL,
    vs9_4 numeric NULL,
    vs9_5 numeric NULL,
    vs9_6 numeric NULL,
    vs9_7 numeric NULL,
    vs9_8 numeric NULL,
    vs9_9 numeric NULL,
    vs9_10 numeric NULL,
    vs9_12 numeric NULL,
    vs9_13 numeric NULL,
    vs9_14 numeric NULL,
    vs9_15 numeric NULL,
    vs9_16 numeric NULL,
    vs9_17 numeric NULL,
    vs9_18 numeric NULL,
    hurtos int4 NULL,
    abusos int4 NULL,
    amenazas int4 NULL,
    homicidios int4 NULL,
    lesiones int4 NULL,
    c_hurto int4 NULL,
    c_abuso int4 NULL,
    c_amenaza int4 NULL,
    c_homicidio int4 NULL,
    c_lesiones int4 NULL
);

CREATE TABLE targeting.prediccion_det (
    "index" int8 NULL,
    level_0 int8 NULL,
    "CC2" text NULL,
    "CS4" text NULL,
    "CV1" text NULL,
    "CS2_CODES" text NULL,
    "GG7" text NULL,
    "AG1" text NULL,
    "LOCALIDAD_COMUNA" text NULL,
    "VS15" text NULL,
    "VS16" text NULL,
    "VS17" text NULL,
    "VS18" text NULL,
    "SEXO" text NULL,
    "GG1" text NULL,
    "MV18_15" text NULL,
    "MV19_8" text NULL,
    "VS0" text NULL,
    "VS8" text NULL,
    "CV4" text NULL,
    "CS2_C_1" float8 NULL,
    "ZONAS" text NULL,
    anio text NULL,
    percepcion_concejo int8 NULL,
    "CS4_cat" int8 NULL,
    satisfaccion int8 NULL,
    corrupcion int8 NULL,
    camino text NULL,
    victima_delito int8 NULL,
    tipo_delito text NULL,
    denuncia_delito text NULL,
    punidad float8 NULL,
    "SEXO_cat" text NULL,
    percepcion_alcalde int8 NULL,
    seguridad_buses int8 NULL,
    solidaridad_abusos_fisicos int8 NULL,
    satisfaccion_barrio int8 NULL,
    seguridad_barrio int8 NULL,
    seguridad int8 NULL,
    zona text NULL,
    escolaridad int8 NULL,
    edad text NULL,
    seguridad_bin int8 NULL,
    seguridad_barrio_bin int8 NULL,
    percepcion_alcalde_bin int8 NULL,
    satisfaccion_ciudad_bin int8 NULL,
    satisfaccion_barrio_bin int8 NULL,
    problema_asaltos_residencias float8 NULL,
    problema_atracos_negocios float8 NULL,
    problema_drogadiccion float8 NULL,
    problema_falta_policias float8 NULL,
    problema_fronteras_invisibles float8 NULL,
    problema_indigencia float8 NULL,
    problema_pandillas float8 NULL,
    problema_ninguno float8 NULL,
    problema_otro float8 NULL,
    problema_para_guerrilla float8 NULL,
    problema_riñas float8 NULL,
    problema_homicidios float8 NULL,
    problema_violaciones float8 NULL,
    problema_atracos_calle float8 NULL,
    problema_robo_carros float8 NULL,
    problema_trafico_drogas float8 NULL,
    problema_vandalismo float8 NULL,
    corrupcion_bin int8 NULL,
    punidad_bin int8 NULL,
    hurtos_y int8 NULL,
    abusos_y int8 NULL,
    amenazas_y int8 NULL,
    homicidios_y int8 NULL,
    lesiones_y int8 NULL,
    c_hurto_y int8 NULL,
    c_abuso_y int8 NULL,
    c_amenaza_y int8 NULL,
    c_homicidio_y int8 NULL,
    c_lesiones_y int8 NULL,
    comuna text NULL,
    estrato int8 NULL,
    hurtos_c int8 NULL,
    abusos_c int8 NULL,
    amenazas_c int8 NULL,
    homicidios_c int8 NULL,
    lesiones_c int8 NULL,
    c_hurto_c int8 NULL,
    c_abuso_c int8 NULL,
    c_amenaza_c int8 NULL,
    c_homicidio_c int8 NULL,
    c_lesiones_c int8 NULL
);

CREATE INDEX ix_targeting_prediccion_det_index ON targeting.prediccion_det USING btree (index);
