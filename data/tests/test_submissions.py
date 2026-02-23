import data.submission as sub
import pytest

TEST_EMAIL = "an3299@nyu.edu"
TEST_NAME = "Andy Ng"

TEMP_EMAIL = "allnng222@yahoo.com"
TEMP_NAME = "Allen Ng"

INVALID_EMAIL = "hello"
NONEXISTENT_EMAIL = "ngandy0202@gmail.com"

def test_is_valid_email():
    result = sub.is_valid_email(TEST_EMAIL) 
    assert result is True


def test_is_valid_name():
    result = sub.is_valid_name(TEST_NAME)
    assert result is True


def test_email_already_exists():
    with pytest.raises(ValueError):
        sub.register("Andrew Chen", TEST_EMAIL)
    

def test_invalid_email():
    with pytest.raises(ValueError):
        sub.is_valid_email(INVALID_EMAIL)


def test_delete_nonexistent_submission():
    with pytest.raises(KeyError):
        sub.delete_submission(NONEXISTENT_EMAIL)


@pytest.fixture(scope="function")
def temp_submission():
    email = sub.register(TEMP_NAME, TEMP_EMAIL)
    yield email
    try:
        sub.delete_submission(email)
    except:
        print("submission already deleted.")


# create test
def test_register(temp_submission):
    # result = sub.register(TEST_NAME, TEST_EMAIL)
    assert TEMP_EMAIL == temp_submission
    assert sub.submission_exists(TEMP_EMAIL)
    assert sub.submission_exists(temp_submission)
    submission = sub.get_submission(temp_submission)
    assert TEMP_EMAIL == submission[sub.EMAIL]
    assert TEMP_NAME == submission[sub.NAME]


# read all test
def test_read_submissions(temp_submission):
    result = sub.read_submissions()
    if len(result) == 0:
        print("submissions database is empty")
        return
    print(result)
    for key, value in result.items():
        assert sub.EMAIL and sub.NAME in value
        assert isinstance(key, str)
    assert temp_submission in result
    assert TEST_EMAIL in result
    assert TEST_NAME in result[TEST_EMAIL][sub.NAME]
    assert "Allen Ng" in result["allnng222@yahoo.com"][sub.NAME]


# read one test 
def test_read_one_submission(temp_submission):
    submission = sub.get_submission(temp_submission)
    print(submission)
    assert submission[sub.EMAIL] == temp_submission
    assert submission[sub.NAME] == TEMP_NAME
    for key, value in submission.items():
        assert isinstance(key, str)
        assert isinstance(value, str)

    assert sub.get_submission(NONEXISTENT_EMAIL) == None
    

# delete test 
def test_delete(temp_submission):
    temp_dict = {sub.NAME: TEMP_NAME, sub.EMAIL: TEMP_EMAIL} 
    assert sub.get_submission(temp_submission) == temp_dict
    result = sub.delete_submission(temp_submission)
    assert sub.get_submission(temp_submission) == None
    assert temp_dict == result


# 


    

