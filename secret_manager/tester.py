from gcp_parameter_manager import ParameterManager, ParameterContainer
import json
import uuid

secret_id = "my_test_secret2"

# test update secret version
payload = {
    "application": "test application",
    "account_owner": "sa",
    "client_id": "bdf79825-431b-4e32-90e3-9ae3f85223b0",
    "client_secret": "038c6ad9-7255-45e0-afe1-a31985178aec",
    "refresh_token": "48f52f74-26e3-4b1b-8df4-878c5bb41e95",
}

response = ParameterManager.update_parameter(
    secret_id,
    payload=json.dumps(payload, indent=4),
    create_if_not_exists=True,
)

print(response)


# test access - secret_id needs to exist
parameter = ParameterManager.access_parameter(secret_id, parse_tokens=True, debug=True)
print(parameter)
print(parameter.application)
print(parameter.account_owner)
print(parameter.client_id)
print(parameter.client_secret)
print(parameter.refresh_token)

from pydantic import BaseModel
class MyKeyParmsModel(BaseModel):
    application: str
    account_owner: str
    client_id: str
    client_secret: str
    refresh_token: str

parms_instance = MyKeyParmsModel(**parameter.__dict__)
print(parms_instance)


# test update parameter key = secret_id must exist with a key: refresh_token:
response = ParameterManager.update_parameter_key(
    secret_id, key_name="refresh_token", key_value=str(uuid.uuid4())
)
print(response)
