import sqlite3
import telebot
import random

TOKEN = '6634758184:AAER6CGOuhUuQk1tdtsKimLxc8YUh_BZMYg'
bot = telebot.TeleBot(TOKEN)

# Создаем базу данных и подключаемся к ней
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

def create_connection():
    return sqlite3.connect('recipes.db')

# Создаем таблицу recipes
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dish_name TEXT,
        ingredients TEXT,
        instructions TEXT
    )
''')
conn.commit()

# Пример рецептов
recipes_data = [
    {
        'dish_name': 'Паста карбонара',
        'ingredients': 'Спагетти, бекон, яйца, сыр пармезан, чеснок, соль, перец',
        'instructions': '1. Обжарьте бекон.\n2. Смешайте яйца с тертым сыром.\n3. Варите спагетти.\n4. Смешайте все ингредиенты.'
    },
    {
        'dish_name': 'Греческий салат',
        'ingredients': 'Помидоры, огурцы, оливки, фета, оливковое масло, лимонный сок, орегано, соль',
        'instructions': '1. Нарежьте помидоры и огурцы.\n2. Добавьте оливки и фета.\n3. Приправьте оливковым маслом, лимонным соком, орегано и солью.'
    },
    {
        'dish_name': 'Омлет',
        'ingredients': 'Яйца, молоко, соль, перец',
        'instructions': '1. Взбейте яйца в миске.\n2.Добавьте молоко, соль и перец.\n3.Хорошо перемешайте.\n4.Вылейте смесь на сковороду и жарьте до готовности.'
    },
    {
        'dish_name': 'Куриные котлеты',
        'ingredients': 'Куриное фарш, лук, чеснок, яйцо, соль, перец, хлебные крошки',
        'instructions': '1.Смешайте куриный фарш с нарезанным луком и чесноком.\n2.Добавьте яйцо, соль и перец.\n3.Сформируйте котлеты и обсыпьте их хлебными крошками.\n4.Жарьте котлеты с обеих сторон до золотистой корки.'
    },
    {
        'dish_name': 'Паста с соусом помидоров',
        'ingredients': 'Макароны, помидоры, лук, чеснок, оливковое масло, базилик, соль, перец',
        'instructions': '1.Обжарьте лук и чеснок в оливковом масле.\n2.Добавьте нарезанные помидоры и тушите их.\n3.Варите макароны в соленой воде.\n4.Смешайте соус с макаронами.\n5.Посыпьте сверху мелко нарезанным базиликом, солью и перцем.'
    },
    {
        'dish_name': 'Картошка по-деревенски',
        'ingredients': 'Картошка, растительное масло, соль, чеснок, зелень',
        'instructions': '1.Нарежьте картошку тонкими ломтями.\n2.Обсыпьте картошку маслом, добавьте соль и измельченный чеснок.\n3.Хорошо перемешайте и выложите на противень.\n4.Запекайте в предварительно разогретой духовке до золотистой корки.\n5.Посыпьте зеленью перед подачей.'
    },
    {
        'dish_name': 'Тыквенный крем-суп',
        'ingredients': 'Тыква, лук, картошка, сливки, соль, перец, масло',
        'instructions': '1.Обжарьте лук в масле.\n2.Добавьте кубики тыквы и картошки, обжаривайте несколько минут.\n3.Залейте овощи водой и варите до мягкости.\n4.Пюрируйте суп блендером, добавьте сливки, соль и перец.\n5.Доведите до кипения и подавайте горячим.'
    }
]

# Добавляем рецепты в базу данных
for recipe in recipes_data:
    cursor.execute('''
        INSERT INTO recipes (dish_name, ingredients, instructions)
        VALUES (?, ?, ?)
    ''', (recipe['dish_name'], recipe['ingredients'], recipe['instructions']))

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я бот с рецептами блюд. Чтобы получить рецепт, напиши /recipe.')


@bot.message_handler(commands=['recipe'])
def send_recipe(message):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes ORDER BY RANDOM() LIMIT 1')
    recipe = cursor.fetchone()
    conn.close()

    if recipe:
        dish_name, ingredients, instructions = recipe[1], recipe[2], recipe[3]
        response = f'Рецепт блюда "{dish_name}":\n\nИнгредиенты:\n{ingredients}\n\nИнструкции:\n{instructions}'
    else:
        response = 'Извините, рецепты закончились. Попробуйте позже.'

    bot.send_message(message.chat.id, response)


if __name__ == '__main__':
    bot.polling()
