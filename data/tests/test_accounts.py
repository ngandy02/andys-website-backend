import data.accounts as acc
import pytest

TEST_EMAIL = "an3299@nyu.edu"
TEST_NAME = "Andy Ng"

TEMP_EMAIL = "allnng222@yahoo.com"
TEMP_NAME = "Allen Ng"

def test_is_valid_email():
    result = acc.is_valid_email(TEST_EMAIL) 
    assert result is True


def test_is_valid_name():
    result = acc.is_valid_name(TEST_NAME)
    assert result is True


@pytest.fixture(scope="function")
def temp_account():
    email = acc.register(TEMP_NAME, TEMP_EMAIL)
    yield email
    try:
        acc.delete_account(email)
    except:
        print("Account already deleted.")


# create test
def test_register(temp_account):
    # result = acc.register(TEST_NAME, TEST_EMAIL)
    assert TEMP_EMAIL == temp_account
    assert acc.account_exists(TEMP_EMAIL)
    assert acc.account_exists(temp_account)
    account = acc.get_account(temp_account)
    assert TEMP_EMAIL == account[acc.EMAIL]
    assert TEMP_NAME == account[acc.NAME]


# read all test
def test_read_accounts(temp_account):
    result = acc.read_accounts()
    if len(result) == 0:
        print("Accounts database is empty")
        return
    print(result)
    for key, value in result.items():
        assert acc.EMAIL and acc.NAME in value
        assert isinstance(key, str)
    assert temp_account in result
    assert TEST_EMAIL in result
    assert TEST_NAME in result[TEST_EMAIL][acc.NAME]
    assert "Allen Ng" in result["allnng222@yahoo.com"][acc.NAME]


# read one test 
def test_read_one_account(temp_account):
    account = acc.get_account(temp_account)
    print(account)
    assert account[acc.EMAIL] == temp_account
    assert account[acc.NAME] == TEMP_NAME
    for key, value in account:
        assert isinstance(key, str)
        assert isinstance(value, str)


    

