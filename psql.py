import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError


# База данных подключение 
Base = declarative_base()
engine = sq.create_engine('postgresql://user@localhost:5432/vkinder_db', client_encoding='utf8')
Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()



# ****** Классы и функции для работы с базой ******


# _____Пользователь_____

#Класс создания таблицы пользователя бота

class User(Base):
    __tablename__ = 'bot_user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id_user = sq.Column(sq.Integer, unique=True)
    name = sq.Column(sq.String)
    surname = sq.Column(sq.String)
    age = sq.Column(sq.String)
    sex = sq.Column(sq.String)
    city = sq.Column(sq.String)

# Проверка регистрации пользователя в БД 
# => Принимает vk_id 
# => Возращает True или False

def registr_info(vk_id):
    current_user_id = session.query(User).filter_by(vk_id_user=vk_id).first()
    if current_user_id.vk_id_user == vk_id:
        return True
    else:
        return False

# Регистрация пользователя 
# => Принимает vk_id_user, name, surname, age, sex, city   
# => Возвращает True если регистрация прошла успешно или False если что то пошло не так

def registration(vk_id_user, name, surname, age, sex, city):
    try:
        new_user = User(
            vk_id_user = vk_id_user,
            name = name,
            surname = surname,
            age = age, 
            sex = sex,
            city = city
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False

# _____Избранное_____

# Класс создания таблицы избранных пользователей
class FavUser(Base):
    __tablename__ = 'favourite'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    fav_vk_id = sq.Column(sq.Integer, unique=True)
    name = sq.Column(sq.String)
    surname = sq.Column(sq.String)
    link = sq.Column(sq.String)
    vk_id_user = sq.Column(sq.Integer, sq.ForeignKey('bot_user.vk_id_user', ondelete='CASCADE'))

# Добавление пользователя в избранное
# => Принимает fav_vk_id, name, surname, link, vk_id_user
# => Возвращает True если добавление прошло успешно или False если пользователь уже есть в избранном
def add_user_favourite(fav_vk_id, name, surname, link, vk_id_user):
    try:
        new_user = FavUser(
            fav_vk_id=fav_vk_id,
            name=name,
            surname=surname,
            link=link,
            vk_id_user=vk_id_user
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False

# Получение пользователей в избранном
# => Принимает vk_id_user
# => Возвращает все добавленные анкеты пользователем в избранное
def check_favourite(vk_id_user):
    current_users_id = session.query(User).filter_by(vk_id_user=vk_id_user).first()
    all_favorite = session.query(FavUser).filter_by(vk_id_user=current_users_id.vk_id_user).all()
    return all_favorite


# Класс создания таблицы фото избранных пользователей
class Photos_FavUser(Base):
    __tablename__ = 'favourite_photos'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    fav_vk_id = sq.Column(sq.Integer, sq.ForeignKey('favourite.fav_vk_id', ondelete='CASCADE'))

# Сохранение в БД фото избранного пользователя
# => Принимает link_photo, fav_vk_id
# => Возвращает True если добавление прошло успешно или False если фото уже есть 
def add_user_favourite_photos(link_photo, fav_vk_id):
    try:
        new_user = Photos_FavUser(
            link_photo=link_photo,
            fav_vk_id=fav_vk_id
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False

# Получение фото пользователей в избранном
# => Принимает fav_vk_id
# => Возвращает фото добавленные к анкете в избранном
def check_favourite_photos(fav_vk_id):
    curren_fav_users_id = session.query(FavUser).filter_by(fav_vk_id=fav_vk_id).first()
    all_favorite_photos = session.query(Photos_FavUser).filter_by(fav_vk_id=curren_fav_users_id.fav_vk_id).all()
    return all_favorite_photos


# _____Черный список_____

# Класс создания таблицы черного списка
class BlackList(Base):
    __tablename__ = 'black_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    bl_vk_id = sq.Column(sq.Integer, unique=True)
    name = sq.Column(sq.String)
    surname = sq.Column(sq.String)
    link = sq.Column(sq.String)
    vk_id_user = sq.Column(sq.Integer, sq.ForeignKey('bot_user.vk_id_user', ondelete='CASCADE'))

# Класс создания таблицы фото черного списка
class Photos_BlackList(Base):
    __tablename__ = 'black_list_photos'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    bl_vk_id = sq.Column(sq.Integer, sq.ForeignKey('black_list.bl_vk_id', ondelete='CASCADE'))