from unittest.mock import MagicMock, create_autospec


class MyCRMService:
    def sync_user(self, *, first_name: str, last_name: str, email: str) -> None:
        print("Calling MyCRM's REST API to send data there. That's slow and unreliable.")


class CreateUser:
    def __init__(self, *, crm_service: MyCRMService) -> None:
        self._crm_service = crm_service

    def execute(self, *, first_name: str, last_name: str, email: str) -> None:
        print("Store user in database")
        print("Send welcome email")
        self._crm_service.sync_user(first_name=first_name, last_name=last_name, email=email)


class CreateUserWrongUsage:
    def __init__(self, *, crm_service: MyCRMService) -> None:
        self._crm_service = crm_service

    def execute(self, *, first_name: str, last_name: str, email: str) -> None:
        print("Store user in database")
        print("Send welcome email")
        self._crm_service.sync_user(first_name, last_name, email)


def test_user_data_synced_to_crm_magic_mock():
    crm_service = MagicMock()
    create_user = CreateUser(crm_service=crm_service)
    first_name = "John"
    last_name = "Doe"
    email = "john@doe.com"

    create_user.execute(first_name=first_name, last_name=last_name, email=email)

    crm_service.sync_user.assert_called_once_with(first_name=first_name, last_name=last_name, email=email)
    # This one passes because usage is correct - keyword arguments are used when calling


def test_user_data_synced_to_crm_create_autospec():
    crm_service = create_autospec(MyCRMService)
    create_user = CreateUser(crm_service=crm_service)
    first_name = "John"
    last_name = "Doe"
    email = "john@doe.com"

    create_user.execute(first_name=first_name, last_name=last_name, email=email)

    crm_service.sync_user.assert_called_once_with(first_name=first_name, last_name=last_name, email=email)
    # This one passes because usage is correct - keyword arguments are used when calling

def test_user_data_synced_to_crm_wrong_usage_magic_mock():
    crm_service = MagicMock()
    create_user = CreateUserWrongUsage(crm_service=crm_service)
    first_name = "John"
    last_name = "Doe"
    email = "john@doe.com"

    create_user.execute(first_name=first_name, last_name=last_name, email=email)


    crm_service.sync_user.assert_called_once_with(first_name, last_name, email)
    # This passes because MagicMock calls whatever you provide, but it should fail because usage is wrong - positional arguments are used when calling instead of keyword arguments


def test_user_data_synced_to_crm_wrong_usage_create_autospec():
    crm_service = create_autospec(MyCRMService)
    create_user = CreateUserWrongUsage(crm_service=crm_service)
    first_name = "John"
    last_name = "Doe"
    email = "john@doe.com"

    create_user.execute(first_name=first_name, last_name=last_name, email=email)

    crm_service.sync_user.assert_called_once_with(first_name, last_name, email)
    # This one is failing because usage is wrong - positional arguments are used when calling instead of keyword arguments

