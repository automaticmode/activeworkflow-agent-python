import json

import pytest
import schema


@pytest.fixture()
def agent_registration_details():
    """Data that an agent shares in response to the 'register' request."""
    return {
        "name": "PyTestAgent",
        "display_name": "Pytest agent",
        "description": "Just a trivial agent for testing purposes.",
        "default_options": {},
    }


@pytest.fixture()
def valid_agent_registration_content(
    agent_registration_details,
):
    """Data that an agent shares in response to the 'register' request."""
    return {"result": agent_registration_details}


@pytest.fixture()
def register_method_request():
    """Sample 'register' method request.

    See https://github.com/automaticmode/active_workflow/wiki/Remote-Agent-API#the-register-method
    for more details.
    """
    return {
        "method": "register",
        "params": {},
    }


@pytest.fixture()
def check_method_request():
    """Sample 'check' method request.

    See https://github.com/automaticmode/active_workflow/wiki/Remote-Agent-API#the-check-method
    for more details.
    """
    return {
        "method": "check",
        "params": {
            "message": None,  # Check if this should be {}.
            "options": {"option": "value"},
            "memory": {"key": "value"},
            "credentials": [
                {
                    "name": "admin_email",
                    "value": "admin@example.org",
                }
            ],
        },
    }


@pytest.fixture()
def receive_method_request():
    """Sample 'receive' method request.

    See https://github.com/automaticmode/active_workflow/wiki/Remote-Agent-API#the-receive-method
    for more details.
    """
    return {
        "method": "receive",
        "params": {
            "message": {
                "payload": {
                    "a": 1,
                    "b": 2,
                }
            },
            "options": {
                "option": "value",
                "email_credential": "admin_email",
            },
            "memory": {"key": "value"},
            "credentials": [
                {
                    "name": "admin_email",
                    "value": "admin@example.org",
                }
            ],
        },
    }


@pytest.fixture()
def unknown_method_request():
    """Sample unknwon/invalid method request for testing purposes."""
    return json.dumps(
        {
            "method": "some_random_method",
            "params": {},
        }
    )


@pytest.fixture()
def valid_register_schema():
    """A schema for the response to 'register' method."""
    # {
    #     "result": {
    #         "name": "MyAgent",
    #         "display_name": "My Agent",
    #         "description": "This is my first agent",
    #         "default_options": {"option": "value"}
    #     }
    # }
    return schema.Schema(
        {
            "result": {
                "name": str,
                "display_name": str,
                "description": str,
                "default_options": schema.Or({str: object}, {}),
            }
        }
    )


@pytest.fixture()
def valid_response_schema():
    """A schema for the response to 'check' and 'receive' methods."""
    # {
    #     "result": {
    #         "errors": [
    #             "Something failed",
    #             "Something else failed"
    #         ],
    #         "logs": [
    #             "Something happened",
    #             "Something else happened"
    #         ],
    #         "memory": {
    #             "key": "new value"
    #         },
    #         "messages": [
    #             {
    #                 "a": 5
    #             },
    #             {
    #                 "a": 6
    #             }
    #         ]
    #     }
    # }
    return schema.Schema(
        {
            "result": {
                "errors": [str],
                "logs": [str],
                "memory": {str: object},
                "messages": [{str: object}],
            }
        }
    )
