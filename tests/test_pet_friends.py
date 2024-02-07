from typing import Any, Union

from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_pf_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) !=0


def test_add_new_pet(name='Тита', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)
    assert status == 200
    assert 'id' in result


def test_add_photo(pet_photo='images/dog.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_pf_pets(auth_key, 'my_pets')
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo(auth_key, pet_id, pet_photo)
        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception('No pets')


def test_update_information(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_pf_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.uptade_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('No pets')


def test_delete_pet(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_pf_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id, name, animal_type, age)
    assert status == 200
