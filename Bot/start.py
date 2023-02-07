from VKBot import Legacy
from config import group_token
from vk_api.bot_longpoll import VkBotEventType
from vk_api.keyboard import VkKeyboardColor
import re
import requests
import psql
import vk_func as vf


def favorite_longpoll(user_id, favorite_keyboard, menu_keyboard):
	people_list = []
	info_list = psql.check_favourite(vk_id_user=user_id)
	if len(info_list) > 0:
		people_list = []
		for element in info_list:
			people_list.append(element[0] + ' ' + element[1] + ' ' + element[2])
		VkBot.write_msg(user_id=user_id,
						message='Вот ваш список избранных:\n {}\n\n1. Вернуться назад\n 2. Убрать человека из ЧС'.format(
							'\n'.join(people_list)), keyboard=favorite_keyboard)
		for event in VkBot.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				if event.message['text'].lower() == 'вернуться назад' or event.message['text'] == '1':
					VkBot.write_msg(user_id=user_id,
									message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
					return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'], )
				elif event.message['text'].lower() == 'убрать человека из избранных' or event.message['text'] == '2':
					...
	else:
		return VkBot.write_msg(user_id=user_id, message='У вас нет людей в списке избранного', keyboard=menu_keyboard)


def registration_longpoll(question, user_id, menu_keyboard):  # Запуск сессии для регистрации пользователя в БД
	return_keyboard = VkBot.create_keyboard(buttons=[{
		'name': 'Вернуться назад',
		'color': VkKeyboardColor.PRIMARY,
		'type': 'text'}]).get_keyboard()
	if question == 'age':
		VkBot.write_msg(user_id=user_id, message='Введите ваш возраст:\n1. Вернуться назад', keyboard=return_keyboard)
		for event in VkBot.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				if event.message['text'].lower() == 'вернуться назад' or event.message['text'] == '1':
					VkBot.write_msg(user_id=user_id,
									message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
					return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'])
				try:
					return int(event.message['text'])
				except:
					VkBot.write_msg(user_id=event.message['from_id'], message='Введите возраст корректно',
									keyboard=return_keyboard)
	elif question == 'sex':
		VkBot.write_msg(user_id=user_id, message='Введите ваш пол: \n1. Мужской\n2. Женский\n3. Вернуться назад',
						keyboard=VkBot.create_keyboard([{
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
					VkBot.write_msg(user_id=user_id,
									message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
					return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'])
				elif event.message['text'].lower() == 'мужской' or event.message['text'] == '1':
					return 'Мужской'
				elif event.message['text'].lower() == 'женский' or event.message['text'] == '2':
					return 'Женский'
				else:
					VkBot.write_msg(user_id=event.message['from_id'],
									message='Введите пол корректно.\n1. Мужской\n2. Женский\n3. Вернуться назад',
									keyboard=VkBot.create_keyboard([{
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
	else:  # city
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
					VkBot.write_msg(user_id=user_id,
									message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
					return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'])
				try:
					return event.object['message']['geo']['place']['city']
				except:
					if event.message['text']:
						return event.message['text']
					else:
						VkBot.write_msg(user_id=user_id, message='Введите ваш город корректно\n 1. Вернуться назад',
										keyboard=location_keyboard)


def black_list_longpoll(user_id, return_keyboard, menu_keyboard):  # Запуск сессии для взаимодействия с черным списком
	print(1)
	black_list = psql.check_black_list(vk_id_user=user_id)
	if len(black_list) > 0:
		print(2)
		people_list = []
		for element in black_list:
			people_list.append(element[0] + ' ' + element[1] + ' ' + element[2])
		VkBot.write_msg(user_id=user_id,
						message='Вот ваш черный список:\n {}\n\n1. Вернуться назад\n 2. Убрать человека из ЧС'.format(
							'\n'.join(people_list)), keyboard=return_keyboard)
		for event in VkBot.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				request = event.message['text']
				if request.lower() == 'вернуться назад' or request == '1':
					VkBot.write_msg(user_id=user_id,
									message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
					return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'])
				elif request.lower() == 'убрать человека из чс' or request == '2':
					VkBot.write_msg(user_id=event.message['from_id'], message='В разработке', keyboard=return_keyboard)
				# delete_user_from_black_list(main_keyboard=return_keyboard, people_list=people_list)
				else:
					VkBot.write_msg(user_id=event.message['from_id'],
									message='Выберите вариант из предложенных!\n1. Вернуться назад\n2. Убрать человека из ЧС',
									keyboard=return_keyboard)
	else:
		return VkBot.write_msg(user_id=user_id, message='У вас нет людей в черном списке', keyboard=menu_keyboard)


def delete_user_from_black_list(main_keyboard, people_list):  # Запуск сессии для удаления из черного списка
	for event in VkBot.longpoll.listen():
		if event.type == VkBotEventType.MESSAGE_NEW:
			request = event.message['text']
			if re.search(r"[А-ЯA-Z]{1}[а-яa-z]+\s+[А-ЯA-Z]{1}[а-яa-z]+", request):
				VkBot.write_msg(user_id=event.message['from_id'], message='В разработке...')
			# DB.delete_user_black_list(request)
			elif request.lower() == 'вернуться назад' or request == '1':
				return VkBot.write_msg(user_id=event.message['from_id'],
									   message='Вот ваш черный список:\n {}\n1. Вернуться назад\n 2. Убрать человека из ЧС'.format(
										   people_list), keyboard=main_keyboard)
			else:
				return VkBot.write_msg(user_id=event.message['from_id'], message='Введите данные корректно',
									   keyboard=main_keyboard)


def info_searching(info, menu_keyboard, user_id, age_for_comparing=None):
	return_keyboard = VkBot.create_keyboard([{
		'name': 'Вернуться назад',
		'color': VkKeyboardColor.SECONDARY,
		'type': 'text'
	}]).get_keyboard()
	if info == 'age_at':
		VkBot.write_msg(user_id=user_id,
						message='Введите минимальный возраст людей, которых хотите найти:\n 1. Вернуться назад',
						keyboard=return_keyboard)
		for event in VkBot.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				if event.message['text'] == 'Вернуться назад' or event.message['text'] == '1':
					VkBot.write_msg(user_id=user_id,
									message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
					return main(user_id=event.message['from_id'], menu_keyboard=menu_keyboard)
				try:
					int(event.message['text'])
					return event.message['text']
				except:
					VkBot.write_msg(user_id=event.message['from_id'], message='Введите возраст корректно')

	elif info == 'age_to':
		VkBot.write_msg(user_id=user_id,
						message='Введите максимальный возраст людей, которых хотите найти:\n 1. Вернуться назад',
						keyboard=return_keyboard)
		for event in VkBot.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				if event.message['text'] == 'Вернуться назад' or event.message['text'] == '1':
					VkBot.write_msg(user_id=user_id,
									message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
					return main(user_id=event.message['from_id'], menu_keyboard=menu_keyboard)
				try:
					int(event.message['text'])
					if int(age_for_comparing) >= int(event.message['text']):
						VkBot.write_msg(user_id=user_id, message='Введите возраст больше {}'.format(age_for_comparing))
					else:
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
		VkBot.write_msg(user_id=user_id,
						message='Поиск девушек или парней?\n 1. Девушек\n2. Парней\n3. Любой пол\n4. Вернуться назад',
						keyboard=sex_keyboard)
		for event in VkBot.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				if event.message['text'] == 'Искать парней' or event.message['text'] == '2':
					return '2'
				elif event.message['text'] == 'Искать девушек' or event.message['text'] == '1':
					return '1'
				elif event.message['text'] == 'Любой пол' or event.message['text'] == '3':
					return '0'
				elif event.message['text'] == 'Вернуться назад' or event.message['text'] == '4':
					VkBot.write_msg(user_id=user_id,
									message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
					return main(user_id=event.message['from_id'], menu_keyboard=menu_keyboard)
				else:
					VkBot.write_msg(user_id=event.message['from_id'], message='Некорректный ответ',
									keyboard=sex_keyboard)
	else:  # City
		city_keyboard = VkBot.create_keyboard([{
			'type': 'location'
		},
			{
				'name': 'Вернуться назад',
				'color': VkKeyboardColor.PRIMARY,
				'type': 'text'
			}]).get_keyboard()
		VkBot.write_msg(user_id=user_id, message='Введите город, в котором хотите искать:\n 1. Вернуться назад',
						keyboard=city_keyboard)
		for event in VkBot.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				if event.message['text'] == 'Вернуться назад' or event.message['text'] == '1':
					VkBot.write_msg(user_id=user_id,
									message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
					return main(menu_keyboard=menu_keyboard)
				try:
					return event.object['message']['geo']['place']['city']
				except:
					if event.message['text']:
						return event.message['text']
					else:
						VkBot.write_msg(user_id=event.message['from_id'],
										message='Введите город корректно\n 1. Вернуться назад', keyboard=city_keyboard)


def searching_question(search_keyboard, like_for_id=None, photo_id=None, count_like=0, fav_name=None, fav_surname=None,
					   fav_link=None, attachment=[]):
	for event in VkBot.longpoll.listen():
		if event.type == VkBotEventType.MESSAGE_NEW:
			if event.message['text'].lower() == 'следующий человек' or event.message['text'] == '1':
				return True
			elif event.message['text'].lower() == 'поставить лайк' or event.message['text'] == '2':
				if count_like == -1:
					VkBot.write_msg(user_id=event.message['from_id'], message='У человека закрыт доступ к фото',
									keyboard=search_keyboard)

				elif count_like > 0:
					VkBot.write_msg(user_id=event.message['from_id'], message='Вы уже поставили лайк',
									keyboard=search_keyboard)
				else:
					vf.like_add(user_id=event.message['from_id'], owner_id=like_for_id, photo_id=photo_id)
					count_like += 1
					VkBot.write_msg(user_id=event.message['from_id'], message='👍', keyboard=search_keyboard)
			elif event.message['text'].lower() == 'вернуться назад' or event.message['text'] == '3':
				return False
			elif event.message['text'].lower() == 'добавить в избранных' or event.message['text'] == '4':
				if (fav_name, fav_surname, fav_link) in psql.check_favourite(vk_id_user=event.message['from_id']):
					VkBot.write_msg(user_id=event.message['from_id'], message='Пользователь уже в списке избранных',
									keyboard=search_keyboard)
				elif (fav_name, fav_surname, fav_link) in psql.check_black_list(vk_id_user=event.message['from_id']):
					VkBot.write_msg(user_id=event.message['from_id'], message='Пользователь в ЧС',
									keyboard=search_keyboard)
				else:
					psql.add_user_favourite(vk_id_user=event.message['from_id'], name=fav_name, surname=fav_surname,
											link=fav_link, fav_vk_id=like_for_id)
					# psql.add_user_favourite_photos(fav_vk_id=like_for_id, link_photo=attachment)
					VkBot.write_msg(user_id=event.message['from_id'], message='✅', keyboard=search_keyboard)
			elif event.message['text'].lower() == 'добавить в чс' or event.message['text'] == '5':
				if (fav_name, fav_surname, fav_link) in psql.check_black_list(vk_id_user=event.message['from_id']):
					VkBot.write_msg(user_id=event.message['from_id'], message='Пользователь уже в ЧС',
									keyboard=search_keyboard)
				elif (fav_name, fav_surname, fav_link) in psql.check_favourite(vk_id_user=event.message['from_id']):
					VkBot.write_msg(user_id=event.message['from_id'], message='Пользователь в списке избранных',
									keyboard=search_keyboard)
				else:
					psql.add_user_black_list(vk_id_user=event.message['from_id'], name=fav_name, surname=fav_surname,
											 link=fav_link, bl_vk_id=like_for_id)
					VkBot.write_msg(user_id=event.message['from_id'], message='✅', keyboard=search_keyboard)
			else:
				VkBot.write_msg(user_id=event.message['from_id'], message='Выберите вариант из предложенных',
								keyboard=search_keyboard)


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
		},
		{
			'name': 'Добавить в избранных',
			'color': VkKeyboardColor.POSITIVE,
			'type': 'text'
		},
		{
			'name': 'Добавить в ЧС',
			'color': VkKeyboardColor.NEGATIVE,
			'type': 'text'
		}]).get_keyboard()
	age_at = info_searching(info='age_at', menu_keyboard=menu_keyboard, user_id=user_id)
	for user in vf.search_users(age_at=age_at,
								age_to=info_searching(info='age_to', menu_keyboard=menu_keyboard, user_id=user_id,
													  age_for_comparing=age_at),
								sex=info_searching(info='sex', menu_keyboard=menu_keyboard, user_id=user_id),
								city=info_searching(info='city', menu_keyboard=menu_keyboard, user_id=user_id),
								vk_id=user_id):
		VkBot.write_msg(user_id=user_id, message='{} {}\n{}\n'.format(user['name'], user['surname'], user['link']))
		attachment = vf.get_photo(user_id=user_id, owner_id=user['vk_id_user'], mode='photo')
		if isinstance(attachment, str):
			VkBot.write_msg(user_id=user_id, message=attachment)
			VkBot.write_msg(user_id=user_id,
							message='1. Следующий человек\n2. Поставить лайк\n3. Вернуться назад\n4. Добавить в избранных\n5. Добавить в ЧС',
							keyboard=search_keyboard)
			if searching_question(search_keyboard=search_keyboard, count_like=-1, like_for_id=user['vk_id_user'],
								  fav_link=user['link'], fav_name=user['name'], fav_surname=user['surname'],
								  attachment=[]) == True:
				pass
			else:
				return VkBot.write_msg(user_id=user_id,
									   message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									   keyboard=menu_keyboard)
		else:
			VkBot.send_photo(user_id=user_id, attachment=attachment, keyboard=search_keyboard)
			VkBot.write_msg(user_id=user_id,
							message='1. Следующий человек\n2. Поставить лайк\n3. Вернуться назад\n4. Добавить в избранных\n5. Добавить в ЧС',
							keyboard=search_keyboard)
			if searching_question(search_keyboard=search_keyboard, like_for_id=user['vk_id_user'],
								  photo_id=vf.get_photo(user_id=user_id, owner_id=user['vk_id_user'], mode='photo_id'),
								  count_like=0, fav_link=user['link'], fav_name=user['name'],
								  fav_surname=user['surname'], attachment=attachment) == True:
				pass
			else:
				return VkBot.write_msg(user_id=user_id,
									   message='Меню:\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									   keyboard=menu_keyboard)


def get_token(open_link_keyboard):  # Регистрация токена от пользователя
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
				},
				{
					'name': 'Просмотреть список избранных',
					'color': VkKeyboardColor.SECONDARY,
					'type': 'text'
				}
			]).get_keyboard()
			access_token = event.message['text']
			if 'error' in requests.get('https://api.vk.com/method/users.get',
									   params={'access_token': access_token, 'user_ids': event.message['from_id'],
											   'fields': 'first_name', 'name_case': 'nom',
											   'v': '5.131'}).json():  # Запрос делается через requests, так как нужно проверить токен пользователя, если сделать запрос через VkBot, то будет запрос с работающего токена группы
				VkBot.write_msg(user_id=event.message['from_id'],
								message='Ваш токен неверен, проверьте правильность ввода и отправьте повторно',
								keyboard=open_link_keyboard)
			else:
				VkBot.write_msg(user_id=event.message['from_id'],
								message='Привет, {}, я Бот Legacy для поиска людей\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных\n Для быстрых ответов можно использовать цифры'.format(
									VkBot.get_name(user_id=event.message['from_id'])[0]), keyboard=menu_keyboard)
				return main(menu_keyboard=menu_keyboard, user_id=event.message['from_id'], access_token=access_token)


def start_bot():  # Первая сессия, которая запускается для получения токена
	open_link_keyboard = VkBot.create_keyboard([{
		'name': 'Получить',
		'link': 'https://oauth.vk.com/authorize?client_id=51537818&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,wall,photos&response_type=token&v=5.131&state=123456',
		'type': 'link'
	}]).get_keyboard()

	for event in VkBot.longpoll.listen():
		if event.type == VkBotEventType.MESSAGE_NEW:
			request = event.message['text']
			if request:
				VkBot.write_msg(user_id=event.message['from_id'],
								message="1. Для работы приложения пришли мне свой токен\n2. Перед ответами Боту ждите 1 секунду, чтобы он успевал обрабатывать запросы.\n3. Токен находится в адресной строке, в параметре access_token после = и до &",
								keyboard=open_link_keyboard)
				get_token(open_link_keyboard=open_link_keyboard)


def main(menu_keyboard, user_id, access_token=None):
	for event in VkBot.longpoll.listen():
		if event.type == VkBotEventType.MESSAGE_NEW:
			request = event.message['text']
			if request.lower() == 'начать поиск' or request == '1':
				VkBot.write_msg(user_id=event.message['from_id'],
								message='Перед ответами Боту ждите 1 секунду, чтобы он успевал обрабатывать запросы.')
				if psql.registr_info(event.message['from_id']) == True:
					start_search(user_id=event.message['from_id'], menu_keyboard=menu_keyboard)
				else:
					VkBot.write_msg(user_id=user_id, message='Вы ещё не зарегистрированы. Пройдите регистрацию.')
					psql.registration(vk_id_user=event.message['from_id'],
									  name=VkBot.get_name(user_id=event.message['from_id'])[0],
									  surname=VkBot.get_name(user_id=event.message['from_id'])[1],
									  age=registration_longpoll(user_id=event.message['from_id'], question='age',
																menu_keyboard=menu_keyboard),
									  sex=registration_longpoll(user_id=event.message['from_id'], question='sex',
																menu_keyboard=menu_keyboard),
									  city=registration_longpoll(user_id=event.message['from_id'], question='city',
																 menu_keyboard=menu_keyboard), user_token=access_token)
					start_search(user_id=event.message['from_id'], menu_keyboard=menu_keyboard)
			elif request.lower() == 'просмотреть черный список' or request == '2':
				VkBot.write_msg(user_id=event.message['from_id'],
								message='Перед ответами Боту ждите 1 секунду, чтобы он успевал обрабатывать запросы.')
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
					black_list_longpoll(user_id=event.message['from_id'], return_keyboard=black_list_keyboard,
										menu_keyboard=menu_keyboard)
				else:
					VkBot.write_msg(user_id=user_id, message='Вы ещё не зарегистрированы. Пройдите регистрацию.')
					psql.registration(vk_id_user=event.message['from_id'],
									  name=VkBot.get_name(user_id=event.message['from_id'])[0],
									  surname=VkBot.get_name(user_id=event.message['from_id'])[1],
									  age=registration_longpoll(user_id=event.message['from_id'], question='age',
																menu_keyboard=menu_keyboard),
									  sex=registration_longpoll(user_id=event.message['from_id'], question='sex',
																menu_keyboard=menu_keyboard),
									  city=registration_longpoll(user_id=event.message['from_id'], question='city',
																 menu_keyboard=menu_keyboard), user_token=access_token)
					VkBot.write_msg(user_id=event.message['from_id'],
									message='Вы ещё не начинали поиск\n\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
			elif request.lower() == 'просмотреть список избранных' or request == '3':
				if psql.registr_info(vk_id=event.message['from_id']) == True:
					favorite_keyboard = VkBot.create_keyboard([{
						'name': 'Вернуться назад',
						'color': VkKeyboardColor.PRIMARY,
						'type': 'text'
					},
						{
							'name': 'Убрать человека из списка избранных',
							'color': VkKeyboardColor.NEGATIVE,
							'type': 'text'
						}
					]).get_keyboard()
					VkBot.write_msg(user_id=user_id,
									message='Перед ответами Боту ждите 1 секунду, чтобы он успевал обрабатывать запросы.',
									keyboard=favorite_keyboard)
					favorite_longpoll(user_id=user_id, favorite_keyboard=favorite_keyboard, menu_keyboard=menu_keyboard)
				else:
					VkBot.write_msg(user_id=user_id, message='Вы ещё не зарегистрированы. Пройдите регистрацию.')
					psql.registration(vk_id_user=event.message['from_id'],
									  name=VkBot.get_name(user_id=event.message['from_id'])[0],
									  surname=VkBot.get_name(user_id=event.message['from_id'])[1],
									  age=registration_longpoll(user_id=event.message['from_id'], question='age',
																menu_keyboard=menu_keyboard),
									  sex=registration_longpoll(user_id=event.message['from_id'], question='sex',
																menu_keyboard=menu_keyboard),
									  city=registration_longpoll(user_id=event.message['from_id'], question='city',
																 menu_keyboard=menu_keyboard), user_token=access_token)
					VkBot.write_msg(user_id=event.message['from_id'],
									message='Вы ещё не начинали поиск\n\n1. Начать поиск\n2. Просмотреть черный список\n3. Просмотреть список избранных',
									keyboard=menu_keyboard)
			else:
				VkBot.write_msg(user_id=event.message['from_id'], message='Выберите команду из предложенных!',
								keyboard=menu_keyboard)


if __name__ == "__main__":
	VkBot = Legacy(group_token=group_token)
	psql.create_tables(engine=psql.engine)
	start_bot()
