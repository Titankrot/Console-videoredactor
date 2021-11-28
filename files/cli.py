import cmd
from .functions import *

CLOSE = "CLOSE"


class Cli(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = ">>> "
        self.intro = "Добро пожаловать\nДля справки наберите 'help'"
        self.doc_header = "Доступные команды" \
                          + "(для справки по конкретной команде наберите" \
                          + " 'help _команда_')"

    def do_crop(self, arg):
        'обрезает видео: [<videoname> <x> <y> <width> <height> as <newname>]'
        args = parse(arg)
        if len(args) != 7:
            print("Неверный формат")
            return False
        name = args[0]
        try:
            x = int(args[1])
            y = int(args[2])
            width = int(args[3])
            height = int(args[4])
        except ValueError:
            print("Неверный формат")
            return False
        if args[5] != "as":
            print("Неверный формат")
            return False
        new_name = args[6]
        try:
            crop(name, x, y, width, height, new_name)
        except AttributeError:
            print("Неверный формат")
            return False
        except KeyError:
            print("Неверный формат")
            return False

    def do_concat(self, arg):
        'соединяет 2 видео: [<firstname> <secondname> as <outname>]'
        args = parse(arg)
        if len(args) != 4:
            print("Неверный формат")
            return False
        first = args[0]
        second = args[1]
        if args[2] != "as":
            print("Неверный формат")
            return False
        name = args[3]
        try:
            concat(first, second, name)
        except AttributeError:
            print("Неверный формат")
            return False
        except KeyError:
            print("Неверный формат")
            return False

    def do_output(self, arg):
        'создает файл из потока: [<videoname>]'
        args = parse(arg)
        if len(args) != 1:
            print("Неверный формат")
            return False
        name = args[0]
        try:
            output(name)
        except AttributeError:
            print("Неверный формат")
            return False
        except KeyError:
            print("Неверный формат")
            return False

    def do_add(self, arg):
        'добавить видео: [<filename> as <name>]'
        args = parse(arg)
        if len(args) != 3:
            print("Неверный формат")
            return False
        filename = args[0]
        if args[1] != "as":
            print("Неверный формат")
            return False
        name = args[2]
        if os.path.exists(filename):
            add_video(filename, name)
        else:
            print("Нет такого файла. АЛО")
            return False

    def do_exit(self, arg):
        'выход из программы'
        print("Пока")
        return True

    def do_info(self, arg):
        'Получение информации о видеофайле: [<videoname>]'
        args = parse(arg)
        if len(args) != 1:
            print("Неверный формат")
            return False
        videoname = args[0]
        try:
            get_info(videoname)
        except AttributeError:
            print("Неверный формат")
            return False
        except KeyError:
            print("Неверный формат")
            return False

    def do_mult_speed(self, arg):
        'изменение скорости в N раз: [<videoname> mult <N> as <newVideoName>]'
        args = parse(arg)
        if len(args) != 5:
            print("Неверный формат")
            return False
        videoname = args[0]
        if args[1] != 'mult' and args[3] != 'as':
            print('Неверный формат')
            return False
        mult = float(args[2])
        new_name = args[4]
        try:
            change_speed(videoname, mult, new_name)
        except AttributeError:
            print("Неверный формат")
            return False
        except KeyError:
            print("Неверный формат")
            return False

    def do_trim(self, arg):
        '''вырезание фрагмента из видео:
         [<videoname> <start> <end> as <newVideoName]
         start and end: hh:mm:ss'''
        args = parse(arg)
        if len(args) != 5 and args[3] != "as":
            print("Неверный формат")
            return False
        videoname = args[0]
        start = args[1]
        end = args[2]
        new_name = args[4]
        try:
            trim(videoname, start, end, new_name)
        except AttributeError:
            print("Неверный формат")
            return False
        except KeyError:
            print("Неверный формат")
            return False

    def default(self, line):
        print("Несуществующая команда")


def parse(arg):
    return tuple(map(str, arg.split()))
