from sqlalchemy.orm import Session

from app import models


def get_percent_occupation(db: Session) -> float:
    """
    Obtiene el porcentaje de las camas ocupadas en el hospital.

    Args:
        db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

    Returns:
        float: Porcentaje de ocupación hospitalaria.
    """
    n_beds: int = db.query(models.Beds).count()
    n_occupied: int = db.query(models.BedsUsed).count()

    return n_occupied / n_beds


def get_avg_stay(db: Session) -> float:
    """
    Obtiene el promedio de las estancias de los pacientes hospitalizados en el hospital.

    Args:
        db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

    Returns:
        float: Promedio de estancia de los pacientes en el hospital.
    """
    hospitalizations: list[models.Hospitalizations] = (
        db.query(models.Hospitalizations).
        filter(
            models.Hospitalizations.last_day.is_not(None)
        )
        .all()
    )

    n: int = len(hospitalizations)
    if n == 0:
        return 0.0
    
    days_sum: int = sum(
        [
            (hospitalization.last_day - hospitalization.entry_day).days 
            for hospitalization in hospitalizations 
        ]
    )

    return days_sum / n


def get_avg_admission(db: Session) -> float:
    """
    Obtiene el promedio de las admisiones de los pacientes hospitalizados en el hospital por día.

    Args:
        db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

    Returns:
        float: Promedio de admisiones de los pacientes en el hospital.
    """
    query = db.query(models.Hospitalizations.entry_day)
    admissions: list[int] = []
    for day in query.distinct().all():
        admissions.append(
            query.filter(models.Hospitalizations.entry_day == day[0]).count()
        )

    return sum(admissions) / len(admissions)


def get_avg_discharge(db: Session) -> float:
    """
    Obtiene el promedio de altas a los pacientes hospitalizados en el hospital por día.

    Args:
        db (sqlalchemy.orm.Session): Sesión de la base de datos para hacer las consultas a la base de datos en Postgresql.

    Returns:
        float: Promedio de dadas de altas a los pacientes en el hospital por día.
    """
    query = db.query(models.Hospitalizations.last_day)
    discharges: list[int] = []
    for day in query.filter(models.Hospitalizations.last_day.is_not(None)).distinct().all():
        discharges.append(
            query.filter(models.Hospitalizations.last_day == day[0]).count()
        )

    return sum(discharges) / len(discharges)
