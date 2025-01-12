from orbify_projects.api.dependencies import get_session


def test_get_session_creates_session(mocker):
    session_mock = mocker.patch("orbify_projects.api.dependencies.SessionLocal")

    session_generator = get_session()
    session = next(session_generator)

    assert session == session_mock.return_value
    session_mock.assert_called_once()
    session_mock.return_value.close.assert_not_called()

    try:
        next(session_generator)
    except StopIteration:
        pass
    else:
        raise AssertionError("Session generator should have stopped.")
    finally:
        session_mock.return_value.close.assert_called_once()
