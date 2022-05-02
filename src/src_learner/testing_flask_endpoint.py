import pytest
import flask_endpoints


@pytest.fixture()
def app():
    print("here")
    app = flask_endpoints()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


def test_predict(client):
    rv = client.post("/api_predict?t?code_to_format=cHJpbnQoKQ==&language=python")
    assert b'{"ok": 1,"prediction": [9,0,0],"result": [{"startIndex": 0,"endIndex": 4,"lItemtokenId": 42},{"startIndex": 5,"endIndex": 5,"lItemtokenId": 54},{"startIndex": 6,"endIndex": 6,"lItemtokenId": 55}]}' == rv.data


"""@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()"""