#!/usr/bin/python3

from brownie import *
import pytest


def test_wrap_increases_balance(wrapped_pengu, pengu_nft, holder, nft_id):
    
    assert wrapped_pengu.balanceOf(holder) > 0


def test_wrap_balance_matches_decimals(wrapped_pengu, pengu_nft, holder, nft_id):
    
    assert wrapped_pengu.balanceOf(holder) == 10 ** wrapped_pengu.decimals()

def test_wrap_bridge_set_as_owner(wrapped_pengu, pengu_nft, holder, nft_id):
    
    assert pengu_nft.ownerOf(0) == wrapped_pengu

def test_wrap_supply_increments(wrapped_pengu, pengu_nft, holder, nft_id):
    
    assert wrapped_pengu.currentCounter() == 1


