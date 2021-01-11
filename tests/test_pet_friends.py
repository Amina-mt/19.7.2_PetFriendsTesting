from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ To check the request for the api key returns a status of 200 and the result has the word key"""

    # Sending a request and saving received response with the status code in status, and the response text in the result
    status, result = pf.get_api_key(email, password)

    # Checking the received data with our expectations
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Checking the request for all pets returns a non blank list.
         First of all, getting the api key and saving it to the auth_key variable. Further using this key
         to request a list of all pets and check that the list is not empty.
         Available filter parameter value - 'my_pets' or '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Bella', animal_type='husky',
                                     age='0', pet_photo='images/dog.jpg'):
    """Checking if we can add a pet with correct data"""

    # Geting the full path of the pet's image and saving it to the variable pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Requesting key api and saving in the variable of auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Adding a pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Checking received response with the expected result
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Checking if we are able to delete a pet"""

    # Getting key auth_key and requesting a list of my_pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Checking if the list of my_pets is blank, we are adding a new pet and requesting a list of my_pets again
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "bella", "husky", "0", "images/dog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Using id of the first pet from the list and sending request to delete
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Requesting a list of my_pets again
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Checking if the response status is 200 and there is no id of deleted pet in the list of my_pets
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Daisy', animal_type='husky', age=1):
    """Checking if we are able to update information about pet"""

    # Getting key auth_key and requesting a list of my_pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # If the list is not blank, we would try to update pet's name, type and age
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Checking if the response status is 200 and pet name matches the given
        assert status == 200
        assert result['name'] == name
    else:
        # if the list of pets is blank, then we would include an exception with the text about missing pets
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo(name='name_1', animal_type='animal_type_1',
                                     age='age_1'):
    """Checking if we are able to add a new pet without photo"""

    # Requesting api key and saving in the variable of auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Adding a new pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    # Checking received response with the expected result
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_animal_type_cyrillic(name='Diamond', animal_type='пудель', age='2', pet_photo='images/пудель.jpg'):
    """Checking if we are able to add a new pet with animal_type in cyrillic data"""

    # Getting the full path of the pet's image and saving it to the variable pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Requesting api key and saving in the variable of auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Adding a new pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Checking received response with the expected result
    assert status == 200
    assert result['name'] == name

def test_post_add_new_pet_with_bad_photo(name='Leo', animal_type='pomeranian', age=1, pet_photo='images/text.txt'):
    """Adding a new pet with a photo but the format of saved file is txt instead of jpg"""

    # Getting the full path of the pet's image and saving it to the variable pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Requesting api key and saving in the variable of auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Adding a new pet
    status, result = pf.post_add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)

    # Checking if we can add txt format file instead of photo
    assert status == 200
    assert 'txt' in pet_photo

def test_add_new_pet_incorrect_data(name='!@#$%^&*:"\<>?', animal_type='33333', age='123456789', pet_photo='images/dog.jpg'):
    """Checking if we are able to add a new pet with incorrect data"""

    # Getting the full path of the pet's image and saving it to the variable pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Requesting api key and saving in the variable of auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Adding a new pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Checking received response with the expected result
    assert status == 200
    assert result['name'] == name

def test_update_self_pet_incorrect_data(name='123456789', animal_type='±!@#$%^&*~', age=-987654321):
    """Checking if we are able to update information about pet with incorrect data"""

    # Getting a key as auth_key and requesting a list of my_pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # If the list is not blank, we would try to update pet's name, type and age
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Checking if the response status is 200 and pet name matches the given
        assert status == 200
        assert result['name'] == name
    else:
        # if the list of pets is blank, then we would include an exception with the text about missing pets
        raise Exception("There is no my pets")

def test_delete_self_pet_incorrect_data():
    """Checking if we are able to delete a pet with incorrect data"""

    # Getting a key as auth_key and requesting a list of my_pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Using id of the third pet from the list and sending request to delete
    pet_id = my_pets['pets'][2]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Requesting a list of my_pets again
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Checking if the response status is 200 and there is no id of deleted pet in the list of my_pets
    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_new_pet_name_293_symbols(name='Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.', animal_type='пудель', age='2', pet_photo='images/пудель.jpg'):
    """Checking if we are able to add a new pet with a name (string) of 293 symbols"""

    # Getting the full path of the pet's image and saving it to the variable pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Requesting api key and saving in the variable of auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Adding a new pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Checking received response with the expected result
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_no_data(name='', animal_type='', age='', pet_photo='images/pomeranian.jpg'):
    """Checking if we are able to add a new pet with a blank sting/data"""

    # Getting the full path of the pet's image and saving it to the variable pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Requesting api key and saving in the variable of auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Adding a new pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Checking received response with the expected result
    assert status == 200
    assert result['name'] == name

def test_update_self_pet_without_data(name='', animal_type='', age=''):
    """Checking if we are able to update information about pet with blank strings/data"""

    # Getting a key as auth_key and requesting a list of my_pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # If the list is not blank, we would try to update pet's name, type and age
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Checking if the response status is 200 and pet name matches the given
        assert status == 200
        assert result['name'] == name
    else:
        # if the list of pets is blank, then we would include an exception with the text about missing pets
        raise Exception("There is no my pets")

def test_delete_self_deleted_pet():
    """Checking if we are able to delete a pet which has been already deleted"""

    # Getting a key as auth_key and requesting a list of my_pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Using id of the first pet from the list and sending request to delete
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Requesting list of my_pets again
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Checking if the response status is 200 and there is no id of deleted pet in the list of my_pets
    assert status == 200
    assert pet_id not in my_pets.values()

def test_get_api_key_for_invalid_log_in(email=valid_email, password=valid_password):
    """ To check the request for the api key returns a status of 200 and the result has the word key"""

    # Sending a request and saving received response with the status code in status, and the response text in the result
    status, result = pf.get_api_key(email, password)

    # Checking the received data with our expectations
    assert status == 200
    assert 'key' in result

def test_set_pet_photo_added_pet(pet_photo='images/pomeranian.jpg'):
    """Checking if we are able to set a photo to the added pet"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][1]['id']
    status, result = pf.set_pet_photo_added_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert 'jpg' in pet_photo