# -*- coding: utf-8 -*-
"""
    Copyright 2010 cloudControl UG (haftungsbeschraenkt)

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import sys
import os

from cctrl.settings import VERSION

from pycclib import cclib
from cctrl.error import InputErrorException, messages
from cctrl.auth import get_credentials, update_tokenfile, delete_tokenfile, read_tokenfile
from cctrl.app import ParseAppDeploymentName


def check_for_updates(latest_version_str, our_version_str=VERSION):
    """
        check if the API reports a version that is greater then our currently
        installed one
    """
    our = dict()
    latest = dict()
    for version, suffix in ((our, our_version_str), (latest, latest_version_str)):
        for part in ['major', 'minor', 'patch']:
            version[part], _, suffix = suffix.partition('.')
            version[part] = int(version[part])
        version['suffix'] = suffix

    for part in ['major', 'minor', 'patch', 'suffix']:
        if latest[part] > our[part]:
            if part == 'major':
                sys.exit(messages['UpdateRequired'])
            else:
                print >> sys.stderr, messages['UpdateAvailable']
            return


def init_api():
    """
        This methods initializes the API but first checks for a
        CCTRL_API_URL environment variable and uses it if found.
        For Windows we also need to load ca_certs differently,
        because the httplib2 provided ones are not included due to
        py2exe.
    """
    try:
        api_url = os.environ.pop('CCTRL_API_URL')
    except KeyError:
        pass
    else:
        cclib.API_URL = api_url
        cclib.DISABLE_SSL_CHECK = True
    if sys.platform == 'win32':
        cclib.CA_CERTS = os.path.join(
            os.path.dirname(os.path.abspath(__file__ )), "../../cacerts.txt")
    return cclib.API(token=read_tokenfile())


def run(args, api):
    """
        run takes care of calling the action with the needed arguments parsed
        using argparse.

        We first try to call the action. In case the called action requires a
        valid token and the api instance does not have one a TokenRequiredError
        gets raised. In this case we catch the error and ask the user for a
        email/password combination to create a new token. After that we call
        the action again.

        pycclib raises an exception any time the API does answer with a
        HTTP STATUS CODE other than 200, 201 or 204. We catch these exceptions
        here and stop cctrlapp using sys.exit and show the error message to the
        user.
    """

    while True:
        try:
            try:
                args.func(args)
            except cclib.TokenRequiredError:
                # check ENV for credentials first
                try:
                    email = os.environ.pop('CCTRL_EMAIL')
                    password = os.environ.pop('CCTRL_PASSWORD')
                except KeyError:
                    email, password = get_credentials()
                try:
                    api.create_token(email, password)
                except cclib.UnauthorizedError:
                    sys.exit(messages['NotAuthorized'])
                else:
                    pass
            except ParseAppDeploymentName:
                sys.exit(messages['InvalidAppOrDeploymentName'])
            else:
                break
        except cclib.UnauthorizedError, e:
            if delete_tokenfile():
                api.set_token(None)
            else:
                sys.exit(messages['NotAuthorized'])
        except cclib.ForbiddenError, e:
            sys.exit(messages['NotAllowed'])
        except cclib.ConnectionException:
            sys.exit(messages['APIUnreachable'])
        except (cclib.BadRequestError, cclib.ConflictDuplicateError, cclib.GoneError,
                cclib.InternalServerError, cclib.NotImplementedError, cclib.ThrottledError,
                InputErrorException), e:
            sys.exit(e)


def shutdown(api):
    """
        shutdown handles updating or deleting the token file on disk each time
        cctrl finishes or gets interrupted.
    """
    if api.check_token():
        update_tokenfile(api)
    else:
        delete_tokenfile()
