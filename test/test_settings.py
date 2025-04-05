from woo_py.models.setting import SettingOption
from woo_py.woo import Woo


def test_settings_methods(woo: Woo):
    # Test getting all settings
    all_settings = woo.get_settings()
    assert len(all_settings) > 0
    for setting in all_settings:
        assert isinstance(setting, SettingOption)
    
    # Test getting settings for a specific group (general is a common group)
    general_settings = woo.get_settings("general")
    assert len(general_settings) > 0
    for setting in general_settings:
        assert isinstance(setting, SettingOption)
    
    # Test getting a specific setting (woocommerce_store_address is a common setting)
    if general_settings:
        # Find a setting ID to test
        setting_id = general_settings[0].id
        
        # Get specific setting
        specific_setting = woo.get_setting("general", setting_id)
        assert specific_setting is not None
        assert specific_setting.id == setting_id
        
        # We typically don't test updating settings in an automated test
        # as it could affect the store configuration