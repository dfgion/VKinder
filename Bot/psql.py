import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError

# База данных подключение 
Base = declarative_base()
DSN = 'postgresql://__@localhost:5432/vkinder_db'
engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()


# ****** Классы и функции для работы с базой ******


# _____Пользователь_____

# Класс создания таблицы пользователя бота

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
			vk_id_user=vk_id_user,
			name=name,
			surname=surname,
			age=age,
			sex=sex,
			city=city,
			token=user_token
		)
		session.add(new_user)
		session.commit()
		return True
	except (IntegrityError, InvalidRequestError):
		return False


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
    all_favorite = session.query(FavUser.fav_vk_id, FavUser.name, FavUser.surname, FavUser.link).filter_by(vk_id_user=current_users_id.vk_id_user).all()
    return all_favorite

def delete_favourite(fav_vk_id):
    current_user = session.query(FavUser).filter_by(fav_vk_id=fav_vk_id).first()
    session.delete(current_user)
    session.commit()

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
	if len(link_photo) > 0:
		link_photo = ', '.join(link_photo)
		try:
			new_user = Photos_FavUser(
				link_photo=link_photo,
				fav_vk_id=fav_vk_id
			)
			session.add(new_user)
			session.commit()
			return
		except (IntegrityError, InvalidRequestError):
			return
	else:
		return


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


def delete_black_list(bl_vk_id):
    current_user = session.query(BlackList).filter_by(bl_vk_id=bl_vk_id).first()
    session.delete(current_user)
    session.commit()

# Добавление пользователя в ЧС
# => Принимает bl_vk_id, name, surname, link, vk_id_user
# => Возвращает True если добавление прошло успешно или False если пользователь уже есть в ЧС
def add_user_black_list(bl_vk_id, name, surname, link, vk_id_user):
	try:
		new_user = BlackList(
			bl_vk_id=bl_vk_id,
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


# Получение пользователей в ЧС
# => Принимает vk_id_user
# => Возвращает все добавленные анкеты пользователем в ЧС
def check_black_list(vk_id_user):
    current_users_id = session.query(User).filter_by(vk_id_user=vk_id_user).first()
    all_black_list = session.query(BlackList.bl_vk_id, BlackList.name, BlackList.surname, BlackList.link).filter_by(vk_id_user=current_users_id.vk_id_user).all()
    return all_black_list

# Класс создания таблицы фото черного списка
class Photos_BlackList(Base):
	__tablename__ = 'black_list_photos'
	id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
	link_photo = sq.Column(sq.String)
	bl_vk_id = sq.Column(sq.Integer, sq.ForeignKey('black_list.bl_vk_id', ondelete='CASCADE'))


def create_tables(engine):
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)
