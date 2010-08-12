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

messages = {}
messages['NoDeployment'] = r'You have to append the deployment name.'
messages['WrongApplication'] = r'This application is unknown.'
messages['WrongDeployment'] = r'This deployment is unknown.'
messages['PasswordsDontMatch'] = r"The passwords don't match."
messages['InvalidApplicationName'] = r'Name may only contain a-z and 0-9 and must not start with a number.' 
messages['WrongUsername'] = r'This username is unknown.'
messages['UserBelongsToApp'] = r'This user already belongs to this application.'
messages['UserDoesntBelongToApp'] = r'This user does not belong to this application.'
messages['DeleteOnlyApplication'] = r'You can only delete applications not deployments. Try undeploy.'
messages['NoAliasGiven'] = r'You have to specify an alias.'
messages['WrongAlias'] = r'This alias is unknown.'
messages['NotAllowed'] = r'Sorry. You are not allowed to perform this action.'
messages['CannotDeleteDeploymentExist'] = r'You have to undeploy all deployments, before you can delete the application.'
messages['NotAuthorized'] = r'The authorization failed, check your e-mail address and password.'
messages['PermissionDenied'] = r'You are not allowed to push to this repository. Maybe check your keys using cctrluser listKeys.'
messages['SecurityQuestionDenied'] = r'Action canceled on user request.'

class InputErrorException(Exception):
    """
        This exception is raised if for some reason someone put something in we
        could not understand at all.
    """
    def __init__(self, errorKey):
        self.message = messages[errorKey]
        
    def __str__(self):
        return self.message

class PasswordsDontMatchException(Exception):
    """
        This exception is raised if the password and the password check weren't
        equal for three times.
    """
    pass