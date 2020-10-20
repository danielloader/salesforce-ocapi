import json
from functools import wraps

from httpx import BasicAuth


def contenttype(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "body" in kwargs:
            print(type(body))
            print(body)
            if type(kwargs["body"]) is str:
                if kwargs["body"].startswith("<"):
                    kwargs["headers"].update({"Content-Type": "application/xml"})
                else:
                    raise TypeError
            elif type(kwargs["body"]) is dict:
                kwargs["headers"].update({"Content-Type": "application/json"})
                kwargs["body"] = json.dumps(kwargs["body"])
            else:
                raise TypeError()

        return func(*args, **kwargs)

    return wrapper


def basicauth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if args[0].auth:
                try:
                    assert type(args[0].auth) is tuple
                    assert len(args[0].auth) == 2
                except AssertionError:
                    print(
                        "Basic Auth needs to be in the format of (username, password)"
                    )
                    raise
                basic_auth = BasicAuth(args[0].auth[0], args[0].auth[1])
                kwargs["headers"].update({"Authorization": basic_auth.auth_header})
        except AttributeError:
            pass
        return func(*args, **kwargs)

    return wrapper
