'''
Синтаксический анализатор
'''
import time

class Sintax(object):
    symbol = ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x',
              'c', 'v', 'b', 'n', 'm')
    digit = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    sign_arifmetic = ('+', '-', '*', '/')
    parentheses = ('(', ')')
    operator = ('=')
    space = (' ')

    def __init__(self, text_file):
        self.strings = text_file
        self.run()

    def _bloks(self):
        '''
        Определяет тип символа
        :return: Список блоков всех символов
        '''
        bloks = []
        for char in self.strings:
            if char in self.symbol:
                bloks.append({'type': 'char',
                             'value': char,
                              'index': time.time()})
            elif char in self.space:
                bloks.append({'type': 'space',
                             'value': char,
                              'index': time.time()})
            elif char in self.digit:
                bloks.append({'type': 'digit',
                             'value': char,
                              'index': time.time()})
            elif char in self.sign_arifmetic:
                bloks.append({'type': 'sign',
                             'value': char,
                              'index': time.time()})
            elif char in self.parentheses:
                bloks.append({'type': 'parentheses',
                             'value': char,
                              'index': time.time()})
            elif char in self.operator:
                bloks.append({'type': 'operator',
                             'value': char,
                              'index': time.time()})
        return bloks


    def _twins(self, bloks):
        '''
        Находит список всех однотипных и идущих подрят символов, наапример слова или цифры 2 разряда
        :param bloks:
        :return: Список с подсписками индексов всех символов
        '''
        map_index = []
        blok_index = []
        j = 0
        for index in range(len(bloks)):
            if (bloks[index]['type'] is 'char') or (bloks[index]['type'] is 'digit'):
                blok_index.append(index)
            elif len(blok_index) != 0:
                map_index.append(blok_index)
                map_index.append(index)
                blok_index = []
            else:
                map_index.append(index)
        if len(blok_index) != 0:
            map_index.append(blok_index)

        return map_index


    def _mod_bloks(self, bloks, map_index):
        '''
        Создает новый блок соединяя все символы и цифры идущие подряд в один блок
        :param bloks:
        :param map_index:
        :return:
        '''
        bloks_new = []
        for index in map_index:
            if type(index) is list:
                obj = {'type': 'char',
                       'value': '',
                       'index': time.time()}
                for j in index:
                    obj['value'] += bloks[j]['value']
                bloks_new.append(obj)
            else:
                bloks_new.append(bloks[index])

        return bloks_new


    def _avtomate(self, bloks):
        '''
        Конечный автомат, проводит синтаксический анализ
        :param bloks:
        :return:
        '''
        state = 0
        for index in range(len(bloks)):
            if state is 0:
                if (bloks[index]['type'] is 'char') or (bloks[index]['type'] is 'digit'):
                    state = 1
                elif (bloks[index]['type'] is 'sign') or (bloks[index]['type'] is 'parentheses'):
                    pass
                else:
                    raise Exception('Оператор не начинается с переменной')
            elif state is 1:
                if bloks[index]['type'] is 'space':
                    state = 2
                elif bloks[index]['type'] is 'parentheses':
                    pass
                else:
                    raise Exception('Пробел обязятелен')
            elif state is 2:
                if bloks[index]['type'] is 'sign':
                    state = 3
                else:
                    raise Exception("Где потерял знак?")
            elif state is 3:
                if bloks[index]['type'] is 'space':
                    state = 0
                else:
                    raise Exception('Пробел обязятелен')

    def run(self):

        bloks = self._bloks()
        map_index = self._twins(bloks)
        bloks_new = self._mod_bloks(bloks, map_index)
        self._avtomate(bloks_new)



