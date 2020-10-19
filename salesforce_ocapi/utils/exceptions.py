class AuthenticationFailure(Exception):
    def __init__(self, message="Credentials not valid."):
        self.message = message
        super().__init__(self.message)


class CredentialsMissing(Exception):
    def __init__(
        self,
        message="Credentials missing, check credentials file or environmental variables.",
    ):
        self.message = message
        super().__init__(self.message)


class OCAPIMethodNotFound(Exception):
    def __init__(
        self,
        endpoint=None,
        method=None,
        message="OCAPI Method missing for this endpoint.",
    ):
        if endpoint and method:
            self.message = f'{endpoint} has no method named "{method}"'
        else:
            self.message = message
        super().__init__(self.message)


class NotOCAPIEndpoint(Exception):
    def __init__(self, obj, message="Not a OCAPI Endpoint object."):
        if obj:
            self.message = f"{obj} is not an OCAPI Endpoint object."
        else:
            self.message = message
        super().__init__(self.message)


class PaginatorProgressHidden(Exception):
    def __init__(self, message="Paginator progress bar is hidden, can't action."):
        self.message = message
        super().__init__(self.message)


class OCAPIException(Exception):
    def __init__(self, res):
        self.message = f"{res.http_version} {res.status_code}: {res.text}"
        super().__init__(self.message)


class IdempotentTimeout(Exception):
    def __init__(self, method, url, data, headers=None):
        self.message = (
            f"Attempted {method} timed out.\n\n"
            "Details:\n"
            f"URL: {url}\n"
            f"Headers: {headers}\n\n"
            f"Body: {data}\n"
            "No retry attempted as method is not idempotent nor safe to retry."
        )
        super().__init__(self.message)
