import vk_api
from vk_conf import user_token
from vk_conf import group_token
from vk_api.exceptions import ApiError
from pprint import pprint

# Вконтакте
# Не забудь указать vk_user в vk_conf
vk_group = vk_api.VkApi(token=group_token)
vk_user = vk_api.VkApi(token=user_token)



# Поиск партнеров => список людей Имя, Фамилия, ссылка, id

def search_users(sex, age_at, age_to, city):
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
        people = [
            element['first_name'],
            element['last_name'],
            basic_link + str(element['id']),
            element['id']
        ]
        suitable_people.append(people)
    return suitable_people

# поиск фото => список из трех самых популярных фото
def get_photo(user_id):
    # Получаем фото
    basic_link = 'https://vk.com/'
    try:
        response = vk_user.method('photos.get',
                              {
                                  'access_token': user_token,
                                  'owner_id': user_id,
                                  'album_id': 'profile',
                                  'count': 10,
                                  'extended': 1,
                                  'photo_sizes': 1,
                              })
    except ApiError:
        return 'нет доступа к фото'
    # Формируем черновой список фото
    users_photos = []
    for i in range(10):
        try:
            users_photos.append(
                [response['items'][i]['likes']['count'],
                 str(basic_link) + 'photo' + str(response['items'][i]['owner_id']) + '_' + str(response['items'][i]['id'])])
        except IndexError:
            users_photos.append([0, 'нет фото.'])
    # Сортируем фото по лайкам и отдаем 3 лучших фото
    sort_users_photos = sorted(users_photos, reverse=True)
    sort2_users_photos = []
    sort2_users_photos.append(sort_users_photos[0])
    sort2_users_photos.append(sort_users_photos[1])
    sort2_users_photos.append(sort_users_photos[2])
    return sort2_users_photos


