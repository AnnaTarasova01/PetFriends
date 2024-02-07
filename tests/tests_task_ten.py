import pytest
import os
from requests_toolbelt import MultipartEncoder
import requests
import re
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_no_email(email="", password=valid_password):
    """Проверка на корректно введный логин. При отсутствии или неверно указанного логина выводится ошибка"""
    email = valid_email
    if email == valid_email:
        status, result = pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result
    else:
        raise ValueError("Неверный логин")


def test_no_password(email=valid_email, password=""):
    """Проверка на корректно введный пароль. При отсутствии или неверно указанного пароля выводится ошибка"""
    password = valid_password
    if password == valid_password:
        status, result = pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result
    else:
        raise ValueError("Неверный пароль")


def test_no_name(name="", animal_type="", age=""):
    """Проверка на добавление питомца без имени. Выводится ошибка если поле name пустое"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    if not name:
        print("Введите имя питомца")
    else:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

def test_name_not_int(name="Гоша", animal_type="", age=""):
    """Проверка ввода имени. Если в имени присутствую цифры, то выводится ошибка"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    if re.search(r'\d', name):
        print("Недопустимые символы. Введите имя питомца")
    else:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

def test_no_animal_type(name="", animal_type="", age=""):
    """Проверка ввода вида животного. При пустом поле возвращается ошибка"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    if not animal_type:
        print("Введите вид питомца")
    else:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert result['animal_type'] == animal_type



def test_not_int_animal_type(name="", animal_type="собака", age=""):
    """Проверка вода вида животного. Если строка содержит цифры, взвращается ошибка"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    if re.search(r'\d', animal_type):
        print("Недопустимые символы. Введите вид питомца")
    else:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert 'id' in result


def test_no_age(name="", animal_type="", age='-1'):
    """Проверка на ввод возраст питомца. Если поле пустое возвращается ошибка"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    if not age:
        print("Введите возраст питомца")
    else:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert 'id' in result


def test_age_int(name='', animal_type='', age='1'):
        """Проверка на ввод возраста. Строка должна содержать только цифры и не может быть отрицательной"""
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        if not any(char.isdigit() for char in age):
            print("Недопустимые символы. Введите возраст питомца")
        elif int(age) < 0:
            print("Недопустимые символы. Введите возраст питомца")
        else:
            status, result = pf.add_new_pet(auth_key, name, animal_type, age)
            assert status == 200
            assert 'id' in result


def test_jpg_photo(pet_photo='images/dog.pdf'):
    """Проверка добавления корректного расширения фото.  Если фото не .jpg или .png возвращается ошибка"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_pf_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    pet_photo_ext = pet_photo.split('.')[-1]  # Получаем расширение файла
    if pet_photo_ext in ['jpg', 'png']:
        pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = pf.add_photo(auth_key, pet_id, pet_photo_path)
        assert status == 200
        assert result.get('pet_photo') is not None
    else:
        print('Неверный формат. Допустимый формат фото .jpg и .png')


def test_no_delete_pets_not_my_list(name='', animal_type='', age=''):
    """Проверка удаления питомца с неверным id. Если питомца в списке нет возвращается ошибка"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_pf_pets(auth_key, 'my_pets')
    pet_id = "Не верный id питомца"
    pet_ids = [pet['id'] for pet in my_pets['pets']]
    if pet_id in pet_ids:
        status, _ = pf.delete_pet(auth_key, pet_id, name, animal_type, age)
        assert status == 200
    else:
        print("Питомца нет в Вашем списке")
