#!/usr/bin/python3

from brownie import *
import pytest


def test_unwrap_empties_balance(wrapped_pengu, holder, nft_id):
    wrapped_pengu.unwrap({'from': holder})
    assert wrapped_pengu.balanceOf(holder) == 0


def test_unwrap_returns_token(wrapped_pengu, pengu_nft, holder, nft_id):
    wrapped_pengu.unwrap({'from': holder})
    assert pengu_nft.ownerOf(0) == holder


