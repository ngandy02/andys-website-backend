import endpoints as ep
import data.submission as sub

from http.client import (
    BAD_REQUEST,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK
)

SUCCESS_MSG = "Feedback Submitted!"

TEST_SUBMISSION = {
    sub.NAME: "Paul Liu",
    sub.EMAIL: "Paulliu123@gmail.com",
    sub.FEEDBACK: "Nice smooth transitions on the UI. It would also be nice to see your research proposals come to life"
}

TEST_EMAIL = "an3299@nyu.edu"

TEST_CLIENT = ep.app.test_client()


def test_create_submission():
    resp = TEST_CLIENT.put(f'{ep.SUBMISSIONS_EP}/create', json=TEST_SUBMISSION)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert ep.MESSAGE in resp_json
    assert ep.RETURN in resp_json
    assert TEST_SUBMISSION[sub.EMAIL] == resp_json[ep.RETURN]
    assert SUCCESS_MSG == resp_json[ep.MESSAGE]


def test_read_submissions():
    resp = TEST_CLIENT.get(f'{ep.SUBMISSIONS_EP}')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert TEST_SUBMISSION[sub.EMAIL] in resp_json
    assert TEST_EMAIL in resp_json
    for value in resp_json.values():
        assert isinstance(value, (dict, list))
        if isinstance(value, dict):
            assert sub.NAME in value 
            assert sub.EMAIL in value
            assert sub.FEEDBACK in value
        elif isinstance(value, list):
            assert isinstance(value[0], dict)
            assert sub.NAME in value[0]
            assert sub.EMAIL in value[0]
            assert sub.FEEDBACK in value[0] 


def test_read_submissions_from_one_email():
    resp = TEST_CLIENT.get(f'{ep.SUBMISSIONS_EP}/{TEST_EMAIL}')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, list)
    for dict in resp_json:
        assert sub.NAME in dict
        assert sub.EMAIL in dict
        assert sub.FEEDBACK in dict
        assert dict[sub.EMAIL] == TEST_EMAIL
