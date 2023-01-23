import pytest
import requests
import json


@pytest.fixture
def supply_url():
    return 'https://reqres.in/api'


@pytest.mark.parametrize("userid, firstname", [(1, "George"), (2, "Janet")])
def test_list_valid_user(supply_url, userid, firstname):
    url = supply_url + "/users/" + str(userid)
    resp = requests.get(url)
    j = json.loads(resp.text)

    assert resp.status_code == 200, resp.text
    assert j['data']['id'] == userid, resp.text
    assert j['data']['first_name'] == firstname, resp.text


def test_list_invalid_user(supply_url):
    url = supply_url + "/users/50"
    resp = requests.get(url)

    assert resp.status_code == 404, resp.text


def test_login_valid(supply_url):
    url = supply_url + "/login/"
    data = {'email': 'test@test.com', 'password': 'something'}
    resp = requests.post(url, data=data)
    j = json.loads(resp.text)

    assert resp.status_code == 200, resp.text
    assert j['token'] == "QpwL5tke4Pnpja7X", resp.text


def test_login_no_password(supply_url):
    url = supply_url + "/login/"
    data = {'email': 'test@test.com'}
    resp = requests.post(url, data=data)
    j = json.loads(resp.text)

    assert resp.status_code == 400, resp.text
    assert j['error'] == "Missing password", resp.text


def test_login_no_email(supply_url):
    url = supply_url + "/login/"
    data = {}
    resp = requests.post(url, data=data)
    j = json.loads(resp.text)

    assert resp.status_code == 400, resp.text
    assert j['error'] == "Missing email or username", resp.text
