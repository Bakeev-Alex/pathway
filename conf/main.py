from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

# Импорт функции для создания карты
from generate_map import create_map

app = FastAPI()

# Хранилище координат
coordinates = []

# Подключение статических файлов (карта HTML)
# app.mount("/templates", StaticFiles(directory="templates"), name="templates")


# Модель координат
class Coordinate(BaseModel):
    id: int
    latitude: float
    longitude: float


@app.get("/", response_class=HTMLResponse)
async def show_map():
    # Возвращаем готовую карту
    coordinates = [
        {
            'id': 1,
            'latitude': 57.792093,
            'longitude': 28.209667
        }
    ]
    # Формирование html карты
    # todo: Возможно не нужно ее генерировать каждый раз
    #  Подумать, как отслеживать события изменения.
    html_map = create_map(coordinates)
    return HTMLResponse(content=html_map)
