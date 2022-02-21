import allure
from pytest import fixture
from typing import List
from dataclasses import dataclass


class GmailClient:
    address: str


@dataclass
class NewPartner:
    id: int
    username: str
    password: str
    email: GmailClient

    def __post_init__(self):
        self.comm_type: str = "email"
        self.comm_value = self.email.address


@fixture
@allure.title("Partner registration via API")
def register_partners(request, api, moderator) -> List[NewPartner]:
    # Get partner count for test
    partner_count = request.node.get_closest_marker(register_partners.__name__).args[0]
    partner_list = []
    for _ in range(partner_count):
        partner = api.emw.create_partner()
        partner_list.append(partner)

    # Return partner list to test
    yield partner_list

    # Change partner state to inactive
    api.moderator.login(moderator)
    for partner in partner_list:
        api.moderator.deactivate_partner(partner.id)
