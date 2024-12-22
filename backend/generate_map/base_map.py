import folium
from folium.plugins import LocateControl

image_1 = 'https://storage.yandexcloud.net/scs-attachments/image/ElementUploadImagesResult/50d9fd403c1d6ca724a6d91bb6daa326b18e9b43.jpeg'
image_2 = 'https://storage.yandexcloud.net/scs-attachments/image/ElementUploadImagesResult/01fa5283d02bd24c753a716196f1ae553206287d.jpeg'

route = [
    {"latitude": 57.815794, "longitude": 28.34139, "name": "Точка 1"},
    {"latitude": 57.81803, "longitude": 28.343554, "name": "Точка 2"},
    {"latitude": 57.818537, "longitude": 28.349829, "name": "Точка 3"},
]


def create_map(coordinates=None):
    # Начальная точка на карте, с какой будет начинаться
    #  ее можно сделать на начало маршрута.
    m = folium.Map(location=[57.8136, 28.3496], zoom_start=14)

    # Текущее местоположение пользователя.
    LocateControl(
        position='topleft',  # Положение кнопки (topleft, topright, bottomleft, bottomright)
        strings={"title": "Показать моё местоположение"},  # Текст при наведении на кнопку
        flyTo=True,  # Плавный переход к текущему местоположению
        keepCurrentZoomLevel=True,  # Сохранить текущий уровень масштаба
    ).add_to(m)

    # Добавляем линию маршрута
    folium.PolyLine(
        locations=[(point["latitude"], point["longitude"]) for point in route],
        color="blue",
        weight=5,
        opacity=0.7
    ).add_to(m)

    # Добавляем минимальные маркеры с текстом для точек линии
    for point in route:
        folium.CircleMarker(
            location=(point["latitude"], point["longitude"]),
            radius=5,  # Радиус точки
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.8,
            tooltip=point["name"],  # Текст при наведении
        ).add_to(m)

    # Добавляем точки, если они есть
    if coordinates:
        for coord in coordinates:
            images_html = f'<img src="{image_1}" width="100" height="100" style="margin:5px;"/>'
            popup_html = f"""
            <div>
                <h4>Координаты: {coord['latitude']}, {coord['longitude']}</h4>
                {images_html}
            </div>
            """
            popup = folium.Popup(popup_html, max_width=300)

            folium.Marker(
                location=[coord['latitude'], coord['longitude']],
                popup=popup
            ).add_to(m)

        # Соединяем точки линией
        folium.PolyLine(
            locations=[[coord['latitude'], coord['longitude']] for coord in coordinates],
            color="blue", weight=3, opacity=0.8
        ).add_to(m)

    # Сохраняем карту в файл
    m.save("templates/map.html")
