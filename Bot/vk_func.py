import vk_api
from vk_api.exceptions import ApiError
from psql import User
from psql import session


# Поиск партнеров
# => Принимает sex, age_at, age_to, city
# => Возращает список из словарей {'name': 'test', 'surname': 'test', 'link': 'test', 'vk_id_user': 'test'}

def search_users(sex, age_at, age_to, city, vk_id):
	vk_user = vk_api.VkApi(token=session.query(User).filter_by(vk_id_user=vk_id).first().token)
	suitable_people = []
	basic_link = 'https://vk.com/id'
	response = vk_user.method('users.search',
							  {'sort': 1,
							   'sex': sex,
							   'status': 6,
							   'age_from': age_at,
							   'age_to': age_to,
							   'has_photo': 1,
							   'count': 300,
							   'online': 0,
							   'hometown': city
							   })
	for element in response['items']:
		people = {'name': element['first_name'], 'surname': element['last_name'],
				  'link': basic_link + str(element['id']), 'vk_id_user': element['id']}
		suitable_people.append(people)
	return suitable_people


def like_add(user_id, owner_id, photo_id):
	vk_user = vk_api.VkApi(token=session.query(User).filter_by(vk_id_user=user_id).first().token)
	vk_user.method('likes.add', {'type': 'photo', 'owner_id': owner_id, 'item_id': photo_id})


# Поиск фото
# => Принимает vk_id 
# => Возращает список из трех самых популярный фото ['фото1', 'фото2', 'фото3']

def get_photo(user_id, owner_id, mode):
	vk_user = vk_api.VkApi(token=session.query(User).filter_by(vk_id_user=user_id).first().token)
	# Получаем фото
	try:
		response = vk_user.method('photos.get',
								  {
									  'access_token': session.query(User).filter_by(vk_id_user=user_id).first().token,
									  'owner_id': owner_id,
									  'album_id': 'profile',
									  'count': 10,
									  'extended': 1,
									  'photo_sizes': 1,
								  })
	except ApiError:
		return 'Нет доступа к фото🥺'
	# Формируем черновой список фото
	users_photos = []
	for i in range(10):
		try:
			users_photos.append(
				[response['items'][i]['likes']['count'],
				 'photo' + str(response['items'][i]['owner_id']) + '_' + str(response['items'][i]['id']),
				 str(response['items'][i]['id'])])
		except IndexError:
			pass
	# Сортируем фото по лайкам и отдаем 3 лучших фото
	if mode == 'photo':
		sort_users_photos = sorted(users_photos, reverse=True)
		sort2_users_photos = []
		counter = 0
		for element in sort_users_photos:
			if counter == 3:
				break
			sort2_users_photos.append(element[1])
			counter += 1
		return sort2_users_photos
	else:
		return users_photos[0][2]  # В нулевом элементе хранится аватарка.
