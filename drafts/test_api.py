import allure
from pytest import mark
from cfg import AllureStepMessage
from utils.common import parse_qs_params


@allure.feature("Partner Email")
@allure.severity(allure.severity_level.BLOCKER)
class TestPartnerEmail:

    @allure.title("Partner email confirmation")
    @allure.description("Partner can register, get email, confirm email via special link")
    @mark.smoke
    @mark.register_partners(1)
    def test_email_confirmation(self, api, register_partners):
        partner = register_partners[0]
        partner.email.wait_new_message()
        link = partner.email.get_email_confirmation_link()
        params = dict(code=parse_qs_params(link, "code"))
        method, response = api.zbp.get_auth_confirm_email(params)
        success_code = 200
        with allure.step(AllureStepMessage.assert_response_status_code.format(success_code)):
            assert response.status_code == success_code
