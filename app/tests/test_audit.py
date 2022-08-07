import json
from fastapi import status

import requests

from schemas import schemas

from . import utils
from . import data


def test_get_audit(client, access_token):
    response = utils.get_audit(client=client, token=access_token, table_name="users")
    response.status_code = status.HTTP_200_OK
