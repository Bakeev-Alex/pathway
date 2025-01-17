import folium
from folium.plugins import LocateControl

from .route_on_map import get_routes, adding_waypoint

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
    generic_map = folium.Map(location=[57.7920936, 28.209667], zoom_start=14)

    # Текущее местоположение пользователя.
    LocateControl(
        position='topleft',  # Положение кнопки (topleft, topright, bottomleft, bottomright)
        strings={"title": "Показать моё местоположение"},  # Текст при наведении на кнопку
        flyTo=True,  # Плавный переход к текущему местоположению
        keepCurrentZoomLevel=True,  # Сохранить текущий уровень масштаба
    ).add_to(generic_map)

    main_route, secondary_routes = get_routes()

    if main_route:
        folium.PolyLine(main_route, color="red", weight=5, opacity=0.9).add_to(generic_map)
    for secondary_route in secondary_routes:
        folium.PolyLine(
            secondary_route,
            color="blue",  # Второстепенные маршруты синие
            weight=3,  # Толщина линии меньше
            opacity=0.7,  # Прозрачность линии
            tooltip="Второстепенный маршрут"
        ).add_to(generic_map)
    for route_1, is_main in [(main_route, True)] + [(r, False) for r in secondary_routes]:
        if route_1:  # Проверяем, что маршрут не пустой
            start_point = route_1[0]  # Первая точка
            end_point = route_1[-1]  # Последняя точка

            # Начальная точка
            folium.CircleMarker(
                location=start_point,
                radius=6,
                color="green" if is_main else "blue",
                fill=True,
                fill_color="green" if is_main else "blue",
                fill_opacity=1,
                tooltip="Начало главного маршрута" if is_main else "Начало второстепенного маршрута"
            ).add_to(generic_map)

            # Конечная точка
            folium.CircleMarker(
                location=end_point,
                radius=6,
                color="red" if is_main else "blue",
                fill=True,
                fill_color="red" if is_main else "blue",
                fill_opacity=1,
                tooltip="Конец главного маршрута" if is_main else "Конец второстепенного маршрута"
            ).add_to(generic_map)


        # for segment in segments:
        #     folium.PolyLine(segment, color="blue", weight=2.5, opacity=1).add_to(generic_map)
        #     # Добавляем маркеры на начала и концы сегментов
        #     if segment:  # Проверяем, что сегмент не пустой
        #         start_point = segment[0]  # Первая точка
        #         end_point = segment[-1]  # Последняя точка
        #
        #         # Точка для начальной точки
        #         folium.CircleMarker(
        #             location=start_point,
        #             radius=4,  # Размер точки
        #             color="green",  # Цвет границы точки
        #             fill=True,
        #             fill_color="green",  # Цвет заливки
        #             fill_opacity=1,
        #         ).add_to(generic_map)
        #
        #         # Точка для конечной точки
        #         folium.CircleMarker(
        #             location=end_point,
        #             radius=4,
        #             color="green",
        #             fill=True,
        #             fill_color="green",
        #             fill_opacity=1
        #         ).add_to(generic_map)

    waypoints = adding_waypoint()
    for waypoint in waypoints:
        # folium.Marker(
        #     location=[waypoint.latitude, waypoint.longitude],
        #     popup=waypoint.name,
        #     icon=folium.Icon(color='red', icon='info-sign')
        # ).add_to
        if "image" in waypoint:
            # HTML для всплывающего окна с изображением
            popup_html = f"""
                    <div>
                        <h4>{waypoint['name']}</h4>
                        <img src="{waypoint['image']}" alt="{waypoint['name']}" width="200" />
                    </div>
                    """
        else:
            # HTML для всплывающего окна без изображения
            popup_html = f"""
                    <div>
                        <h4>{waypoint['name']}</h4>
                    </div>
                    """

        popup = folium.Popup(popup_html, max_width=300)

        folium.Marker(
            location=[waypoint["latitude"], waypoint["longitude"]],
            popup=popup,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(generic_map)

    # Добавляем линию маршрута
    # folium.PolyLine(
    #     locations=[(point["latitude"], point["longitude"]) for point in route],
    #     color="blue",
    #     weight=5,
    #     opacity=0.7
    # ).add_to(generic_map)

    # https://python-visualization.github.io/folium/latest/user_guide/ui_elements/icons.html -- Сделать разные иконки
    # Добавляем минимальные маркеры с текстом для точек линии
    # for point in route:
    #     folium.CircleMarker(
    #         location=(point["latitude"], point["longitude"]),
    #         radius=5,  # Радиус точки
    #         color="red",
    #         fill=True,
    #         fill_color="red",
    #         fill_opacity=0.8,
    #         tooltip=point["name"],  # Текст при наведении
    #     ).add_to(generic_map)

    # https://python-visualization.github.io/folium/latest/user_guide/raster_layers/wms_tile_layer.html -- Можно добавлять разные слои

    # Добавляем точки, если они есть
    # if coordinates:
    #     for coord in coordinates:
    #         images_html = f'<img src="{image_1}" width="100" height="100" style="margin:5px;"/>'
    #         popup_html = f"""
    #         <div>
    #             <h4>Координаты: {coord['latitude']}, {coord['longitude']}</h4>
    #             {images_html}
    #         </div>
    #         """
    #         popup = folium.Popup(popup_html, max_width=300)
    #
    #         folium.Marker(
    #             location=[coord['latitude'], coord['longitude']],
    #             popup=popup
    #         ).add_to(generic_map)
    #
    #     # Соединяем точки линией
    #     folium.PolyLine(
    #         locations=[[coord['latitude'], coord['longitude']] for coord in coordinates],
    #         color="blue", weight=3, opacity=0.8
    #     ).add_to(generic_map)

    # generic_map.save("templates/map.html")
    return generic_map.get_root().render()
