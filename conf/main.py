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
app.mount("/templates", StaticFiles(directory="templates"), name="templates")


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
            'latitude': 57.815863,
            'longitude': 28.347319
        }
    ]
    if not os.path.exists("templates/map.html"):
        create_map(coordinates)  # Генерируем карту, если её нет
    with open("templates/map.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/add_coordinates")
async def add_coordinates(coord: Coordinate):
    # Добавляем новую координату
    coordinates.append(coord.dict())
    create_map(coordinates)  # Обновляем карту
    return JSONResponse({"status": "success", "coordinates": coordinates})


@app.get("/get_coordinates")
async def get_coordinates():
    # Возвращаем список всех координат
    return JSONResponse({"coordinates": coordinates})
