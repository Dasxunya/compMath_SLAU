import colors as color
from functions import file_function as file_function
from functions import console_function as console_function
from functions import generate_function as generate_function

while True:
    try:
        print(color.PURPLE, 'Выбери режим ввода для решения уравнения методом Гаусса с выбором главного элемента:')
        print(color.PURPLE, '\n',
              '\t', '1 - Считывание из файла')
        print('\t', '2 - Ввод линейной системы вручную')
        print('\t', '3 - Автоматическая генерация матрицы')
        print('\t', '4 - Выход')

        number = int(input('\n\t >'))

        if number == 1:
            print(color.YELLOW, '\n\tВы выбрали ввод данных через файл:')
            file_function(input('\tВведите имя файла:'))
        elif number == 2:
            print(color.YELLOW, '\n\tВы выбрали ввод данных через консоль:')
            console_function()

        elif number == 3:
            print(color.YELLOW, '\n\tВы выбрали автоматическую генерацию матрицы:')
            generate_function()

        elif number == 4:
            print(color.PURPLE, '\nДо встречи :)')
            break

        else:
            print(color.RED, 'Такого пункта не существует... Воспользуйтесь предложенными в меню :)\n')

    except KeyboardInterrupt:
        print(color.RED, '\nПрограмма прервана :(\n')
        exit(1)
    except FileNotFoundError:
        print("Проверьте имя файла\n")
    except:
        print(color.RED, '\nЧто-то пошло не так :(')
