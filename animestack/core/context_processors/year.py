from datetime import datetime as dt


def year(request):
    """
    Добавляет переменную с текущим годом.
    """
    year_now = dt.now()
    return {"year": year_now.year}
