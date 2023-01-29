import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError


# База данных подключение 
Base = declarative_base()
engine = sq.create_engine('postgresql://user@localhost:5432/vkinder_db', client_encoding='utf8')
Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()



# Классы и функции для работы с базой
#_______________________________________________________

# Пользователь
#_______________________________________________________

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
def check_db_master(vk_id):
    current_user_id = session.query(User).filter_by(vk_id_user=vk_id).first()
    if current_user_id == vk_id:
        return True
    else:
        return False

# Регистрация пользователя
def register_user(vk_id_user, name, surname, age, sex, city):
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

# Избранное
#_______________________________________________________

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

# Черный список
#_______________________________________________________

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