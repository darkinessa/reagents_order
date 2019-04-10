#статус заказа
DRAFT = 0
NEW_ORDER = 1
HANDLING = 2
PASSED = 3
WAITING = 4
RECEIVED = 5
CANCELED = 6
SUSPENDED = 7

STATUS = {
    DRAFT: 'Черновик',
    NEW_ORDER: 'Новый заказ',
    HANDLING:'В обработке',
    PASSED: 'Передан поставщику',
    WAITING: 'Ожидается поставка',
    RECEIVED: 'Пришла поставка',
    CANCELED: 'Заказ отклонен',
    SUSPENDED: 'Заказ отложен'
}

#Срочность заказа
IMMEDIATE = 0
PLANNED = 1

URGENCY = [('IMM', 'Срочный'), ('PL', 'Стратегический')]

#цель заказа

ELPHYS = 0
MOLBIO = 1
BEHAVIOR = 2
IMMUNRES = 3
OTHER = 4

AIM = [
    ('ELP', 'для электрофизиологических работ'),
    ('MOBIO', 'для молекулярно-биологических работ'),
    ('BIH', 'для экспериментов с поведением'),
    ('IMRES', 'для иммуноцитохимических / иммуногистохимических исследований'),
    ('OTHER', 'Cвой вариант, пояснить в комментарии к заказу')
]
