from abc import ABC, abstractmethod

class BaseDNSProvider(ABC):
    """Interface that all DNS providers must implement."""

    @abstractmethod
    def get_record_ip(self, domain):
        """Returns the current IP of the A record, or ALIAS string."""
        pass

    @abstractmethod
    def update_record_ip(self, domain, new_ip):
        """Updates the A record to the new IP."""
        pass

    @abstractmethod
    def get_certbot_flags(self):
        """Returns the specific certbot flags (e.g., --dns-route53)."""
        pass