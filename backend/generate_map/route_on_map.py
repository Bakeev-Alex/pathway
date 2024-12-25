import gpxpy
import folium

# Открываем и читаем GPX файл

# todo: Обернуть все в класс (Singleton), возможно сделать сервисы.


def get_gpx():
    gpx_file = open('source/route_on_map.gpx', 'r')  # Замените на путь к вашему GPX-файлу
    gpx = gpxpy.parse(gpx_file)

    return gpx


def get_points():

    gpx = get_gpx()
    # Создаем карту Folium
    points = []  # Для маршрута

    # Перебираем треки и маршруты в файле
    # todo: некорректно рассчитывает точки
    #  Потому что все тропы, которые прилегающие, рассчитываются с конца маршрута прямой линией и только,
    #  когда доходит до основного маршрута, она идет как нужно
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append([point.latitude, point.longitude])
                # map_center = [point.latitude, point.longitude]  # Центр карты по последней точке

    return points


def adding_waypoint():
    gpx = get_gpx()
    waypoints = []

    for waypoint in gpx.waypoints:
        waypoints.append(waypoint)

    return waypoints
