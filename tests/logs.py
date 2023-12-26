import os.path
import pprint
import logging
from faker import Faker
import allure
import pytest
import requests

faker = Faker()
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'logs_api.log')

def configure_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

base_logger = configure_logger('base_request_logger', log_file)

class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, data=data)
            elif request_type == 'PUT':
                response = requests.put(url, data=data)
            else:
                response = requests.delete(url)

            if not expected_error and response.status_code == 200:
                stop_flag = True
            elif expected_error:
                stop_flag = True

        pprint.pprint(f'{request_type} example')
        pprint.pprint(response.url)
        pprint.pprint(response.status_code)
        pprint.pprint(response.reason)
        pprint.pprint(response.text)
        pprint.pprint(response.json())
        pprint.pprint('**********')
        return response

    def get(self, endpoint, expected_error=False):
        url = f'{self.base_url}/{endpoint}'
        response = self._request(url, 'GET', expected_error=expected_error)
        return response.json()

    def post(self, endpoint, body):
        url = f'{self.base_url}/{endpoint}'
        response = self._request(url, 'POST', data=body)
        return response.json()['message']

    def put(self, endpoint, endpoint_id, body):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'PUT', data=body)
        return 'Updated'

    def delete(self, endpoint, endpoint_id):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        return 'Deleted'
    

BASE_URL = 'https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev'
base_request = BaseRequest(BASE_URL)


#Запросы

def get_req(essence):
    essence_info = base_request.get(essence)
    pprint.pprint(essence_info)
    base_logger.info(essence_info)

get_req('birds')

def post_req(essence, data):
    essence_info = base_request.post(essence, json=data)
    pprint.pprint(essence_info.json())
    base_logger.info(essence_info)

data = {
      "id": 3,
      "species": "Elephant",
      "habitat": "Savannah",
      "average_lifespan": 60
    }

#post_req('animals', data)



def put_req(essence, id, data):
    essence_id = base_request.put(f'{essence}', id, data)
    pprint.pprint(essence_id)
    base_logger.info(essence_id)



def delete_req(essence, id):
    deleted_essence = base_request.delete(f'{essence}', id)
    pprint.pprint(deleted_essence)
    base_logger.info(deleted_essence)

# delete_req('animals',3)



@allure.feature('Add new animal')
@allure.story('Провека на то, что новое животное добавилось в db.json')
def test_similarName():
    user_info = base_request.get('animals', 2)
    assert dataToUpdAnimal["name"] == user_info["name"]
    pass


@allure.feature('Arr length')
@allure.story('Проверка на то, сколько зарегистрированно птиц')
def test_value():
    posts = requests.get('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/birds')
    assert 3 == len(posts.json())


@allure.feature('Delete animal')
@allure.story('Проверка удаления животного из db.json')
def test_deletedData():
    response = requests.get('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/animals')
    animals = response.json()
    animals_sp = [animals["species"] for animal in animals]
    assert "Tiger" not in animals_sp


@allure.feature('Get fish name')
@allure.story('Проверка получения вида конкретной рыбы')
@pytest.mark.parametrize('studioID', [1, 2, 3])
def test_getStudio(fishID):
    response = requests.get(f'https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/fish/{fishID}')

    fish = response.json()
    fishName = fish["species"]

    assert response.status_code == 200

    print(f"Studio #{fishID}: {fishName}")


@allure.feature('Check 200 status')
@allure.story('Проверка наличия статуса 200 после получения всех ящериц / проверка наличия ящериц с определённым id')
@pytest.mark.parametrize('lizardID', [1, 2, 3])
def test_checkStatus(lizardID):
    response = requests.get(f'https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/lizards/{lizardID}')
    assert response.status_code == 200


@allure.feature('Check this horse')
@allure.story('Проверка есть ли тот или иной автор')
def test_similarPosts():
    response = requests.get('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/horses')
    horses = response.json()
    found = False
    for horse in horses:
        if horse["species"] == "Thoroughbred":
            found = True
            break
    assert found, "Horse 'Thoroughbred' not found in the response"


@allure.feature('Count data < 5')
@allure.story('Проверка на то, действительно ли кол-во ящериц меньше 5')
def test_value():
    response = requests.get('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/lizards')
    assert len(response.json()) < 5

@allure.feature('Check delete data')
@allure.story('проверка удаления данных')
def test_delete():
    response = requests.delete('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/horse')
    assert len(response.json()) == 0

@allure.feature('Having photos')
@allure.story('есть ли зона обитания у животного')
def test_photoProfile():
    response = requests.get('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/animals')
    animals = response.json()
    for animal in animals:
        assert "habitat" not in animal, "Habitat not found in animals"


@allure.feature('Check this course')
@allure.story('Проверка есть ли тот или вид')
def test_similarPosts():
    response = requests.get('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/fish')
    fish = response.json()
    found = False
    for fi in fish:
        if fi["species"] == "Salmon":
            found = True
            break
    assert found, "Not found in the response"


@allure.feature('Get info about this horse')
@allure.story('Проверка получения данных конкретных лошадей')
@pytest.mark.parametrize('userID', [1, 2, 3])
def test_getStudio(horseID):
    response = requests.get(f'https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/horses/{horseID}')

    horses = response.json()

    assert response.status_code == 200

    print(f"Studio #{horseID}: {horses}")



@allure.feature('having this word')
@allure.story('есть ли слово Forest в зоне обитания ящериц')
def test_photoProfile():
    response = requests.get('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/lizards')
    lizards = response.json()
    liz_info = [liz["habitat"] for liz in lizards]
    assert "Forest" not in liz_info


@allure.feature('Get lizard Iguana')
@allure.story('есть ли ящерица Iguana')
def test_photoProfile():
    response = requests.get('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/lizards')
    lizards = response.json()
    for lizard in lizards:
        assert "Iguana" not in lizard, "Lizard not found in data"

@allure.feature('horse count > 0')
@allure.story('Проверка на то, действительно ли кол-во лощадей больше 0')
def test_userValue():
    response = requests.get('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/horses')
    assert len(response.json()) > 0


@allure.feature('Delete all data in fish')
@allure.story('проверка удаления данных в fish')
def test_userDelete():
    response = requests.delete('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/fish')
    assert len(response.json()) == 0

@allure.feature('Get info about this course')
@allure.story('Проверка получения данных конкретных животных')
@pytest.mark.parametrize('animalID', [1, 2, 3])
def test_getDesignCourseInfo(animalID):
    response = requests.get(f'https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/animals/{animalID}')

    animal = response.json()

    assert response.status_code == 200

    print(f"Studio #{animalID}: {animal}")

@allure.feature('Get lizard Gecko')
@allure.story('есть ли ящерица Gecko')
def test_checkUserName():
    response = requests.get('https://super-duper-space-eureka-jj566wggwgrcj5rj-3000.app.github.dev/lizards')
    lizards = response.json()
    for lizard in lizards:
        assert "Gecko" not in lizard, "Lizard not found in data"
