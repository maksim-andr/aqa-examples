import allure
from pytest import mark
from dataclasses import dataclass


@dataclass
class Device:
    id: int
    name: str


@allure.feature("Tests for Client dashboard")
@allure.severity(allure.severity_level.CRITICAL)
class TestClient:

    @allure.title("Session verification via Client user")
    @allure.description("Client can verify charging session on Reports page, Devices page, common Dashboard")
    @mark.smoke
    @mark.device_count(1)
    def test_login_as_client(self, pages_b2b, api, create_default_location_new_client_b2b,
                             emulate_devices, dashboard_page_new_client_b2b):
        # Fixtures results
        reseller, client = dashboard_page_new_client_b2b
        location = create_default_location_new_client_b2b
        device: Device = emulate_devices[0]

        # Add device to location
        pages_b2b.header.add_new_device()
        pages_b2b.device.create_page.add_default_device(device, location)
        assert device.name in pages_b2b.device.list_page.get_device_name_list()

        # Start and wait charging session
        api.cloud_emulator.plugin_and_run(device.id)
        pages_b2b.device.list_page.wait_for_device_status_charging(device.name)
        api.cloud_emulator.unplug_and_stop(device.id)

        # Login as client
        pages_b2b.header.logout()
        assert pages_b2b.login_page.is_loaded()
        pages_b2b.login_page.login(reseller.email.address, reseller.password)
        pages_b2b.client.list_page.wait_loading_clients_list()
        pages_b2b.client.list_page.search_client(client.name)
        pages_b2b.client.list_page.click_login_as_client(client.name)
        with allure.step("Verify Dashboard is loaded"):
            assert pages_b2b.dashboard_page.is_loaded()

        # Verify session report via Reports
        pages_b2b.navigation_menu.go_to_reports()
        pages_b2b.reports_page.click_tab_sessions()
        pages_b2b.reports_page.wait_report_sessions_data_visible()
        with allure.step("Verify session report via Reports"):
            assert device.name in pages_b2b.reports_page.get_sessions_device_name_list()

        # Verify session report via Devices
        pages_b2b.navigation_menu.go_to_devices()
        pages_b2b.device.list_page.go_to_device_details(device.name)
        pages_b2b.device.details_page.click_tab_history()
        with allure.step("Verify session report via Devices"):
            assert pages_b2b.device.details_page.get_history_row_count() == 1

        # Go to dashboard and verify components
        pages_b2b.navigation_menu.go_to_home()
        with allure.step("Verify Dashboard components"):
            assert pages_b2b.dashboard_page.is_loaded()
            assert pages_b2b.header.is_filter_locations_visible()

        # Go to client list and verify components
        pages_b2b.header.click_back_to_reseller()
        with allure.step("Verify Clients list components"):
            assert len(pages_b2b.client.list_page.get_client_list())
