#!/usr/bin/python3
import brownie


def test_sender_balance_decreases(accounts, pengu_coin):
    sender_balance = pengu_coin.balanceOf(accounts[0])
    amount = sender_balance // 4

    pengu_coin.approve(accounts[1], amount, {'from': accounts[0]})
    pengu_coin.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert pengu_coin.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(accounts, pengu_coin):
    receiver_balance = pengu_coin.balanceOf(accounts[2])
    amount = pengu_coin.balanceOf(accounts[0]) // 4

    pengu_coin.approve(accounts[1], amount, {'from': accounts[0]})
    pengu_coin.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert pengu_coin.balanceOf(accounts[2]) == receiver_balance + amount


def test_caller_balance_not_affected(accounts, pengu_coin):
    caller_balance = pengu_coin.balanceOf(accounts[1])
    amount = pengu_coin.balanceOf(accounts[0])

    pengu_coin.approve(accounts[1], amount, {'from': accounts[0]})
    pengu_coin.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert pengu_coin.balanceOf(accounts[1]) == caller_balance


def test_caller_approval_affected(accounts, pengu_coin):
    approval_amount = pengu_coin.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    pengu_coin.approve(accounts[1], approval_amount, {'from': accounts[0]})
    pengu_coin.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert pengu_coin.allowance(accounts[0], accounts[1]) == approval_amount - transfer_amount


def test_receiver_approval_not_affected(accounts, pengu_coin):
    approval_amount = pengu_coin.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    pengu_coin.approve(accounts[1], approval_amount, {'from': accounts[0]})
    pengu_coin.approve(accounts[2], approval_amount, {'from': accounts[0]})
    pengu_coin.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert pengu_coin.allowance(accounts[0], accounts[2]) == approval_amount


def test_total_supply_not_affected(accounts, pengu_coin):
    total_supply = pengu_coin.totalSupply()
    amount = pengu_coin.balanceOf(accounts[0])

    pengu_coin.approve(accounts[1], amount, {'from': accounts[0]})
    pengu_coin.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert pengu_coin.totalSupply() == total_supply


def test_returns_true(accounts, pengu_coin):
    amount = pengu_coin.balanceOf(accounts[0])
    pengu_coin.approve(accounts[1], amount, {'from': accounts[0]})
    tx = pengu_coin.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert tx.return_value is True


def test_transfer_full_balance(accounts, pengu_coin):
    amount = pengu_coin.balanceOf(accounts[0])
    receiver_balance = pengu_coin.balanceOf(accounts[2])

    pengu_coin.approve(accounts[1], amount, {'from': accounts[0]})
    pengu_coin.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert pengu_coin.balanceOf(accounts[0]) == 0
    assert pengu_coin.balanceOf(accounts[2]) == receiver_balance + amount


def test_transfer_zero_pengu_coins(accounts, pengu_coin):
    sender_balance = pengu_coin.balanceOf(accounts[0])
    receiver_balance = pengu_coin.balanceOf(accounts[2])

    pengu_coin.approve(accounts[1], sender_balance, {'from': accounts[0]})
    pengu_coin.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert pengu_coin.balanceOf(accounts[0]) == sender_balance
    assert pengu_coin.balanceOf(accounts[2]) == receiver_balance


def test_transfer_zero_pengu_coins_without_approval(accounts, pengu_coin):
    sender_balance = pengu_coin.balanceOf(accounts[0])
    receiver_balance = pengu_coin.balanceOf(accounts[2])

    pengu_coin.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert pengu_coin.balanceOf(accounts[0]) == sender_balance
    assert pengu_coin.balanceOf(accounts[2]) == receiver_balance


def test_insufficient_balance(accounts, pengu_coin):
    balance = pengu_coin.balanceOf(accounts[0])

    pengu_coin.approve(accounts[1], balance + 1, {'from': accounts[0]})
    with brownie.reverts():
        pengu_coin.transferFrom(accounts[0], accounts[2], balance + 1, {'from': accounts[1]})


def test_insufficient_approval(accounts, wrapped_pengu, holder):
    balance = wrapped_pengu.balanceOf(holder)

    wrapped_pengu.approve(accounts[1], balance - 1, {'from': holder})
    with brownie.reverts():
        wrapped_pengu.transferFrom(holder, accounts[2], balance, {'from': accounts[1]})


def test_no_approval(accounts, wrapped_pengu, holder):
    balance = wrapped_pengu.balanceOf(holder)

    with brownie.reverts():
        wrapped_pengu.transferFrom(holder, accounts[2], balance, {'from': accounts[1]})


def test_revoked_approval(accounts, wrapped_pengu, holder):
    balance = wrapped_pengu.balanceOf(holder)

    wrapped_pengu.approve(accounts[1], balance, {'from': holder})
    wrapped_pengu.approve(accounts[1], 0, {'from': holder})

    with brownie.reverts():
        wrapped_pengu.transferFrom(holder, accounts[2], balance, {'from': accounts[1]})


def test_transfer_to_self(accounts, wrapped_pengu, holder):
    sender_balance = wrapped_pengu.balanceOf(holder)
    amount = sender_balance // 4

    wrapped_pengu.approve(holder, sender_balance, {'from': holder})
    wrapped_pengu.transferFrom(holder, holder, amount, {'from': holder})

    assert wrapped_pengu.balanceOf(holder) == sender_balance
    assert wrapped_pengu.allowance(holder, holder) == sender_balance - amount


def test_transfer_to_self_no_approval(accounts, wrapped_pengu, holder):
    amount = wrapped_pengu.balanceOf(holder)

    with brownie.reverts():
        wrapped_pengu.transferFrom(holder, accounts[0], amount, {'from': accounts[0]})


def test_transfer_event_fires(accounts, pengu_coin):
    amount = pengu_coin.balanceOf(accounts[0])

    pengu_coin.approve(accounts[1], amount, {'from': accounts[0]})
    tx = pengu_coin.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[2], amount]
