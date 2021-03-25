import json
import pytest

import activeworkflow_agent as aw


### ParsedRequest


def test_parsed_request_with_method_register(register_method_request):
    request = aw.ParsedRequest(register_method_request)

    # {
    #     "method": "register",
    #     "params": {}
    # }
    assert request.method == "register"
    assert request.options == {}
    assert request.credentials == []
    assert request.memory == {}
    assert request.message is None


def test_parsed_request_with_method_check(check_method_request):
    request = aw.ParsedRequest(check_method_request)

    # {
    #     "method": "check",
    #     "params": {
    #         "message": null,
    #         "options": {
    #             "option": "value"
    #         },
    #         "memory": {
    #             "key": "value"
    #         },
    #         "credentials": [
    #             {"name": "admin_email", "value": "admin@example.org"}
    #         ]
    #     }
    # }
    assert request.method == "check"
    assert request.message is None
    assert request.options == {"option": "value"}
    assert request.memory == {"key": "value"}
    assert request.credentials == [
        {"name": "admin_email", "value": "admin@example.org"}
    ]


def test_parsed_request_with_method_receive(receive_method_request):
    request = aw.ParsedRequest(receive_method_request)

    # {
    #     "method": "receive",
    #     "params": {
    #         "message": {
    #             "payload": { "a": 1, "b": 2 }
    #         },
    #         "options": {
    #             "option": "value",
    #             "email_credential": "admin_email"
    #         },
    #         "memory": {
    #             "key": "value"
    #         },
    #         "credentials": [
    #             { "name": "admin_email", "value": "admin@example.org" }
    #         ]
    #     }
    # }
    assert request.method == "receive"
    assert request.message == {"a": 1, "b": 2}
    assert request.options == {
        "option": "value",
        "email_credential": "admin_email",
    }
    assert request.memory == {"key": "value"}
    assert request.credentials == [
        {"name": "admin_email", "value": "admin@example.org"}
    ]


### RegisterResponse


def test_register_response(agent_registration_details):
    """Successfully create a RegisterResponse object."""
    assert aw.RegisterResponse(**agent_registration_details)


def test_register_response_to_dict(
    agent_registration_details, valid_register_schema
):
    """RegisterResponse.to_dict() returns a valid response dict."""
    response = aw.RegisterResponse(**agent_registration_details)

    valid_register_schema.validate(response.to_dict())


def test_register_response_to_json(agent_registration_details):
    """RegisterResponse.to_json() returns valid JSON."""
    response = aw.RegisterResponse(**agent_registration_details)

    json.loads(response.to_json())


def test_register_response_with_invalid_default_options():
    """Throws an exception when default_options is not a dict."""
    with pytest.raises(TypeError):
        aw.RegisterResponse(
            name="SomeAgent",
            display_name="Some Agent",
            description="Some agent for testing purposes.",
            default_options="This should not be a string.",
        )


### Response


def test_add_logs_to_response():
    """Successfully add log messages to a response."""
    response = aw.Response()
    log1 = "Logging something"
    log2 = "Logging something else"

    response.add_logs(log1, log2)
    logs = response.to_dict()["result"]["logs"]

    assert log1 in logs and log2 in logs


def test_add_logs_to_response_does_not_accept_empty_strings():
    """Throws exception when a log is an empty string."""
    response = aw.Response()
    empty_string = ""

    with pytest.raises(ValueError):
        response.add_logs(empty_string)


def test_add_logs_to_response_only_accepts_strings():
    """Throws exception when a log is not a string."""
    response = aw.Response()
    not_a_string = {}

    with pytest.raises(TypeError):
        response.add_logs("A regular log", not_a_string)


def test_add_logs_to_response_only_succeeds_when_all_log_entries_valid():
    """Throws exception and doesn't add any log entries if one is invalid."""
    response = aw.Response()
    valid_log = "A log entry"
    not_a_string = {}

    with pytest.raises(TypeError):
        response.add_logs(valid_log, not_a_string)

    assert valid_log not in response.to_dict()["result"]["logs"]


def test_add_errors_to_response_does_not_accept_empty_strings():
    """Throws exception when an error is an empty string."""
    response = aw.Response()
    empty_string = ""

    with pytest.raises(ValueError):
        response.add_errors(empty_string)


def test_add_errors_to_response_only_accepts_strings():
    """Throws exception when an error is not a string."""
    response = aw.Response()
    not_a_string = {}

    with pytest.raises(TypeError):
        response.add_errors(not_a_string)


def test_add_errors_to_response_only_succeeds_when_all_error_entries_valid():
    """Throws exception and doesn't add any error entries if one is invalid."""
    response = aw.Response()
    valid_error = "A log entry"
    not_a_string = {}

    with pytest.raises(TypeError):
        response.add_errors(valid_error, not_a_string)

    assert valid_error not in response.to_dict()["result"]["errors"]


def test_add_errors_to_response():
    """Successfully add error messages to a response."""
    response = aw.Response()
    err1 = "An error"
    err2 = "Another error"

    response.add_errors(err1, err2)
    errors = response.to_dict()["result"]["errors"]

    assert err1 in errors and err2 in errors


def test_add_messages_to_response():
    """Successfully add messages to a response."""
    response = aw.Response()
    msg = {"Hello": "World"}
    another_msg = {"Bye": "Now"}

    response.add_messages(msg, another_msg)
    messages = response.to_dict()["result"]["messages"]

    assert msg in messages


def test_add_messages_to_response_only_accepts_dicts():
    """Throws an exception when any of the messages passed is not a dict."""
    response = aw.Response()
    msg = {"Hello": "World"}
    another_msg = "Bye Now"

    with pytest.raises(TypeError):
        response.add_messages(msg, another_msg)


def test_add_messages_to_response_only_succeeds_when_all_messages_are_valid():
    """Throws exception and doesn't add any messages if one is invalid."""
    response = aw.Response()
    msg = {"Hello": "World"}
    another_msg = "Bye Now"

    with pytest.raises(TypeError):
        response.add_messages(msg, another_msg)

    assert msg not in response.to_dict()["result"]["messages"]


def test_add_memory_to_response():
    """Successfully add memory to a response."""
    response = aw.Response()
    mem = {"Something": "to remember"}

    response.add_memory(mem)
    memory = response.to_dict()["result"]["memory"]

    assert mem == memory


def test_add_memory_only_accepts_dicts():
    """Throws an exception when a message is not a dict."""
    response = aw.Response()
    mem = ["Not", "a dict"]

    with pytest.raises(TypeError):
        response.add_memory(mem)


def test_response_to_dict(valid_response_schema):
    """Response should return a valid response dict."""
    response = aw.Response()
    response.add_errors("An error", "Another error")
    response.add_logs("Log something", "Log something else")
    response.add_messages({"Hello": "World"}, {"Hi": 1})
    response.add_memory({"Something": {"to": "remember"}})

    valid_response_schema.validate(response.to_dict())


def test_response_to_json():
    """Response should be serialisable to JSON."""
    response = aw.Response()
    response.add_errors("An error", "Another error")
    response.add_logs("Log something", "Log something else")
    response.add_messages({"Hello": "World"}, {"Hi": 1})
    response.add_memory({"Something": {"to": "remember"}})

    json.loads(response.to_json())
