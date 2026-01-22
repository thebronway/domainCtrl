import logging
from app.config import Config

logger = logging.getLogger(__name__)

def get_provider():
    """Factory: Returns the configured DNS Provider instance."""
    config = Config()
    name = config.provider

    if name == 'route53':
        from .route53 import Route53Provider
        return Route53Provider()
    
    # Future providers go here:
    # elif name == 'cloudflare':
    #     from .cloudflare import CloudflareProvider
    #     return CloudflareProvider()

    elif name == 'demo':
        return None # Handled by demo logic elsewhere

    else:
        raise Exception(f"Unknown Provider: {name}")