import gpxpy
import folium

# Открываем и читаем GPX файл

# todo: Обернуть все в класс (Singleton), возможно сделать сервисы.


def get_gpx():
    with open('src/source/route_on_map.gpx', 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return gpx


def get_segments():
    ...
#
#     gpx = get_gpx()
#     all_segments = []
#
#     # Перебираем треки и маршруты в файле
#     # todo: некорректно рассчитывает точки
#     #  Потому что все тропы, которые прилегающие, рассчитываются с конца маршрута прямой линией и только,
#     #  когда доходит до основного маршрута, она идет как нужно
#     for track in gpx.tracks:
#         for segment in track.segments:
#             points = [[point.latitude, point.longitude] for point in segment.points]
#             # for point in segment.points:
#             #     points.append([point.latitude, point.longitude])
#                 # map_center = [point.latitude, point.longitude]  # Центр карты по последней точке
#             all_segments.append(points)
#     return all_segments


def get_routes():
    gpx = get_gpx()
    main_route = []
    secondary_routes = []

    for track in gpx.tracks:
        for i, segment in enumerate(track.segments):
            points = [[point.latitude, point.longitude] for point in segment.points]
            if i == 0:  # Первый сегмент — главный маршрут
                main_route = points
            else:  # Остальные сегменты — второстепенные маршруты
                secondary_routes.append(points)

    return main_route, secondary_routes


def adding_waypoint():
    gpx = get_gpx()
    waypoints = []

    points_with_images = {
        "Кемпинг, парковка": 'https://storage.yandexcloud.net/scs-attachments/image/ElementUploadImagesResult/01fa5283d02bd24c753a716196f1ae553206287d.jpeg',
        "Магазин Магнит": 'https://storage.yandexcloud.net/scs-attachments/image/ElementUploadImagesResult/50d9fd403c1d6ca724a6d91bb6daa326b18e9b43.jpeg'
    }

    for waypoint in gpx.waypoints:
        # FixMe: Почему-то выводятся некоторые названия как None
        waypoint_data = {
            "latitude": waypoint.latitude,
            "longitude": waypoint.longitude,
            "name": waypoint.name,
        }
        if waypoint.name in points_with_images:
            waypoint_data["image"] = points_with_images[waypoint.name]
        waypoints.append(waypoint_data)

    return waypoints

    # gpx = get_gpx()
    #
    # # Устанавливаем центр карты (например, по первой точке)
    # first_point = gpx.tracks[0].segments[0].points[0]
    # map_center = [first_point.latitude, first_point.longitude]
    #
    # # Создаём карту Folium
    # gpx_map = folium.Map(location=map_center, zoom_start=13)
    #
    # # Получаем все сегменты и добавляем их как отдельные линии
    # segments = get_segments()
    # for segment in segments:
    #     folium.PolyLine(segment, color='blue', weight=2.5).add_to(gpx_map)

    # return gpx_map
