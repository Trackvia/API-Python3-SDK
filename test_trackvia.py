import time
import pytest
from trackviapy3 import TrackVia

tv = TrackVia("", "")

# Test Vars
vars = {
    'view_id': 47,
    'record_id': 0,
    'email': ''
}

# Begin tests
def test_get_all_apps():
    res = tv.get_all_apps()
    assert len(res) > 0

def test_get_all_views():
    res = tv.get_all_views()
    assert len(res) > 0

def test_get_view():
    res = tv.get_view(vars['view_id'])
    assert 'structure' in res
    assert 'data' in res

def test_get_all_records():
    res = tv.get_all_records(vars['view_id'])
    assert 'structure' in res
    assert 'data' in res

def test_create_record():
    data = [{
        'Single Line': 'test',
        'Paragraph': 'test',
        'Number': 1,
        'Percentage': 1,
        'Currency': 1.00
    }]
    res = tv.create_record(vars['view_id'], data)
    assert 'structure' in res
    assert 'data' in res

    #save record id for later
    vars['record_id'] = int(res['data'][0].get('Record ID'))

def test_get_record():
    res = tv.get_record(vars['view_id'], vars['record_id'])
    assert 'structure' in res
    assert 'data' in res

def test_update_record():
    data = [{
        'Single Line': 'test123',
        'Paragraph': 'test123',
        'Number': 11,
        'Percentage': 1.1,
        'Currency': 1.01
    }]
    res = tv.update_record(vars['view_id'], vars['record_id'], data)

    single_line = res['data'][0]['Single Line']
    assert data[0]['Single Line'] == single_line

    paragram = res['data'][0]['Paragraph']
    assert data[0]['Paragraph'] == paragram

    number = int(res['data'][0]['Number'])
    assert data[0]['Number'] == number

    Percentage = float(res['data'][0]['Percentage'])
    assert data[0]['Percentage'] == Percentage

    currency = float(res['data'][0]['Currency'])
    assert data[0]['Currency'] == currency

def test_delete_record():
    res = tv.delete_record(vars['view_id'], vars['record_id'])
    assert "" is res

def test_get_users():
    res = tv.get_users()
    assert 'structure' in res
    assert 'data' in res

def test_create_user():
    timestamp = int(time.time())
    email = "{email}+{timestamp}@trackvia.com".format(email=vars['email'], timestamp=timestamp)
    first_name = 'Test'
    last_name = 'User'
    timezone = 'America/Denver'

    res = tv.create_user(email=email, first_name=first_name, last_name=last_name, timezone=timezone)
    assert 'structure' in res
    assert 'data' in res