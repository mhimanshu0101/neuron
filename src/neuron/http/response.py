"""Various HTTP response for use in returning proper HTTP codes."""
from django import http
from rest_framework import response

class Response(response.Response):
    def __init__(
        self, data=None, status=None, template_name=None,
        header=None,
        exception=None, content_type=None):
        super(Response).__init__(data, status, template_name, 
        header, exception, content_type)


class OK(Response):
    """
    200 OK
    Should be used to indicate nonspecific success. Must not be used to
    communicate errors in the response body.
    In most cases, 200 is the code the client hopes to see instantly.
    It indicates that the REST API successfully carried out whatever action
    the client requested, and that no more specific code in the 2xx series is
    appropriate. Unlike the 204 status, a 200 response should include a
    response body.    
    """
    status_code = 200


class Created(Response):
    """
    201 Created.
    To be used to indicate successful resource creation.
    A REST API responds with 201 status code whenever a collection
    creates or a store adds, a new resource at the client's
    request.
    """
    status_code = 201


class Accepted(Response):
    """
    202 Accepted.
    To be used when system accepted the client request and indicate
    successful start of an asynchronous action.
    A 202 response states that client's request will be handled asynchronously.
    It is typically used for actions that take a long while to process.
    Controller/django backend views resources may send 202 responses, but other resource types
    should not.
    """
    status_code = 202


class NoContent(Response):
    """
    204 No Content
    To be used when response body is intentionally empty.
    A 204 status code is usually sent out in response of a
    PUT, POST, PATCH or DELETE request, when REST API declines 
    to send back any status message or representation in the
    response message's body.
    """
    status_code = 204


class NotFound(Response):
    """404 Not Found

    Must be used when a client's URI cannot be mapped to a resource.
    The 404 error status code indicates that the REST API can't map the
    client's URI to a resource.
    """
    status_code = 404