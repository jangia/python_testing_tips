import requests
from http import HTTPStatus


def test_default_assertion_message():
    user = {"email": "<EMAIL>", "is_happy": False}
    assert user["is_happy"] is True
    # >       assert user["is_happy"] is True
    # E       assert False is True


def test_custom_assertion_message():
    user = {"email": "<EMAIL>", "is_happy": False}
    assert user["is_happy"] is True, "Failure: user is not happy!"
    # >       assert user["is_happy"] is True, "Failure: user is not happy!"
    # E       AssertionError: Failure: user is not happy!
    # E       assert False is True


def test_weather_api_bad_request_with_default_assertion_message():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": "London"}

    response = requests.get(url, params=params)

    assert response.status_code == HTTPStatus.OK
    # >       assert response.status_code == HTTPStatus.OK
    # E       assert 401 == <HTTPStatus.OK: 200>
    # E        +  where 401 = <Response [401]>.status_code
    # E        +  and   <HTTPStatus.OK: 200> = HTTPStatus.OK


def test_weather_api_bad_request_with_custom_assertion_message():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": "London"}

    response = requests.get(url, params=params)

    assert response.status_code == HTTPStatus.OK, response.text
    # >       assert response.status_code == HTTPStatus.OK, response.text
    # E       AssertionError: {"cod":401, "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."}
    # E       assert 401 == <HTTPStatus.OK: 200>
    # E        +  where 401 = <Response [401]>.status_code
    # E        +  and   <HTTPStatus.OK: 200> = HTTPStatus.OK
