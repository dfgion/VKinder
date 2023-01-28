from VKBot import Legacy
from config import group_token
from vk_api.longpoll import VkEventType
from pprint import pprint
from vk_api.keyboard import VkKeyboardColor
import re

def black_list_longpoll(return_keyboard, menu_keyboard):
    for event in VkBot.longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:

                                if event.to_me:
                                    request = event.text
                                    if request.lower() == 'вернуться назад':
                                        return VkBot.write_msg(user_id=event.user_id, message = f"Меню:", keyboard=menu_keyboard)
                                    elif request.lower() == 'убрать человека из чс':
                                        VkBot.write_msg(user_id=event.user_id, message='Введите имя и фамилию того, кого хотите убрать')
                                        delete_user_from_black_list(main_keyboard=return_keyboard)
                                    else:
                                        VkBot.write_msg(user_id=event.user_id, message='Выберите вариант из предложенных!', keyboard=return_keyboard)

def delete_user_from_black_list(main_keyboard):
    for event in VkBot.longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:

                                if event.to_me:
                                    request = event.text
                                    if re.search(r"[А-ЯA-Z]{1}[а-яa-z]+\s+[А-ЯA-Z]{1}[а-яa-z]+", request):
                                        return VkBot.write_msg(user_id=event.user_id, message='В разработке...', keyboard=main_keyboard)
                                        # DB.delete_user_black_list(request)
                                    else:
                                        return VkBot.write_msg(user_id=event.user_id, message='Введите данные корректно', keyboard=main_keyboard)


def main():
    for event in VkBot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text
            if request.lower() == "начать":
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
                VkBot.write_msg(user_id=event.user_id, 
                                message = f"Привет, {VkBot.get_name(event.user_id)}, Я Legacy-Бот для поиска людей.", 
                                keyboard=menu_keyboard)                                                         
            elif request.lower() == 'начать поиск':
                VkBot.write_msg(user_id=event.user_id, message='В разработке...', keyboard=menu_keyboard)
                # if registr_info() == True:
                #     ...
                # else:
                #     registration()
            elif request.lower() == 'просмотреть черный список':
                if True:
                    keyboard = VkBot.create_keyboard([{
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
                    VkBot.write_msg(user_id=event.user_id, message=f'Вот ваш черный список:', keyboard=keyboard)
                    black_list_longpoll(return_keyboard=keyboard, menu_keyboard=menu_keyboard)
                else:
                    registration()
            else:
                VkBot.write_msg(user_id=event.user_id, message='Выберите команду из предложенных!', keyboard=menu_keyboard)

                    
                        
if __name__ == "__main__":
    VkBot = Legacy(group_token=group_token)
    main()


