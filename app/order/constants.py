def format_const(key, constants_list):
    for value in constants_list:
        if key in value:
            return value[1]


# Срочность заказа

URGENCY = [(0, 'срочный'),
           (1, 'стратегический'),
           ]

# цель заказа

AIM = [
    (0, 'электрофизиологические работы'),
    (1, 'молекулярно-биологические работы'),
    (2, 'эксперименты поведением'),
    (3, 'иммуноцитохимические / гистохимические исследования'),
    (4, 'другое, пояснить в комментарии к заказу')
]

# замена

REPLACE = [('0', 'Возможна'),
           ('1', 'Невозможна'),
           ('2', 'Другое')]

REPORT_CHOICE = [('user_id', 'Заказчик'),
                 ('reagent_name', 'Название'),
('reagent_description', 'Описание'),

('package', 'Фасовка'),
('package_unit', 'Единица измерения'),
('reagent_count', 'Количество'),
('vendor_name', 'Производитель'),
('replacement', 'Замена'),
('catalogue_number', 'Артикул'),
('url_reagent', 'Ссылка'),
('urgency', 'Срочность'),
('reagent_aim', 'Цель'),
('reagent_comments', 'Комментарии'),
('item_status', 'Статус'),
('reagent_in_order', 'Номер заказа'),
]

