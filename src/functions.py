import random
import colors as color
from math import fabs
import re
import datetime

# Функция, если нужно будет округлить
def toFixed(num):
    return f'{num:.3f}'


def file_function(filename):
    try:
        n = -1
        array = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if (line != '\n') and (line != ' ') and (line != ' \n'):
                    n += 1
            if n > 20:
                print(color.RED,
                      'В файле превышено количество уравнений! Уменьшите до 20 или менее и попробуйте снова.\n')
                return
        file.close()

        with open(filename, 'r', encoding='utf-8') as file:
            file.readline()
            for row in file:
                line = list(row.split())
                for i in line:
                    #не пропускает числа -7 отрицательные без точки, можно было исправить регуляркой
                    if (re.search('(\d{1,}\.{1}\d{1,})', i) is None) and (not i.isnumeric()):
                        print(color.RED,
                              'Проверьте формат введенных данных (вещественные числа должны быть разделены точкой).')
                        return
                array.append(list(line))
            file.close()
            compute = Calculator(n, optimize(n, array))
            compute.calculate()
            del compute
    except FileNotFoundError:
        print(color.RED, 'Файл не найден. Проверьте введенное имя.\n')


# Для консольного ввода
def console_function():
    try:
        n = int(input("\tВведите количество строк в уравнении (число не должно превышать 20):\n\t>"))
        if (n <= 20) and (n > 1):
            array = []
            print(color.YELLOW, "Введите строки в следующем формате:")
            print(color.YELLOW, "\tai1, ai2, ai3, ... ain bi")
            for i in range(n):
                while True:
                    line = list((input(str(i + 1) + ': ').split()))
                    if int(len(line) != n + 1):
                        print(color.RED,
                              "Кол-во строк не совпадает с количеством столбцов. \nПроверьте правильность ввода и "
                              "попробуйте снова")
                    else:
                        array.append(line)
                        break
            compute = Calculator(n, optimize(n, array))
            compute.calculate()
            del compute
        else:
            print(color.RED, "Проверьте правильность ввода!")
            return
    except ValueError:
        print(color.RED, "Неверные аргументы ввода!")


# TODO: Функция генерирующая значения для матрицы
def generate_function():
    try:
        array = []
        n = int(input("\tВведите количество строк в уравнении (число не должно превышать 20):\n\t>"))
        if (n <= 20) and (n > 1):
            print(color.YELLOW, "Генерирую матрицу...")
            for i in range(n):
                line = [random.randint(-20, 20) + random.uniform(-1, 1) for _ in range(n + 1)]
                array.append(line)
            compute = Calculator(n, optimize(n, array))
            compute.calculate()
            del compute
        else:
            print(color.YELLOW, "Проверьте правильность ввода и попробуйте снова")
    except ValueError:
        print(color.RED, "Неверные аргументы ввода!")


# привести матрицы в удобный для рассчетов вид дробных чисел()
def optimize(n, arr):
    i = 0
    while i < n:
        j = 0
        while j <= n:
            arr[i][j] = float(arr[i][j])
            j += 1
        i += 1
    return arr


class Calculator:
    n = 0  # количество уравнений/неизвестных
    coeff = []  # система уравнений
    vector = []  # вектор неизвестных
    det = 0  # определитель матрицы
    swap_counter = 0  # количество перестановок

    def __init__(self, n, coeff):
        self.n = n
        self.coeff = coeff
        self.det = []
        self.swap_counter = 0

    def calculate(self):
        try:
            print(color.YELLOW, "\t\nПолученная система:\n")
            self.print_coeff()

            start = datetime.datetime.now()
            self.make_triangle()
            print('\n', color.YELLOW, 'Матрица треугольного вида:\n')
            self.print_coeff()

            # Определитель
            self.get_det()

            timedelta = datetime.datetime.now() - start
            print(color.YELLOW, "Время работы метода: " + str(timedelta) + "\n")

            print('\n', color.YELLOW, 'Столбец неизвестных:')
            self.comp_vector_x()
            self.print_vector_x()

            print('\n', color.YELLOW, 'Столбец невязок:')
            self.print_residuals()

        except ZeroDivisionError:
            return

        except ArithmeticError:
            return

    # Вывод системы на экран
    def print_coeff(self):
        i = 0
        while i < self.n:
            j = 0
            while j < self.n:
                print(" ", toFixed(self.coeff[i][j]), '\t', end='')
                j += 1
            print(toFixed(self.coeff[i][-1]), "b[" + str(i + 1) + "]")
            i += 1

    # поиск наибольшего главного элемента и перестановка строк
    def search_main(self, counter):
        i = counter
        j = counter
        max_el = 0
        while i < self.n:
            if fabs(self.coeff[i][j]) > fabs(max_el):
                max_el = self.coeff[i][j]
                temp = self.coeff[j]
                self.coeff[j] = self.coeff[i]
                self.coeff[i] = temp
                self.swap_counter += 1
            i += 1
        if max_el != 0:
            return max_el
        if max_el == 0:
            print("\nНет решений:(")
            return ArithmeticError

    # Приведение к треугольному виду
    def make_triangle(self):
        try:
            counter = 0
            while counter < self.n:
                self.search_main(counter)
                m = counter
                while m < self.n - 1:
                    a = -(self.coeff[m + 1][counter] / self.coeff[counter][counter])
                    j = counter
                    while j < self.n:
                        self.coeff[m + 1][j] += a * self.coeff[counter][j]
                        j += 1
                    self.coeff[m + 1][-1] += a * self.coeff[counter][-1]
                    m += 1
                k = 0
                line_sum = 0
                while k < self.n:
                    line_sum += self.coeff[counter][k]
                    k += 1
                if line_sum == 0:
                    print(color.RED, 'Данная система не совместима, решений нет!')
                    return ArithmeticError
                counter += 1
        except ValueError:
            print(color.RED, "Некорректная работа с данными")
            return

    # Определитель
    def get_det(self):
        i = 0
        self.det = 1
        while i < self.n:
            self.det *= self.coeff[i][i]
            i += 1
        if self.swap_counter % 2 == 1:
            self.det *= -1
        print('\n', color.YELLOW, 'Определитель', ' = ', self.det, '\n')
        if self.det == 0:
            print(color.RED, 'Нет решения, т.к. система вырожденная')
            return ArithmeticError

    # Подсчет искомых х
    def comp_vector_x(self):
        i = self.n - 2
        self.vector.append(self.coeff[self.n - 1][-1] / self.coeff[self.n - 1][self.n - 1])
        while i > -1:
            k = self.n - 1
            val = self.coeff[i][-1]
            while k > i:
                val = val - self.vector[self.n - 1 - k] * self.coeff[i][k]
                k -= 1
            self.vector.append(val / self.coeff[i][i])
            i -= 1

    def print_vector_x(self):
        i = 0
        print(color.YELLOW, 'Решение системы:')
        self.vector.reverse()
        while i < self.n:
            print('\t', 'x[' + str(i + 1) + ']:', self.vector[i])
            i += 1
        print('')

    # Подсчет невязки r1 ... rn
    def print_residuals(self):
        i = 0
        print(color.YELLOW, 'Невязки:')
        while i < self.n:
            res = 0
            j = 0
            while j < self.n:
                res = res + self.coeff[i][j] * self.vector[j]
                j += 1
            res = res - self.coeff[i][-1]
            i += 1
            print('\t', 'Невязка', i, 'строки:', fabs(res))
        print('')
