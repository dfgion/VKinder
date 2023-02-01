from VKBot import Legacy
from config import group_token
from vk_api.bot_longpoll import VkBotEventType
from vk_api.keyboard import VkKeyboardColor
import re
import requests
import psql 
import vk_func as vf

def registration_longpoll(question, user_id, menu_keyboard): # Запуск сессии для регистрации пользователя в БД
    return_keyboard = VkBot.create_keyboard(buttons=[{
                                        'name': 'Вернуться назад', 
                                        'color': VkKeyboardColor.PRIMARY, 
                                        'type': 'text'}]).get_keyboard()
    if question == 'age':
        VkBot.write_msg(user_id=user_id, message='Введите ваш возраст:\n1. Вернуться назад', keyboard=return_keyboard)
        for event in VkBot.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.message['text'].lower() == 'вернуться назад' or event.message['text'] == '1':
                    VkBot.write_msg(user_id=user_id, message='Меню:\n1. Начать поиск\n2. Просмотреть черный список', keyboard=menu_keyboard)
                    return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'])
                try:
                    return int(event.message['text'])
                except:
                    VkBot.write_msg(user_id=event.message['from_id'], message='Введите возраст корректно', keyboard=return_keyboard)               
    elif question == 'sex':
        VkBot.write_msg(user_id=user_id, message='Введите ваш пол: \n1. Мужской\n2. Женский\n3. Вернуться назад', keyboard=VkBot.create_keyboard([{
                                                                                                        'name': 'Мужской',
                                                                                                        'color': VkKeyboardColor.SECONDARY,
                                                                                                        'type': 'text'
                                                                                                         },
                                                                                                         {
                                                                                                        'name': 'Женский',
                                                                                                        'color': VkKeyboardColor.SECONDARY,
                                                                                                        'type': 'text'
                                                                                                         },
                                                                                                         {
                                                                                                        'name': 'Вернуться назад',
                                                                                                        'color': VkKeyboardColor.PRIMARY,
                                                                                                        'type': 'text'
                                                                                                         }]).get_keyboard())
        for event in VkBot.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.message['text'].lower() == 'вернуться назад' or event.message['text'] == '3': 
                        VkBot.write_msg(user_id=user_id, message='Меню:\n1. Начать поиск\n2. Просмотреть черный список', keyboard=menu_keyboard)
                        return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'])
                    elif event.message['text'].lower() == 'мужской' or event.message['text'] == '1':
                        return 'Мужской'
                    elif event.message['text'].lower() == 'женский' or event.message['text'] == '2':
                        return 'Женский'
                    else:
                        VkBot.write_msg(user_id=event.message['from_id'], message='Введите пол корректно.\n1. Мужской\n2. Женский\n3. Вернуться назад', keyboard=VkBot.create_keyboard([{
                                                                                                                                                            'name': 'Мужской',
                                                                                                                                                            'color': VkKeyboardColor.SECONDARY,
                                                                                                                                                            'type': 'text'
                                                                                                                                                            },
                                                                                                                                                            {
                                                                                                                                                            'name': 'Женский',
                                                                                                                                                            'color': VkKeyboardColor.SECONDARY,
                                                                                                                                                            'type': 'text'
                                                                                                                                                            },
                                                                                                                                                            {
                                                                                                                                                            'name': 'Вернуться назад',
                                                                                                                                                            'color': VkKeyboardColor.PRIMARY,
                                                                                                                                                            'type': 'text'
                                                                                                                                                            }]).get_keyboard())
    else: # city
        location_keyboard = VkBot.create_keyboard([{ 
                                                    'type': 'location'
                                                    },
                                                    {
                                                    'name': 'Вернуться назад', 
                                                    'color': VkKeyboardColor.PRIMARY, 
                                                    'type': 'text'
                                                    }
                                                    ]).get_keyboard()
        VkBot.write_msg(user_id=user_id, message='Введите ваш город\n 1. Вернуться назад', keyboard=location_keyboard)
        for event in VkBot.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.message['text'].lower() == 'вернуться назад' or event.message['text'] == '1': 
                    VkBot.write_msg(user_id=user_id, message='Меню:\n1. Начать поиск\n2. Просмотреть черный список', keyboard=menu_keyboard)
                    return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'])
                try:
                    return event.object['message']['geo']['place']['city']
                except:
                    if event.message['text']:
                        return event.message['text']
                    else: 
                        VkBot.write_msg(user_id=user_id, message='Введите ваш город корректно\n 1. Вернуться назад', keyboard=location_keyboard)


def black_list_longpoll(user_id, return_keyboard, menu_keyboard): # Запуск сессии для взаимодействия с черным списком
    black_list = ['Алена Семенова', 'Артур Пирожков']
    people_list = '\n'.join(black_list)
    if len(people_list) > 0:
        VkBot.write_msg(user_id=user_id, message=f'Вот ваш черный список:\n {people_list}\n\n1. Вернуться назад\n 2. Убрать человека из ЧС', keyboard=return_keyboard)
        for event in VkBot.longpoll.listen():
                                if event.type == VkBotEventType.MESSAGE_NEW:
                                        request = event.message['text']
                                        if request.lower() == 'вернуться назад' or request == '1':
                                            VkBot.write_msg(user_id=user_id, message='Меню:\n1. Начать поиск\n2. Просмотреть черный список', keyboard=menu_keyboard)
                                            return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'])
                                        elif request.lower() == 'убрать человека из чс' or request == '2':
                                            VkBot.write_msg(user_id=event.message['from_id'], message='В разработке', keyboard=return_keyboard)
                                            # delete_user_from_black_list(main_keyboard=return_keyboard, people_list=people_list)
                                        else:
                                            VkBot.write_msg(user_id=event.message['from_id'], message='Выберите вариант из предложенных!\n1. Вернуться назад\n2. Убрать человека из ЧС', keyboard=return_keyboard)
    else:
        return VkBot.write_msg(user_id=user_id, message=f'У вас нет людей в черном списке', keyboard=menu_keyboard)

def delete_user_from_black_list(main_keyboard, people_list): # Запуск сессии для удаления из черного списка
    for event in VkBot.longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            request = event.message['text']
            if re.search(r"[А-ЯA-Z]{1}[а-яa-z]+\s+[А-ЯA-Z]{1}[а-яa-z]+", request):
                VkBot.write_msg(user_id=event.message['from_id'], message='В разработке...')
                # DB.delete_user_black_list(request)
            elif request.lower() == 'вернуться назад' or request == '1':
                return VkBot.write_msg(user_id=event.message['from_id'], message=f'Вот ваш черный список:\n {people_list}\n1. Вернуться назад\n 2. Убрать человека из ЧС', keyboard=main_keyboard)
            else:
                return VkBot.write_msg(user_id=event.message['from_id'], message='Введите данные корректно', keyboard=main_keyboard)

def info_searching(info, menu_keyboard, user_id):
    return_keyboard = VkBot.create_keyboard([{
                        'name': 'Вернуться назад',
                        'color': VkKeyboardColor.SECONDARY,
                        'type': 'text'
                       }]).get_keyboard()
    if info == 'age_at':
        VkBot.write_msg(user_id=user_id, message='Введите минимальный возраст людей, которых хотите найти:\n 1. Вернуться назад', keyboard=return_keyboard)
        for event in VkBot.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.message['text'] == 'Вернуться назад' or event.message['text'] == '1':
                    VkBot.write_msg(user_id=user_id, message='Меню:\n1. Начать поиск\n2. Просмотреть черный список', keyboard=menu_keyboard)
                    return main(user_id=event.message['from_id'], menu_keyboard=menu_keyboard)
                try:
                    int(event.message['text'])
                    return event.message['text']
                except:
                    VkBot.write_msg(user_id=event.message['from_id'], message='Введите возраст корректно')
    elif info == 'age_to':
        VkBot.write_msg(user_id=user_id, message='Введите максимальный возраст людей, которых хотите найти:\n 1. Вернуться назад', keyboard=return_keyboard)
        for event in VkBot.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.message['text'] == 'Вернуться назад' or event.message['text'] == '1':
                    VkBot.write_msg(user_id=user_id, message='Меню:\n1. Начать поиск\n2. Просмотреть черный список', keyboard=menu_keyboard)
                    return main(user_id=event.message['from_id'], menu_keyboard=menu_keyboard)
                try:
                    int(event.message['text'])
                    return event.message['text']
                except:
                    VkBot.write_msg(user_id=event.message['from_id'], message='Введите возраст корректно')
    elif info == 'sex':
        sex_keyboard = VkBot.create_keyboard([{
                                                'name': 'Искать девушек', 
                                                'color': VkKeyboardColor.SECONDARY, 
                                                'type': 'text'
                                            },
                                            {
                                                'name': 'Искать парней',
                                                'color': VkKeyboardColor.SECONDARY,
                                                'type': 'text'
                                            },
                                            {
                                                'name': 'Любой пол',
                                                'color': VkKeyboardColor.SECONDARY,
                                                'type': 'text'
                                            },
                                            {
                                                'name': 'Вернуться назад',
                                                'color': VkKeyboardColor.PRIMARY,
                                                'type': 'text'
                                            }]).get_keyboard()
        VkBot.write_msg(user_id=user_id, message='Поиск девушек или парней?\n 1. Девушек\n2. Парней\n3. Любой пол\n4. Вернуться назад', keyboard=sex_keyboard)
        for event in VkBot.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:                                                                                                
                if event.message['text'] == 'Искать парней' or event.message['text'] == '2':
                    return '2'
                elif event.message['text'] == 'Искать девушек' or event.message['text'] == '1':
                    return '1'
                elif event.message['text'] == 'Любой пол' or event.message['text'] == '3':
                    return '0'
                elif event.message['text'] == 'Вернуться назад' or event.message['text'] == '4':
                    VkBot.write_msg(user_id=user_id, message='Меню:\n1. Начать поиск\n2. Просмотреть черный список', keyboard=menu_keyboard)
                    return main(user_id=event.message['from_id'], menu_keyboard=menu_keyboard)
                else:
                    VkBot.write_msg(user_id=event.message['from_id'], message='Некорректный ответ', keyboard=sex_keyboard)
    else: #City
        city_keyboard = VkBot.create_keyboard([{ 
                                                'type': 'location'
                                                },
                                                {
                                                'name': 'Вернуться назад', 
                                                'color': VkKeyboardColor.PRIMARY, 
                                                'type': 'text'
                                                }]).get_keyboard()
        VkBot.write_msg(user_id=user_id, message='Введите город, в котором хотите искать:\n 1. Вернуться назад', keyboard=city_keyboard)
        for event in VkBot.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:                                                                                                                                        
                if event.message['text'] == 'Вернуться назад' or event.message['text'] == '1':
                    VkBot.write_msg(user_id=user_id, message='Меню:\n1. Начать поиск\n2. Просмотреть черный список', keyboard=menu_keyboard)
                    return main(menu_keyboard=menu_keyboard) 
                try:
                    return event.object['message']['geo']['place']['city']
                except:
                    if event.message['text']:
                        return event.message['text']
                    else:
                        VkBot.write_msg(user_id=event.message['from_id'], message='Введите город корректно\n 1. Вернуться назад', keyboard=city_keyboard)
                
def searching_question(search_keyboard):
    for event in VkBot.longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.message['text'].lower() == 'следующий человек':
                return True
            elif event.message['text'].lower() == 'вернуться назад':
                return False
            elif event.message['text'].lower() == 'поставить лайк':
                ...
            else:
                VkBot.write_msg(user_id=event.message['from_id'], message='Выберите вариант из предложенных', keyboard=search_keyboard)
def start_search(menu_keyboard, user_id):
    search_keyboard = VkBot.create_keyboard([{
                                            'name': 'Следующий человек',  
                                            'color': VkKeyboardColor.SECONDARY,
                                            'type': 'text'
                                            },
                                            {
                                            'name': 'Поставить лайк',  
                                            'color': VkKeyboardColor.POSITIVE,
                                            'type': 'text'
                                            },
                                            {
                                            'name': 'Вернуться назад',  
                                            'color': VkKeyboardColor.PRIMARY,
                                            'type': 'text'  
                                            }]).get_keyboard()
    for user in vf.search_users(sex=info_searching(info='sex', menu_keyboard=menu_keyboard, user_id=user_id), age_at=info_searching(info='age_at', menu_keyboard=menu_keyboard, user_id=user_id), age_to=info_searching(info='age_to', menu_keyboard=menu_keyboard, user_id=user_id), city =info_searching(info='city', menu_keyboard=menu_keyboard, user_id=user_id), vk_id=user_id):
        VkBot.write_msg(user_id=user_id, message='{} {}\n{}\n'.format(user['name'], user['surname'], user['link']), keyboard=search_keyboard)
        if searching_question(search_keyboard=search_keyboard) == True:
            pass
        else:
            return VkBot.write_msg(user_id=user_id, message='Меню:\n1. Начать поиск\n2. Просмотреть черный список', keyboard=menu_keyboard)

def get_token(): # Регистрация токена от пользователя
    for event in VkBot.longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW:
                                    menu_keyboard = VkBot.create_keyboard([{
                                                        'name': 'Начать поиск', 
                                                        'color': VkKeyboardColor.POSITIVE, 
                                                        'type': 'text'
                                                        },
                                                        {
                                                        'name': 'Просмотреть черный список',
                                                        'color': VkKeyboardColor.NEGATIVE,
                                                        'type': 'text'
                                                        }
                                                        ]).get_keyboard()
                                    access_token = event.message['text']
                                    if 'error' in requests.get('https://api.vk.com/method/users.get', params={'access_token': access_token, 'user_ids': event.message['from_id'], 'fields': 'first_name', 'name_case': 'nom', 'v': '5.131'}).json(): # Запрос делается через requests, так как нужно проверить токен пользователя, если сделать запрос через VkBot, то будет запрос с работающего токена группы
                                        VkBot.write_msg(user_id=event.message['from_id'], message='Ваш токен неверен, проверьте правильность ввода и отправьте повторно')
                                    else:
                                        VkBot.write_msg(user_id=event.message['from_id'], message='Привет, {}, я Бот Legacy для поиска людей\n1. Начать поиск\n2. Просмотреть черный список\n Для быстрых ответов можно использовать цифры'.format(VkBot.get_name(user_id=event.message['from_id'])[0]), keyboard=menu_keyboard)
                                        return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'], access_token=access_token)

def start_bot(): # Первая сессия, которая запускается для получения токена
    for event in VkBot.longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            request = event.message['text']
            if request:
                    VkBot.write_msg(user_id=event.message['from_id'], 
                                    message = "Для работы приложения пришли мне свой токен из адресной строки, перейдя по этой ссылке:\nhttps://oauth.vk.com/authorize?client_id=51535805&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,wall,photos&response_type=token&v=5.131&state=123456\nТокен - это значение, которое идёт после access_token= и до &") 
                    get_token()

def main(menu_keyboard, user_id, access_token = None):
    for event in VkBot.longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            request = event.message['text']                                                     
            if request.lower() == 'начать поиск' or request == '1':
                if psql.registr_info(event.message['from_id']) == True:
                    start_search(user_id = event.message['from_id'], menu_keyboard=menu_keyboard)
                else:
                    VkBot.write_msg(user_id=user_id, message='Вы ещё не зарегистрированы. Пройдите регистрацию.')
                    psql.registration(vk_id_user=event.message['from_id'], name=VkBot.get_name(user_id=event.message['from_id'])[0], surname=VkBot.get_name(user_id=event.message['from_id'])[1], age=registration_longpoll(user_id=event.message['from_id'], question='age', menu_keyboard=menu_keyboard), sex=registration_longpoll(user_id=event.message['from_id'], question='sex', menu_keyboard=menu_keyboard), city=registration_longpoll(user_id=event.message['from_id'], question='city', menu_keyboard=menu_keyboard), user_token=access_token)
                    start_search(user_id = event.message['from_id'], menu_keyboard=menu_keyboard)
            elif request.lower() == 'просмотреть черный список' or request == '2':
                if psql.registr_info(vk_id=event.message['from_id']) == True:
                    black_list_keyboard = VkBot.create_keyboard([{
                                                    'name': 'Вернуться назад', 
                                                    'color': VkKeyboardColor.PRIMARY, 
                                                    'type': 'text'
                                                    },
                                                    {
                                                    'name': 'Убрать человека из ЧС',
                                                    'color': VkKeyboardColor.NEGATIVE,
                                                    'type': 'text'
                                                    }
                                                    ]).get_keyboard()
                    black_list_longpoll(user_id=event.message['from_id'], return_keyboard=black_list_keyboard, menu_keyboard=menu_keyboard)
                else:
                    VkBot.write_msg(user_id=user_id, message='Вы ещё не зарегистрированы. Пройдите регистрацию.')
                    psql.registration(vk_id_user=event.message['from_id'], name=VkBot.get_name(user_id=event.message['from_id'])[0], surname=VkBot.get_name(user_id=event.message['from_id'])[1], age=registration_longpoll(user_id=event.message['from_id'], question='age', menu_keyboard=menu_keyboard), sex=registration_longpoll(user_id=event.message['from_id'], question='sex', menu_keyboard=menu_keyboard), city=registration_longpoll(user_id=event.message['from_id'], question='city', menu_keyboard=menu_keyboard), user_token=access_token)
                    VkBot.write_msg(user_id=event.message['from_id'], message='Вы ещё не начинали поиск\n1. Начать поиск\n2. Просмотреть черный список', keyboard=menu_keyboard)
            else:
                VkBot.write_msg(user_id=event.message['from_id'], message='Выберите команду из предложенных!', keyboard=menu_keyboard)

class TOKEN:
    def __init__(self, token):
          self.TOKEN = token

if __name__ == "__main__":
    VkBot = Legacy(group_token=group_token)
    psql.create_tables(engine=psql.engine)
    start_bot()


