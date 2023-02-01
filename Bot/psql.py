import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError

# База данных подключение 
Base = declarative_base()
DSN = 'postgresql://postgres:jjUUhy23@localhost:5432/vkinder_db'
engine = sq.create_engine(DSN)
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
    token = sq.Column(sq.String, unique=True)

# Проверка регистрации пользователя в БД 
# => Принимает vk_id 
# => Возращает True или False

def registr_info(vk_id):
    current_user_id = session.query(User).filter_by(vk_id_user=vk_id).first()
    if current_user_id:
        if current_user_id.vk_id_user == vk_id:
            return True
    return False

# Регистрация пользователя 
# => Принимает vk_id_user, name, surname, age, sex, city   
# => Возвращает True если регистрация прошла успешно или False если что то пошло не так

def registration(vk_id_user, name, surname, age, sex, city, user_token):
    try:
        new_user = User(
            vk_id_user = vk_id_user,
            name = name,
            surname = surname,
            age = age, 
            sex = sex,
            city = city,
            token = user_token
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False

# _____Избранное_____

# Класс создания таблицы избранных пользователей
class DatingUser(Base):
    __tablename__ = 'favourite'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    fav_vk_id = sq.Column(sq.Integer, unique=True)
    name = sq.Column(sq.String)
    surname = sq.Column(sq.String)
    link = sq.Column(sq.String)
    vk_id_user = sq.Column(sq.Integer, sq.ForeignKey('bot_user.vk_id_user', ondelete='CASCADE'))



# Класс создания таблицы фото избранных пользователей
class Photos_DatingUser(Base):
    __tablename__ = 'favourite_photos'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    fav_vk_id = sq.Column(sq.Integer, sq.ForeignKey('favourite.fav_vk_id', ondelete='CASCADE'))

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

def create_tables(engine):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
