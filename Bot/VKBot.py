import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class Legacy:
    def __init__(self, group_token):
        self.token = group_token
        self.vk = vk_api.VkApi(token=group_token)
        self.longpoll = VkLongPoll(self.vk)
    def create_keyboard(self, buttons=[]):
        keyboard = VkKeyboard(one_time=True)
        for button in buttons:
            name = button['name']
            if button['type'] == 'text':
                color = button['color']
                keyboard.add_button(label = f'{name}', color=color)
            elif button['type'] == 'link':
                link = button['link']
                keyboard.add_openlink_button(label=f'{name}', link=link)
            
        return keyboard
    def get_name(self, user_id):
        name = self.vk.method('users.get', {'user_ids': user_id, 'access_token': self.token, 'name_case': 'nom'})[0]['first_name']
        return name
    def write_msg(self, user_id, message, keyboard = None):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), 'keyboard': keyboard})