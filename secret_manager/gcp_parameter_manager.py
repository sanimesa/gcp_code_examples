import os
import json
from typing import Union
from google.cloud import secretmanager

class ParameterContainer:
    """
    A simple container class to hold parameters loaded from Secret Manager.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class ParameterManager:
    """
    A utility class for managing parameters stored in Google Cloud Secret Manager.
    """

    __default_project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    __default_version = 'latest'

    @staticmethod
    def access_parameter(
        secret_id: str,
        parse_tokens: bool = False,
        project_id: str = __default_project_id,
        version_id: str = __default_version,
        debug: bool = False,
    ) -> Union[str, ParameterContainer]:
        """
        Retrieves a parameter from Google Cloud Secret Manager.

        Args:
            secret_id (str): The ID of the secret to retrieve.
            parse_tokens (bool, optional): Whether to parse the secret as JSON and return a ParameterContainer object. Defaults to False.
            project_id (str, optional): The Google Cloud project ID. Defaults to the value of the GOOGLE_CLOUD_PROJECT environment variable.
            version_id (str, optional): The version of the secret to access. Defaults to 'latest'.
            debug (bool, optional): Whether to print the secret value. Defaults to False.

        Returns:
            Union[str, ParameterContainer]: The secret value as a string or a ParameterContainer object if parse_tokens is True.
        """

        client = secretmanager.SecretManagerServiceClient()

        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})

        payload = response.payload.data.decode("UTF-8")

        if debug:
            print("Plain text: {}".format(payload))

        if parse_tokens:
            p_obj = json.loads(payload, object_hook=lambda d: ParameterContainer(**d))
            print(type(p_obj))
            return p_obj

        return payload

    @staticmethod
    def check_parameter_exists(
        client: secretmanager.SecretManagerServiceClient, name: str
    ) -> bool:
        """
        Checks if a secret exists in Google Cloud Secret Manager.

        Args:
            client (secretmanager.SecretManagerServiceClient): The Secret Manager client.
            name (str): The full resource name of the secret to check.

        Returns:
            bool: True if the secret exists, False otherwise.
        """
        try:
            response = client.access_secret_version(name=name)
            print(f"secret {name} exists {response}")
            return True
        except Exception as e:
            print(f"secret {name} does not exist")
            return False

    @staticmethod
    def create_parameter(
        secret_id: str, project_id: str = __default_project_id
    ) -> bool:
        """
        Creates a new secret in Google Cloud Secret Manager.

        Args:
            secret_id (str): The ID of the secret to create.
            project_id (str, optional): The Google Cloud project ID. Defaults to the value of the GOOGLE_CLOUD_PROJECT environment variable.

        Returns:
            bool: True if the secret was created successfully, False otherwise.
        """
        try:
            client = secretmanager.SecretManagerServiceClient()

            parent = f"projects/{project_id}"

            print(f"Creating secret {secret_id} in parent {parent}")
            secret = client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": secret_id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )
            print("Created secret: {}".format(secret.name))
            return True
        except Exception as e:
            print("An error has occurred: ", e)
            return False

    @staticmethod
    def update_parameter(
        secret_id: str, payload: str, create_if_not_exists: bool = False, project_id: str = __default_project_id
    ) -> bool:
        """
        Updates a secret in Google Cloud Secret Manager.

        Args:
            secret_id (str): The ID of the secret to update.
            payload (str): The new secret value as a JSON string.
            create_if_not_exists (bool, optional): Whether to create the secret if it doesn't exist. Defaults to False.
            project_id (str, optional): The Google Cloud project ID. Defaults to the value of the GOOGLE_CLOUD_PROJECT environment variable.

        Returns:
            google.cloud.secretmanager_v1.types.SecretVersion: The updated secret version.
        """

        try: 
            client = secretmanager.SecretManagerServiceClient()

            payload = payload.encode("UTF-8")

            if create_if_not_exists:
                name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
                if not ParameterManager.check_parameter_exists(client, name):
                    response = ParameterManager.create_parameter(secret_id, project_id)

            parent = f"projects/{project_id}/secrets/{secret_id}"
            response = client.add_secret_version(
                request={
                    "parent": parent,
                    "payload": {"data": payload},
                }
            )

            print("Updated secret: {}".format(response.name))
            return True
        except Exception as e:
            print("An error has occurred while updating secret: ", e)
            return False

    @staticmethod
    def update_parameter_key(
        secret_id: str,
        key_name: str,
        key_value: str,
        project_id: str = __default_project_id,
    ) -> bool:
        """
        Updates a specific key within a secret in Google Cloud Secret Manager.

        This method retrieves the secret, updates the specified key with the provided value,
        and then updates the entire secret in Secret Manager.

        Args:
            secret_id (str): The ID of the secret to update.
            key_name (str): The name of the key within the secret to update.
            key_value (str): The new value for the specified key.
            create_if_not_exists (bool, optional): Whether to create the secret if it doesn't exist. Defaults to False.
            project_id (str, optional): The Google Cloud project ID. Defaults to the value of the GOOGLE_CLOUD_PROJECT environment variable.

        Returns:
            bool: True if the secret was updated successfully, False otherwise.
        """

        try: 
            payload = ParameterManager.access_parameter(secret_id, parse_tokens=False, project_id=project_id)
            print(type(payload), payload)

            p_obj = json.loads(payload)
            p_obj.update({key_name: key_value})
            print(p_obj)

            response = ParameterManager.update_parameter(secret_id=secret_id, payload=payload)
            print("Updated secret parameter: {}".format(response))

            return response
        except Exception as e:
            print("An error has occurred while updating secret key: ", e)
            return False