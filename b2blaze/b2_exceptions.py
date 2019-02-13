"""
Copyright George Sibble 2018
"""


class B2ApplicationKeyNotSet(Exception):
    """ You must set the B2_KEY_ID environment variable before running the application """

    pass


class B2KeyIDNotSet(Exception):
    """ You must set the B2_APPLICATION_KEY environment variable before running the application """

    pass


class B2Exception(Exception):
    """ Base exception class for the Backblaze API """

    @staticmethod
    def parse(response):
        """ Parse the response error code and return the related error type. """

        API_EXCEPTION_CODES = {
            400: B2RequestError,
            401: B2UnauthorizedError,
            403: B2ForbiddenError,
            404: B2FileNotFoundError,
            408: B2RequestTimeoutError,
            429: B2TooManyRequestsError,
            500: B2InternalError,
            503: B2ServiceUnavailableError,
        }

        try:
            response_json = response.json()
            message = response_json["message"]
            code = response_json["code"]
            status = int(response_json["status"])

            # Return B2Exception if unrecognized status code
            if not status in API_EXCEPTION_CODES:
                return B2Exception("{} - {}: {}".format(status, code, message))

            ErrorClass = API_EXCEPTION_CODES[status]
            return ErrorClass("{} - {}: {}".format(status, code, message))

        except:
            return Exception(
                "error parsing response. status code - {} Response JSON: {}".format(
                    response.status_code, response_json
                )
            )


class B2FileNotFoundError(Exception):
    """ 404 Not Found """

    pass


class B2RequestError(Exception):
    """ There is a problem with a passed in request parameters. See returned message for details """

    pass


class B2UnauthorizedError(Exception):
    """ When calling b2_authorize_account, this means that there was something wrong with the accountId/applicationKeyId or with the applicationKey that was provided. The code unauthorized means that the application key is bad. The code unsupported means that the application key is only valid in a later version of the API.

    The code unauthorized means that the auth token is valid, but does not allow you to make this call with these parameters. When the code is either bad_auth_token or expired_auth_token you should call b2_authorize_account again to get a new auth token.
    """

    pass


class B2ForbiddenError(Exception):
    """ You have a reached a storage cap limit, or account access may be impacted in some other way; see the human-readable message.
    """

    pass


class B2RequestTimeoutError(Exception):
    """ The service timed out trying to read your request. """

    pass


class B2OutOfRangeError(Exception):
    """ The Range header in the request is outside the size of the file.. """

    pass


class B2TooManyRequestsError(Exception):
    """ B2 may limit API requests on a per-account basis. """

    pass


class B2InternalError(Exception):
    """ An unexpected error has occurred. """

    pass


class B2ServiceUnavailableError(Exception):
    """ The service is temporarily unavailable. The human-readable message identifies the nature of the issue, in general we recommend retrying with an exponential backoff between retries in response to this error.
    """

    pass


class B2InvalidBucketName(Exception):
    """ Bucket name must be alphanumeric or '-' """

    pass


class B2InvalidBucketConfiguration(Exception):
    """ Value error in bucket configuration """

    pass


class B2AuthorizationError(Exception):
    """ An error with the authorization request """

    pass


class B2InvalidRequestType(Exception):
    """ Request type must be get or post """

    pass
