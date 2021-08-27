from brownie import Bridge, accounts

def main():
    return Bridge.deploy("0xBd3531dA5CF5857e7CfAA92426877b022e612cf8", 'Penguin', 'PENGU', 18, {'from': accounts[0]})

