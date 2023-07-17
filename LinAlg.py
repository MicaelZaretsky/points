import math
import random

import numpy

# Сделать пару проверок на правильность определения точек на одной линии
def get_triangle_parameters(x1, y1, x2, y2, x3, y3):
    # x1,y1 = 5.,6.7
    # x2,y2 = 5.,1.3
    # x3,y3 = 7.7,4.3

    if ( (y3-y2)*(x2-x1)*(x3-x1) == (y2-y1)*(x3-x2)*(x3-x1) == (y3-y1)*(x3-x2)*(x2-x1)):
        # Три точки лежат на одной прямой => через них нельзя провести окружность
        print("!!! Точки лежат на прямой)")
        print(x1, x2, x3, y1, y2, y3)
        return [0,0,0]
    # Найти x0,y0 координаты центра окружности, а так же R - радиус окружности

    # Уравнения:
    # -2(x1-x2)* x0 + (x1-x2)(x1+x2) = 2(y1-y2)* y0 - (y1-y2)(y1+y2)
    # -2(x2-x3)* x0 + (x2-x3)(x2+x3) = 2(y2-y3)* y0 - (y2-y3)(y2+y3)
    # -2(x1-x3)* x0 + (x1-x3)(x3+x1) = 2(y1-y3)* y0 - (y1-y3)(y1+y3)

    # A1 = 2(x1-x2), B1 = 2(y1-y2), C1 = (x1-x2)(x1+x2) + (y1-y2)(y1+y2)
    # A2 = 2(x2-x3), B2 = 2(y2-y3), C2 = (x2-x3)(x2+x3) + (y2-y3)(y2+y3)
    # A3 = 2(x1-x3), B3 = 2(y1-y3), C3 = (x1-x3)(x1+x3) + (y1-y3)(y1+y3)

    A1 = 2 * (x1 - x2)
    B1 = 2 * (y1 - y2)
    C1 = (x1 - x2) * (x1 + x2) + (y1 - y2) * (y1 + y2)

    A2 = 2 * (x2 - x3)
    B2 = 2 * (y2 - y3)
    C2 = (x2 - x3) * (x2 + x3) + (y2 - y3) * (y2 + y3)

    A3 = 2 * (x1 - x3)
    B3 = 2 * (y1 - y3)
    C3 = (x1 - x3) * (x1 + x3) + (y1 - y3) * (y1 + y3)

    try:
        A = numpy.array([[A1, B1], [A2, B2]])
        B = numpy.array([C1, C2])

        x0, y0 = numpy.linalg.solve(A, B)

        R = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    except numpy.linalg.LinAlgError:
        # A = numpy.array([[A1, B1], [A3, B3]])
        # B = numpy.array([C1, C3])
        #
        # x0, y0 = numpy.linalg.solve(A, B)

        print("ОШБИКА ТУТ: (Точки лежат на прямой)")
        print(x1,x2,x3,y1,y2,y3)

        x0 = y0 = R = 0

    return [x0,y0,R]
