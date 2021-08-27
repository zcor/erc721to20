#!/usr/bin/python3

import pytest
from brownie import Contract

@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass

# Test with the Pudgy Penguins Contract
@pytest.fixture(scope="module")
def pengu_coin(Bridge, accounts):
    return Bridge.deploy("0xBd3531dA5CF5857e7CfAA92426877b022e612cf8", 'Penguin', 'PENGU', 18, {'from': accounts[0]})


@pytest.fixture(scope="module")
def nft_id():
    return 0

@pytest.fixture(scope="module")
def pengu_nft(pengu_coin):
    return Contract(pengu_coin.linked721())

@pytest.fixture(scope="module")
def holder(pengu_nft, nft_id):
    return pengu_nft.ownerOf(nft_id)

@pytest.fixture(scope="module")
def wrapped_pengu(pengu_coin, pengu_nft, holder, nft_id):
    pengu_nft.approve(pengu_coin, nft_id, {'from': holder})
    pengu_coin.wrap(nft_id, {'from': holder})
    return pengu_coin

