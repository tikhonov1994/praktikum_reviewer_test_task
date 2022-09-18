import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # В целом использование тернарного оператора оправданно
        # для коротких выражений.
        # В данном случае для лучшей читаемости заменить на if-else
        # В качестве значения по умолчанию для date лучше предоставить None
        # Это экономней по памяти и проверка на "is None" более канонична
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Имя Record нарушает PEP8
        # https://peps.python.org/pep-0008/#function-and-variable-names
        # Переменные именуются со строчных букв
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Почему бы не использовать оператор "+="?
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                # Дважды по коду высчитывается разность дат.
                # Лучше создать переменную "дата неделю назад" и проверять,
                # что дата записи внутри периода [неделя назад, сегодня].
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Текст из комментария лучше перенести в docstring
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Вместо использования двух f-строк лучше обернуть возвращаемое
            # значение в скобки и использовать одну f-строку
            # В задании есть требование об округлении значений до сотых
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Лишние скобки
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Pyhthon - язык нестрогой типизации. Указывать тип данных таким образом
    # необязательно - он преобразуется в/из int/float по ходу выполнения.
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Выше указаны курсы валют как константы, а в определении
    # функции они стали значениями по умолчанию для переменных.
    # Нужно либо отказаться от констант и определить значения по умолчанию,
    # либо убрать переменные курсов из определения функции и обращаться к
    # константам как ИмяКласса.ИМЯ_КОНСТАНТЫ
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Хочешь переименовать переменную - сделай это в определении функции.
        # Избегай дублей. Можно переопределять приходящую на вход переменную.
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        # Предлагаю считать все значения currency кроме 'usd' и 'eur' рублями.
        # Таким образом мы в любом случае получим ответ.
        elif currency_type == 'rub':
            # Эта строка не имеет смысла. Ты сравниваешь остаток с единицей.
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # Для выхода по этому условию нам не нужны рассчеты валют.
        # Можно поместить это условие выше и не делать ненужные рассчеты.
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Выше по коду есть проверки на равенство остатка нулю и что
        # остаток больше нуля.
        # Если мы дошли до этой строки, то остаток точно отрицательный.
        # Дополнительная проверка не нужна - можно сразу возвращать ответ.
        elif cash_remained < 0:
            # Перенос строки обратным бэкслешем не рекомендован требованиями
            # к коду студентов. Можно обернуть строку в скобки.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Переопределение родительского метода не имеет смысла,
    # если ничего не меняется.
    # Он и без объявления отнаследуется от класса-родителя.
    def get_week_stats(self):
        super().get_week_stats()
