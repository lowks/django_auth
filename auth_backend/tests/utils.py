import json

import responses


def mock_out_post_users(id, email, profile=None):
    url = 'https://auth.kagiso.io/api/v1/users/.json'
    data = {
        'id': id,
        'email': email,
        'confirmation_token': '49:1YkTO2:1VuxvGJre66xqQj6rkEXewmVs08',
        'email_confirmed': None,
        'profile': profile,
        'created': '2015-04-21T08:18:30.368602Z',
        'modified': '2015-04-21T08:18:30.374410Z'
    }

    responses.add(
        responses.POST,
        url,
        body=json.dumps(data),
        status=201,
    )

    return url, data


def mock_out_put_users(id, email, profile=None):
    url = 'https://auth.kagiso.io/api/v1/users/{id}/.json'.format(id=id)
    data = {
        'id': 1,
        'email': email,
        'profile': profile,
        'created': '2015-04-21T08:18:30.368602Z',
        'modified': '2015-04-21T08:18:30.374410Z'
    }

    responses.add(
        responses.PUT,
        url,
        body=json.dumps(data),
        status=200,
    )

    return url, data


def mock_out_delete_users(id):
    url = 'https://auth.kagiso.io/api/v1/users/{id}/.json'.format(id=id)

    responses.add(
        responses.DELETE,
        url,
        status=204,
    )

    return url


def mock_out_confirm_email(id):
    url = 'https://auth.kagiso.io/api/v1/users/{id}/confirm_email/.json'.format(id=id)  # noqa

    responses.add(
        responses.POST,
        url,
        status=204,
    )

    return url


def mock_out_post_sessions(email, password, status):
    url = 'https://auth.kagiso.io/api/v1/sessions/.json'

    responses.add(
        responses.POST,
        url,
        status=status,
    )

    return url


def mock_out_delete_sessions(id):
    url = 'https://auth.kagiso.io/api/v1/sessions/{id}/.json'.format(id=id)

    responses.add(
        responses.DELETE,
        url,
        status=200,
    )

    return url
