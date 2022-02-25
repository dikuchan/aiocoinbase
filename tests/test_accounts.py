import os

import pytest

import aiocoinbase

CONNECTOR_PARAMETERS = {
    "key": os.getenv("COINBASE_SANDBOX_KEY"),
    "secret": os.getenv("COINBASE_SANDBOX_SECRET"),
    "passphrase": os.getenv("COINBASE_SANDBOX_PASSPHRASE"),
    "endpoint": os.getenv("COINBASE_SANDBOX_ENDPOINT"),
}
ACCOUNT_ID = os.getenv("COINBASE_SANDBOX_ID")


@pytest.mark.asyncio
async def test_get_account():
    connector = await aiocoinbase.connector(**CONNECTOR_PARAMETERS)
    await connector.accounts.get(ACCOUNT_ID)


@pytest.mark.asyncio
async def test_get_accounts():
    connector = await aiocoinbase.connector(**CONNECTOR_PARAMETERS)
    await connector.accounts.get_all()


@pytest.mark.asyncio
async def test_get_holds():
    connector = await aiocoinbase.connector(**CONNECTOR_PARAMETERS)
    await connector.accounts.get_holds(ACCOUNT_ID)


@pytest.mark.asyncio
async def test_get_ledger():
    connector = await aiocoinbase.connector(**CONNECTOR_PARAMETERS)
    await connector.accounts.get_ledger(ACCOUNT_ID)


@pytest.mark.asyncio
async def test_get_transfers():
    connector = await aiocoinbase.connector(**CONNECTOR_PARAMETERS)
    await connector.accounts.get_transfers(ACCOUNT_ID)
