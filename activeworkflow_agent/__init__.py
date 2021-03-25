"""ActiveWorkflow Agent Python.

A library to help you write ActiveWorkflow agents in Python that communicate
with ActiveWorkflow via the Remote Agent API. For more information see:

https://docs.activeworkflow.org/remote-agent-api.

The library provides the following classes:

    * ParsedRequest - to parse and encapsulate requests from ActiveWorkflow.
    * RegisterResponse - helper to create responses to the 'register' method.
    * CheckResponse - helper to create responses to the 'check' method.
    * ReceiveResponse - helper to create responses to the 'receive' method.
"""

import json


class ParsedRequest:
    """Helper class to parse the content of a request from the AW agent API."""

    def __init__(self, request):
        """Create a ParsedRequest object.

        Parameters
        ----------
        request : dict
            A dict containing the request received from ActiveWorkflow's API.
            See https://docs.activeworkflow.org/remote-agent-api#protocol for
            more details.

        Attributes
        ----------
        method : str
            The protocol method carried in the request. For more details see:
            https://docs.activeworkflow.org/remote-agent-api/#methods
        options: dict
            A dict with configuration options for the agent.
        memory : dict
            The memory (state) of the agent; can be updated by the agent.
        credentials : list
             An array of user credentials.
        message : dict
             The message that the agent has received.
        """
        self.method = request["method"]
        self.options = {}
        self.memory = {}
        self.credentials = []
        self.message = None

        if self.method in ("check", "receive"):
            self.options = request["params"]["options"]
            self.memory = request["params"]["memory"]
            self.credentials = request["params"]["credentials"]
        if self.method == "receive":
            self.message = request["params"]["message"]["payload"]


class RegisterResponse:
    """Helper class to construct an object to hold an agent's metadata."""

    def __init__(self, name, display_name, description, default_options={}):
        """Create a RegisterResponse object for responding to 'register' method.

        Parameters
        ----------
        name : str
            The name of the agent you want to register. It must be a unique
            identifier written in upper camel case, for example: MyAgent.
        display_name : str
            The name of the agent in free form, as it will be displayed on the
            the user interface.
        description : str
           The description of an agent, which can be in Markdown. It should include an
           introduction (the first line) and usage information, including a description
           of all the configuration options for your agent.
        default_options: dict
           The default options that a user can use as a starting point when
           configuring the agent.
        """
        self.name = name
        self.display_name = display_name
        self.description = description
        self.default_options = default_options
        self._validate()

    def to_dict(self):
        """Returns a dict with the agent's metadata.

        It is in the format that ActiveWorkflow's Agent API expects.
        """
        return {
            "result": {
                "name": self.name,
                "display_name": self.display_name,
                "description": self.description,
                "default_options": self.default_options,
            }
        }

    def to_json(self):
        """Returns a JSON with the agent's metadata.

        It is in the format that ActiveWorkflow's Agent API expects.
        """
        return json.dumps(self.to_dict())

    def _validate(self):
        if not isinstance(self.default_options, dict):
            raise TypeError("default_options must be a dict.")
        if not isinstance(self.name, str):
            raise TypeError("name must be a string.")
        if not isinstance(self.display_name, str):
            raise TypeError("display_name must be a string.")
        if not isinstance(self.description, str):
            raise TypeError("description must be a string.")


class Response:
    """Build a response to the 'check' and 'receive' methods.

    A response looks like this:
    {
        "result": {
            "errors": [
                "Something failed",
                "Something else failed"
            ],
            "logs": [
                "Something happened",
                "Something else happened"
            ],
            "memory": {
                "key": "new value"
            },
            "messages": [
               {
                   "a": 5
               },
               {
                   "a": 6
               }
            ]
        }
    }
    See https://docs.activeworkflow.org/remote-agent-api#responses and
    https://docs.activeworkflow.org/remote-agent-api#methods
    for more details.
    """

    def __init__(self):
        """Create an object for responding to 'receive' or 'check' methods."""
        self._errors = []
        self._logs = []
        self._messages = []
        self._memory = {}

    def add_logs(self, *logs):
        """Add log messages to the response object."""
        for log in logs:
            if not isinstance(log, str):
                raise TypeError("Log entries must be (non-empty) strings.")
            if log == "":
                raise ValueError("Log entries can not be empty strings.")

        for log in logs:
            self._logs.append(log)

    def add_errors(self, *errors):
        """Add error messages to the response object."""
        for err in errors:
            if not isinstance(err, str):
                raise TypeError("Error entries must be (non-empty) strings.")
            if err == "":
                raise ValueError("Error entries can not be empty strings.")

        for err in errors:
            self._errors.append(err)

    def add_messages(self, *messages):
        """Add messages to the response object."""
        for msg in messages:
            if not isinstance(msg, dict):
                raise TypeError("Messages must be dicts.")

        for msg in messages:
            self._messages.append(msg)

    def add_memory(self, mem):
        """Add a memory to the response object."""
        if not isinstance(mem, dict):
            raise TypeError("A memory has to be a dict.")

        self._memory = mem

    def to_dict(self):
        """Returns a dict of the response.

        It is in the format that ActiveWorkflow's Agent API expects.
        """
        return {
            "result": {
                "errors": self._errors,
                "logs": self._logs,
                "memory": self._memory,
                "messages": self._messages,
            }
        }

    def to_json(self):
        """Returns a JSON of the response.

        It is in the format that ActiveWorkflow's Agent API expects.
        """
        return json.dumps(self.to_dict())


CheckResponse = Response
ReceiveResponse = Response
