from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Импорт функции для создания карты
from src.generate_map import create_map

app = FastAPI()

# Хранилище координат
coordinates = []

# Модель координат
class Coordinate(BaseModel):
    id: int
    latitude: float
    longitude: float


@app.get("/", response_class=HTMLResponse)
async def wait():
    # Координаты начальной точки.
    coordinates = [
        {
            'id': 1,
            'latitude': 57.792093,
            'longitude': 28.209667
        }
    ]
    html_map = create_map(coordinates)
    return HTMLResponse(content=html_map)

# @app.get("/", response_class=HTMLResponse)
# async def show_map():
#     # Возвращаем готовую карту
#     coordinates = [
#         {
#             'id': 1,
#             'latitude': 57.792093,
#             'longitude': 28.209667
#         }
#     ]
#     # Формирование html карты
#     # todo: Возможно не нужно ее генерировать каждый раз
#     #  Подумать, как отслеживать события изменения.
#     html_map = create_map(coordinates)
#     return HTMLResponse(content=html_map)
