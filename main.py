import math
import re
import matplotlib.pyplot as plt
import numpy as np

import LinAlg


class Point:
    def __init__(self, *args):
        self.cord = args

    # def __str__(self):
    #     return self.cord.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.cord == other.get_cords():
                return True
            else:
                return False
        else:
            raise TypeError

    def distance(self, point_b):
        # Функция высчитывает расстояние между двумя точками
        if isinstance(point_b, self.__class__):
            cords_b = point_b.get_cords()
            if len(self.cord) == len(cords_b):
                S = 0
                for i in range(len(self.cord)):
                    S += (self.cord[i] - cords_b[i]) ** 2
                d = math.sqrt(S)
                return d
            else:
                raise ValueError
        else:
            raise ValueError

    def get_cords(self):
        return self.cord


class Line:
    def __init__(self, point_a, point_b):
        # Должны быть переданы две точки
        if (point_a == point_b) or not (isinstance(point_a, Point.__class__) and isinstance(point_b, Point.__class__)):
            raise ValueError
        else:
            cord1, cord2 = point_a.get_cords(), point_b.get_cords()
            if cord1[0] == cord2[0]:
                # Точки лежат на вертикальной прямой
                self.k = 'special'
                self.b = cord1[0]
            else:
                self.k = (cord1[1] - cord2[1]) / (cord1[0] - cord2[0])
                self.b = cord1[1] - self.k * cord1[0]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.get_parameters() == other.get_parameters():
                return True
            else:
                return False
        else:
            raise TypeError

    def get_parameters(self):
        return [self.k, self.b]

    def isPointOnTheLine(self, o):
        if isinstance(o, Point.__class__):
            cord = o.get_cords()
            if self.k == 'special':  # Вертикальная линия
                if self.b == cord[0]:
                    return True
                else:
                    return False
            elif self.k * cord[0] + self.b == cord[1]:
                return True
            else:
                return False
        else:
            raise ValueError

    def get_normal(self, o):
        # Возвращает перпендикуляр из точки на прямую
        pass


class Circle:
    def __init__(self, center, radius):
        # center = [x,y]
        self.center = center
        self.radius = radius

    def isPointOnTheCircle(self, cord):
        # cord = пара чисел [x,y]
        if ((cord[0] - self.center[0]) ** 2 + (cord[1] - self.center[1]) ** 2) == (self.radius) ** 2:
            return True
        else:
            return False

    def get_radius(self):
        return self.radius

    def get_center(self):
        return self.center

    def get_cords(self, accurancy=1 / 10 ** 6):
        accurancy = self.radius / 10 ** 6

    def __eq__(self, other):  # Сравнение окружностей
        if isinstance(other, self.__class__):
            if (self.radius == other.get_radius()) and (self.center == other.get_center()):
                return True
            else:
                return False
        else:
            raise TypeError


# A = Circle([0, 0], radius=10)
# o = Point(12, 42)
# b = Point(12, 43)
# print(o.distance(b))
# exit()


def draw_points(points, color=''):
    # points ~ list of [x,y]
    for i in range(len(points)):
        plt.plot([points[i][0]], [points[i][1]], color + '-o')


def get_input():
    # Получет все необходимые данные

    # ScaleSize = int(input("Введите масштаб: "))
    ScaleSize = 22
    NumberOfPoints = int(input("Введите колличество точек: "))
    # NumberOfPoints = 8
    FileName = input("Введите название файла: ")
    # FileName = 'dots2.txt'

    with open(FileName) as file:
        _str = file.read()
        points = __filter_coord_data(_str)

        if NumberOfPoints > len(points):
            print(f"Ошибка в файле не достаточно точек, их колличество: {len(points)}")

        print(f'Точки: {points}')
    return {'ScaleSize': ScaleSize, 'points': points}


def __filter_coord_data(str):
    str = re.sub(r'[^-.0123456789,; \n]', r'', str)  # Удалить все кроме символов и их разделителей
    S = re.split(" |\n", str)  # Разделить по парам чисел
    S = list(filter(None, S))  # Удалить пустые
    # S ~ [['32,44'],['444,333],...]

    S = [re.split(",|;", S[i]) for i in
         range(len(S))]  # Разделение на пары чисел в формате строк ~ [ ['32','444'], ...]

    for i in range(len(S)):
        if len(S[len(S) - 1 - i]) != 2:
            S.pop(len(S) - 1 - i)
        else:
            if '' in S[len(S) - 1 - i]:
                S.pop(len(S) - 1 - i)
            else:
                S[len(S) - 1 - i] = [float(S[len(S) - 1 - i][0]), float(S[len(S) - 1 - i][1])]
    # S ~ [[32,3232], [4343,322], [322,1], ...]
    return S


def main():
    # Основная функция программы
    inputS = get_input()
    ScaleSize = inputS['ScaleSize']
    points = inputS['points']

    x = []
    y = []
    for i in range(len(points)):
        x.append(points[i][0])
        y.append(points[i][1])

    draw_points(points)
    draw_right_circle(x, y)

    plt.show()


# def draw_square(x, y):
#     # Функция рисует один квадрат по 4 точкам
#     x_ = [x[i] for i in range(4)]
#     y_ = [y[i] for i in range(4)]
#     x_.append(y_[0])
#     y_.append(x_[0])
#     # Прорисовка
#     plt.plot(x_, y_, '-o')
#

def get_all_triangles(x, y):
    # Функция получает все тройки точек из списка
    Triangles = []
    if len(x) != len(y):
        print("Ошибка! Число x не равное числу y")
        return
    for i in range(len(x) - 2):
        for j in range(i + 1, len(x) - 1):
            for k in range(j + 1, len(x)):
                # Три точки по ним строить окружности
                A = [x[i], y[i]]
                B = [x[j], y[j]]
                C = [x[k], y[k]]
                Triangles.append([A, B, C])
    return Triangles


def draw_right_circle(x, y):
    # Функция рисует окружность,содержащую максимальное колличество точек из списка
    Triangles = get_all_triangles(x, y)  # Получение всех троек чисел
    Objects = []  # Сюда записываем все типы окружностей (их радиусы, центры)
    for i in range(len(Triangles)):
        data = get_circle(Triangles[i])
        Objects.append(data)
    Objects.sort()
    # print('\n\n\n\n', Objects)

    # Поиск окружности, которая встречается максимальное колличество раз
    Max = [1, 1]
    for i in range(len(Objects) - 1):
        Count = 1
        n = None
        if Objects[i] == Objects[i + 1]:
            Count += 1
            n = i
            for j in range(i + 2, len(Objects)):
                if Objects[i] == Objects[j]:
                    Count += 1
                else:
                    break
            if Count > Max[0]:
                Max[0] = Count
                Max[1] = n
    # print(Max)

    # Count = 0
    x0, y0, R = Objects[Max[1]]  # Окружность, содержащая максимальное число точек
    p = get_points_on_the_circle([x0, y0, R], points=[x, y])  # Поиск тех точек, что лежат на окружности
    draw_circle(x0, y0, R)  # Рисует нашу окружность
    draw_points(p, color='k')  # Помечает точки, лежащие на окружности

    print("\n\n\n")
    print(f"Итого было построено на окружности {len(p)} точк.: {p}")
    l = get_max_distance(p)  # Получает две точки с максимальным между ними расстоянием
    # print(l[0],str(l[1]),str(l[2]))
    draw_by_points([l[1], l[2]])  # Рисуем линию между двумя этими точками

    center = Point(x0, y0)
    A = get_normal_point(l[1], l[2], center)  # Получаем точку основания перпендикуляра, опущенного из центра окружности
    draw_by_points([center, A])


def get_normal_point(point_a, point_b, point_c):
    # point_a,point_b - точки отрезка
    # point_c - точка центра окружности
    if isinstance(point_a.__class__, Point.__class__) and isinstance(point_b.__class__, Point.__class__) and isinstance(
            point_c.__class__, Point.__class__):
        cord1, cord2, cord3 = point_a.get_cords(), point_b.get_cords(), point_c.get_cords()
        x1, y1 = cord1
        x2, y2 = cord2
        x3, y3 = cord3
        x = (x1 * x1 * x3 - 2 * x1 * x2 * x3 + x2 * x2 * x3 + x2 *
             (y1 - y2) * (y1 - y3) - x1 * (y1 - y2) * (y2 - y3)) / ((x1 - x2) *
                                                                    (x1 - x2) + (y1 - y2) * (y1 - y2))
        y = (x2 * x2 * y1 + x1 * x1 * y2 + x2 * x3 * (y2 - y1) - x1 *
             (x3 * (y2 - y1) + x2 * (y1 + y2)) + (y1 - y2) * (y1 - y2) * y3) / ((
                                                                                        x1 - x2) * (x1 - x2) + (
                                                                                        y1 - y2) * (
                                                                                        y1 - y2))
        return Point(x, y)
    else:
        raise ValueError


def draw_by_points(points):
    # points Формата класса Point
    x = []
    y = []
    for i in range(len(points)):
        # print(points[i].__class__)
        if isinstance(points[i].__class__, Point.__class__):
            cord = points[i].get_cords()
            x.append(cord[0])
            y.append(cord[1])
        else:
            raise ValueError
    plt.plot(x, y, 'b-')


def get_points_on_the_circle(data, points):
    # Возвращает все точки из списка, лежащие на окружности
    # data ~ [x0, y0, radius]
    # points ~ [[x1,x2,x3,..],[y1,y2,y3,...]]
    x0, y0, R = data
    circle = Circle([x0, y0], radius=R)
    p = []
    for i in range(len(points[0])):
        X = points[0][i]
        Y = points[1][i]
        if circle.isPointOnTheCircle([X, Y]):
            # print(f"{count}. Точка {X};{Y} лежит на нашей окружности {x0, y0, R}")
            # plt.plot([X], [Y], 'k-o')
            p.append([X, Y])
    return p


def get_max_distance(points):
    # Находит 2 точки, с максимальным между ними расстоянием
    # points ~ [[x1,x2,x3,..][y1,y2,y3,..]]
    p = []
    Max = [0, None, None]

    for i in range(len(points)):
        p.append(Point(points[i][0], points[i][1]))
    for i in range(len(p) - 1):
        for j in range(i, len(p)):
            d = p[i].distance(p[j])
            if d > Max[0]:
                Max[0] = d
                Max[1] = p[i]
                Max[2] = p[j]
    return Max


def mark_points(points):
    pass


def draw_circle(x0, y0, R):
    # Функция рисует окружность по центру и радиусу
    if R > 0:
        # Рисуем круг
        x_ = np.arange(x0 - R, x0 + R, R / (10 ** 6))
        y_ = np.array([math.sqrt(abs(R ** 2 - (X - x0) ** 2)) + y0 for X in x_])
        y__ = np.array([-math.sqrt(abs(R ** 2 - (X - x0) ** 2)) + y0 for X in x_])
        print([x_])
        print(y_)
        plt.plot(x_, y_, 'r', x_, y__, 'r', [x_[-1], x_[-1]], [y_[-1], y__[-1]], 'r')
    else:
        print("Неверный радиус")
        raise ValueError


def get_circle(points):
    # Функция получает окружность по тройке точек
    x_ = [points[i][0] for i in range(3)]  # Получаем отдельно Иксы и отдельно Игрики
    y_ = [points[i][1] for i in range(3)]

    # Решаем систему линейных уравнений и находим центр с радиусом
    x0, y0, R = LinAlg.get_triangle_parameters(x_[0], y_[0], x_[1], y_[1], x_[2], y_[2])

    if R != 0:
        print(f"Построена окружность - x0={x0},y0={y0},R={R}")
    else:
        print("нулевой радиус")

    return [x0, y0, R]


main()
# get_input()
