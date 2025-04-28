import random

from woo_py.models.payment_gateway import PaymentGateway
from woo_py.woo import Woo


def test_payment_gateway_methods(woo: Woo, random_str: str):
    # List payment gateways
    gateways = woo.list_payment_gateways()
    assert len(gateways) > 0
    
    # Get the first gateway for testing
    if gateways:
        gateway_id = gateways[0].id
        
        # Get a specific gateway
        gateway = woo.get_payment_gateway(gateway_id)
        assert gateway is not None
        assert gateway.id == gateway_id
        
        # Store original title
        original_title = gateway.title
        
        try:
            # Update the gateway (just changing the title for testing)
            gateway.title = f"Test Gateway {random_str}"
            updated_gateway = woo.update_payment_gateway(gateway_id, gateway)
            assert updated_gateway.id == gateway_id
            assert updated_gateway.title == f"Test Gateway {random_str}"
            
            # Verify update worked by getting it again
            refreshed_gateway = woo.get_payment_gateway(gateway_id)
            assert refreshed_gateway.title == f"Test Gateway {random_str}"
            
        finally:
            # Restore original title
            gateway.title = original_title
            woo.update_payment_gateway(gateway_id, gateway)