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
SELECT      ANIO AS YEAR,
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
