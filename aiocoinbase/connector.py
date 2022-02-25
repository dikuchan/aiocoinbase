import aiohttp

from .endpoints import (
    Accounts,
    Conversions,
    Currencies,
    Deposits,
    Fees,
    Oracle,
    Orders,
    Products,
    Profiles,
    Reports,
    Transfers,
    Withdrawals,
)


class Connector:
    def __init__(
        self,
        secret: str,
        session: aiohttp.ClientSession,
    ):
        """
        asyncio Coinbase Pro connector.

        Connector class with the properties representing groups of endpoints.

        This class must be initialized via the `connector` method, where all the
        necessary headers are defined.

        :param secret: Coinbase API secret.
        :param session: aiohttp client session.
        """
        self.accounts = Accounts(secret, session)
        self.conversions = Conversions(secret, session)
        self.currencies = Currencies(secret, session)
        self.deposits = Deposits(secret, session)
        self.fees = Fees(secret, session)
        self.oracle = Oracle(secret, session)
        self.orders = Orders(secret, session)
        self.products = Products(secret, session)
        self.profiles = Profiles(secret, session)
        self.reports = Reports(secret, session)
        self.transfers = Transfers(secret, session)
        self.withdrawals = Withdrawals(secret, session)


async def connector(
    key: str,
    secret: str,
    passphrase: str,
    *,
    endpoint: str = "https://api.exchange.coinbase.com",
) -> Connector:
    """
    Create a Coinbase Pro connector.

    :param key: Coinbase Pro API key.
    :param secret: Coinbase Pro API secret.
    :param passphrase: Passphrase specified when creating the Coinbase Pro API key.
    :param endpoint: Coinbase Pro API URL.
    """
    session = aiohttp.ClientSession(
        endpoint,
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "cb-access-key": key,
            "cb-access-passphrase": passphrase,
        },
    )

    return Connector(secret, session)
