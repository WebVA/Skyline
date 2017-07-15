import pytest

from skylines.schemas import UserSchema


@pytest.fixture
def schema():
    return UserSchema()


@pytest.fixture
def partial_schema():
    return UserSchema(partial=True)


@pytest.fixture
def callsign_schema():
    return UserSchema(only=('trackingCallsign',))


@pytest.fixture
def delay_schema():
    return UserSchema(only=('trackingDelay',))


def test_deserialization_skips_id(partial_schema):
    data, errors = partial_schema.load(dict(id=6))
    assert not errors
    assert 'id' not in data


def test_deserialization_passes_for_valid_email(schema):
    data, errors = schema.load(dict(email='john@doe.com'))
    assert not errors
    assert data.get('email_address') == 'john@doe.com'


def test_deserialization_fails_for_empty_email(schema):
    data, errors = schema.load(dict(email=''))
    assert 'email' in errors
    assert 'Not a valid email address.' in errors.get('email')


def test_deserialization_passes_for_valid_callsign(callsign_schema):
    data, errors = callsign_schema.load(dict(trackingCallsign='TH'))
    assert not errors
    assert data.get('tracking_callsign') == 'TH'


def test_deserialization_passes_for_missing_callsign(callsign_schema):
    data, errors = callsign_schema.load(dict())
    assert not errors
    assert data.get('tracking_callsign') == None


def test_deserialization_passes_for_empty_callsign(callsign_schema):
    data, errors = callsign_schema.load(dict(trackingCallsign=''))
    assert not errors
    assert data.get('tracking_callsign') == ''


def test_deserialization_passes_for_stripped_callsign(callsign_schema):
    data, errors = callsign_schema.load(dict(trackingCallsign='TH           '))
    assert not errors
    assert data.get('tracking_callsign') == 'TH'


def test_deserialization_fails_for_long_callsign(callsign_schema):
    data, errors = callsign_schema.load(dict(trackingCallsign='12345890'))
    assert 'trackingCallsign' in errors
    assert 'Longer than maximum length 5.' in errors.get('trackingCallsign')


def test_deserialization_passes_for_valid_delay(delay_schema):
    data, errors = delay_schema.load(dict(trackingDelay=5))
    assert not errors
    assert data.get('tracking_delay') == 5


def test_deserialization_passes_for_valid_delay_string(delay_schema):
    data, errors = delay_schema.load(dict(trackingDelay='10'))
    assert not errors
    assert data.get('tracking_delay') == 10


def test_deserialization_fails_for_invalid_delay(delay_schema):
    data, errors = delay_schema.load(dict(trackingDelay=-1))
    assert 'trackingDelay' in errors
    assert 'Must be between 0 and 60.' in errors.get('trackingDelay')