DROP MATERIALIZED VIEW TARGETING.VW_CRIMES_YEAR;
CREATE      MATERIALIZED VIEW TARGETING.VW_CRIMES_YEAR AS
SELECT      YEAR,
            CRIME_TYPE,
            BOROUGH_ID,
            BOROUGH_NAME,
            BOROUGH_COMMUNE,
            BOROUGH_STRATUM,
            BOROUGH_ZONE,
            SUM(QUANTITY) AS TOTAL
FROM        (
                SELECT      CAST(ACTIVITY.ANIO AS INT) AS YEAR,
                            ACTIVITY.TIPO_CRIMEN AS CRIME_TYPE,
                            ACTIVITY.ID_BARRIO AS BOROUGH_ID,
                            BOROUGH.BARRIO AS BOROUGH_NAME,
                            BOROUGH.COMUNA AS BOROUGH_COMMUNE,
                            CAST(BOROUGH.ESTRA_MODA AS INT) AS BOROUGH_STRATUM,
                            BOROUGH.ZONA AS BOROUGH_ZONE,
                            CAST(ACTIVITY.CANTIDAD AS INT) AS QUANTITY
                FROM        TARGETING.FCT_ACT_CRIMINAL AS ACTIVITY
                            INNER JOIN
                            TARGETING.DIM_BARRIOS AS BOROUGH
                                ON BOROUGH.ID_BARRIO = ACTIVITY.ID_BARRIO
            ) AS SUMMARY
GROUP BY    YEAR,
            CRIME_TYPE,
            BOROUGH_ID,
            BOROUGH_NAME,
            BOROUGH_COMMUNE,
            BOROUGH_STRATUM,
            BOROUGH_ZONE;

DROP MATERIALIZED VIEW TARGETING.VW_CRIMES_YEAR_MONTH;
CREATE      MATERIALIZED VIEW TARGETING.VW_CRIMES_YEAR_MONTH AS
SELECT      YEAR,
            MONTH,
            CRIME_TYPE,
            BOROUGH_ID,
            BOROUGH_NAME,
            BOROUGH_COMMUNE,
            BOROUGH_STRATUM,
            BOROUGH_ZONE,
            SUM(QUANTITY) AS TOTAL
FROM        (
                SELECT      CAST(ACTIVITY.ANIO AS INT) AS YEAR,
                            CAST(EXTRACT(MONTH FROM ACTIVITY.FECHAHORA) AS INT) AS MONTH,
                            ACTIVITY.TIPO_CRIMEN AS CRIME_TYPE,
                            ACTIVITY.ID_BARRIO AS BOROUGH_ID,
                            BOROUGH.BARRIO AS BOROUGH_NAME,
                            BOROUGH.COMUNA AS BOROUGH_COMMUNE,
                            CAST(BOROUGH.ESTRA_MODA AS INT) AS BOROUGH_STRATUM,
                            BOROUGH.ZONA AS BOROUGH_ZONE,
                            CAST(ACTIVITY.CANTIDAD AS INT) AS QUANTITY
                FROM        TARGETING.FCT_ACT_CRIMINAL AS ACTIVITY
                            INNER JOIN
                            TARGETING.DIM_BARRIOS AS BOROUGH
                                ON BOROUGH.ID_BARRIO = ACTIVITY.ID_BARRIO
            ) AS SUMMARY
GROUP BY    YEAR,
            MONTH,
            CRIME_TYPE,
            BOROUGH_ID,
            BOROUGH_NAME,
            BOROUGH_COMMUNE,
            BOROUGH_STRATUM,
            BOROUGH_ZONE;

DROP MATERIALIZED VIEW TARGETING.VW_PERCEPTION_YEAR;
CREATE      MATERIALIZED VIEW TARGETING.VW_PERCEPTION_YEAR AS
SELECT      YEAR,
            COMMUNE,
            COUNT(
                CASE
                    WHEN SECURITY_PERCEPTION = 0 THEN 1
                END
            ) AS INSECURE,
            COUNT(
                CASE
                    WHEN SECURITY_PERCEPTION = 1 THEN 1
                END
            ) AS SECURE,
            COUNT(SECURITY_PERCEPTION) TOTAL
FROM        (
                SELECT      CAST(ANIO AS INT) AS YEAR,
                            COMUNA AS COMMUNE,
                            SEGURIDAD_BIN AS SECURITY_PERCEPTION
                FROM        TARGETING.PREDICCION_DET
            ) AS PERCEPTION
GROUP BY    YEAR,
            COMMUNE;


DROP MATERIALIZED VIEW TARGETING.VW_PERCEPTION_VARIABLES_YEAR;
CREATE      MATERIALIZED VIEW TARGETING.VW_PERCEPTION_VARIABLES_YEAR AS
SELECT      CAST(ANIO AS INT) AS YEAR,
            EDAD AS AGE_RANGE,
            ESCOLARIDAD AS EDUCATION_CODE,
            CASE
                ESCOLARIDAD
                WHEN 1 THEN 'ILLITERATE'
                WHEN 3 THEN 'PRIMARY SCHOOL'
                WHEN 4 THEN 'HIGH SCHOOL'
                WHEN 5 THEN 'TECHNICAL'
                WHEN 6 THEN 'PROFESSIONAL'
                ELSE 'UNDEFINED'
            END AS EDUCATION,
            ESTRATO AS SOCIAL_STRATUM,
            COUNT(
                CASE
                    WHEN SEGURIDAD_BIN = 0 THEN 1
                END
            ) AS INSECURE,
            COUNT(
                CASE
                    WHEN SEGURIDAD_BIN = 1 THEN 1
                END
            ) AS SECURE,
            COUNT(SEGURIDAD_BIN) TOTAL
FROM        TARGETING.PREDICCION_DET
GROUP BY    ANIO,
            EDAD,
            ESCOLARIDAD,
            ESTRATO;

CREATE      OR REPLACE VIEW TARGETING.VW_CRIMES_VICTIM_DATETIME AS
SELECT      DATE_TIME,
            CRIME_TYPE,
            CRIME_CHAPTER,
            BOROUGH_ID,
            BOROUGH_NAME,
            BOROUGH_COMMUNE,
            BOROUGH_STRATUM,
            BOROUGH_ZONE,
            AGE_RANGE,
            SEX,
            EDUCATION,
            QUANTITY
FROM        (
                SELECT      ACTIVITY.FECHAHORA AS DATE_TIME,
                            ACTIVITY.TIPO_CRIMEN AS CRIME_TYPE,
                            ACTIVITY.CAPITULO AS CRIME_CHAPTER,
                            ACTIVITY.ID_BARRIO AS BOROUGH_ID,
                            BOROUGH.BARRIO AS BOROUGH_NAME,
                            BOROUGH.COMUNA AS BOROUGH_COMMUNE,
                            CAST(BOROUGH.ESTRA_MODA AS INT) AS BOROUGH_STRATUM,
                            BOROUGH.ZONA AS BOROUGH_ZONE,
                            RANGO_EDAD AS AGE_RANGE,
                            SEXO AS SEX,
                            ESCOLARIDAD AS EDUCATION,
                            CAST(ACTIVITY.CANTIDAD AS INT) AS QUANTITY
                FROM        TARGETING.FCT_ACT_CRIMINAL AS ACTIVITY
                            INNER JOIN
                            TARGETING.DIM_BARRIOS AS BOROUGH
                                ON BOROUGH.ID_BARRIO = ACTIVITY.ID_BARRIO
            ) AS SUMMARY;


CREATE OR REPLACE VIEW TARGETING.VW_FORECAST_CRIMES AS
SELECT      CAST(ANIO AS INT) AS YEAR,
            MES AS MONTH,
            COMUNA AS COMMUNE,
            CASE
                WHEN (TIPO_CRIMEN = 'HUR' AND SEXO IN ('-', 'NO APLICA')) OR TIPO_CRIMEN = 'HUR_OTROS' THEN 'NO APLICA'
                WHEN TIPO_CRIMEN <> 'HUR_OTROS' AND SEXO IN ('-', 'NO APLICA') THEN 'MASCULINO'
                ELSE SEXO
            END AS SEX,
            CASE
                WHEN TIPO_CRIMEN = 'HUR' AND SEXO IN ('-', 'NO APLICA') THEN 'THEFT (OTHER)'
                WHEN TIPO_CRIMEN = 'HUR' THEN 'THEFT'
                WHEN TIPO_CRIMEN = 'LEP' THEN 'PERSONAL INJURIES'
                WHEN TIPO_CRIMEN = 'HOM' THEN 'HOMICIDES'
                WHEN TIPO_CRIMEN = 'TER' THEN 'THREATS AND TERRORISM'
                WHEN TIPO_CRIMEN = 'ASX' THEN 'ABUSIVE SEXUAL ACTS AND SEXUAL EXPLOITATION'
                WHEN TIPO_CRIMEN = 'HUR_OTROS' THEN 'THEFT (OTHER)'
                ELSE 'OTHERS'
            END AS CRIME_TYPE,
            VALOR AS VALUE
FROM        TARGETING.FORECAST_CRIMES;
