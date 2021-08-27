#!/usr/bin/python3
import brownie


def test_sender_balance_decreases(accounts, pengu_coin):
    sender_balance = pengu_coin.balanceOf(accounts[0])
    amount = sender_balance // 4

    pengu_coin.transfer(accounts[1], amount, {"from": accounts[0]})

    assert pengu_coin.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(accounts, pengu_coin):
    receiver_balance = pengu_coin.balanceOf(accounts[1])
    amount = pengu_coin.balanceOf(accounts[0]) // 4

    pengu_coin.transfer(accounts[1], amount, {"from": accounts[0]})

    assert pengu_coin.balanceOf(accounts[1]) == receiver_balance + amount


def test_total_supply_not_affected(accounts, pengu_coin):
    total_supply = pengu_coin.totalSupply()
    amount = pengu_coin.balanceOf(accounts[0])

    pengu_coin.transfer(accounts[1], amount, {"from": accounts[0]})

    assert pengu_coin.totalSupply() == total_supply


def test_returns_true(accounts, pengu_coin):
    amount = pengu_coin.balanceOf(accounts[0])
    tx = pengu_coin.transfer(accounts[1], amount, {"from": accounts[0]})

    assert tx.return_value is True


def test_transfer_full_balance(accounts, pengu_coin):
    amount = pengu_coin.balanceOf(accounts[0])
    receiver_balance = pengu_coin.balanceOf(accounts[1])

    pengu_coin.transfer(accounts[1], amount, {"from": accounts[0]})

    assert pengu_coin.balanceOf(accounts[0]) == 0
    assert pengu_coin.balanceOf(accounts[1]) == receiver_balance + amount


def test_transfer_zero_pengu_coins(accounts, pengu_coin):
    sender_balance = pengu_coin.balanceOf(accounts[0])
    receiver_balance = pengu_coin.balanceOf(accounts[1])

    pengu_coin.transfer(accounts[1], 0, {"from": accounts[0]})

    assert pengu_coin.balanceOf(accounts[0]) == sender_balance
    assert pengu_coin.balanceOf(accounts[1]) == receiver_balance


def test_transfer_to_self(accounts, pengu_coin):
    sender_balance = pengu_coin.balanceOf(accounts[0])
    amount = sender_balance // 4

    pengu_coin.transfer(accounts[0], amount, {"from": accounts[0]})

    assert pengu_coin.balanceOf(accounts[0]) == sender_balance


def test_insufficient_balance(accounts, pengu_coin):
    balance = pengu_coin.balanceOf(accounts[0])

    with brownie.reverts():
        pengu_coin.transfer(accounts[1], balance + 1, {"from": accounts[0]})


def test_transfer_event_fires(accounts, pengu_coin):
    amount = pengu_coin.balanceOf(accounts[0])
    tx = pengu_coin.transfer(accounts[1], amount, {"from": accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[1], amount]
