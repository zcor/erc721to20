# @version ^0.2.0

"""
@title ERC721 to ERC20 Bridge
@notice Simple ERC20 Token minted by wrapping linked ERC721 
        https://eips.ethereum.org/EIPS/eip-20
        https://eips.ethereum.org/EIPS/eip-721
"""

from vyper.interfaces import ERC20
from vyper.interfaces import ERC721 as ERC721



implements: ERC20


event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256


name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)
totalSupply: public(uint256)

# Address of Linked ERC-721 Contract
linked721: public(address)

balances: HashMap[address, uint256]
allowances: HashMap[address, HashMap[address, uint256]]

# Map of owned ERC-721 tokens
ownedTokens: HashMap[uint256, uint256]
currentCounter: public(uint256)

@external
def __init__(_nft_addr: address, _name: String[64], _symbol: String[32], _decimals: uint256):
 
    self.name = _name
    self.symbol = _symbol
    self.decimals = _decimals
    self.linked721 = _nft_addr
    self.currentCounter = 0


@view
@external
def balanceOf(_owner: address) -> uint256:
    """
    @notice Getter to check the current balance of an address
    @param _owner Address to query the balance of
    @return Token balance
    """
    return self.balances[_owner]


@view
@external
def allowance(_owner : address, _spender : address) -> uint256:
    """
    @notice Getter to check the amount of tokens that an owner allowed to a spender
    @param _owner The address which owns the funds
    @param _spender The address which will spend the funds
    @return The amount of tokens still available for the spender
    """
    return self.allowances[_owner][_spender]


@external
def approve(_spender : address, _value : uint256) -> bool:
    """
    @notice Approve an address to spend the specified amount of tokens on behalf of msg.sender
    @dev Beware that changing an allowance with this method brings the risk that someone may use both the old
         and the new allowance by unfortunate transaction ordering. One possible solution to mitigate this
         race condition is to first reduce the spender's allowance to 0 and set the desired value afterwards:
         https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
    @param _spender The address which will spend the funds.
    @param _value The amount of tokens to be spent.
    @return Success boolean
    """
    self.allowances[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True


@internal
def _transfer(_from: address, _to: address, _value: uint256):
    """
    @dev Internal shared logic for transfer and transferFrom
    """
    assert self.balances[_from] >= _value, "Insufficient balance"
    self.balances[_from] -= _value
    self.balances[_to] += _value
    log Transfer(_from, _to, _value)


@external
def transfer(_to : address, _value : uint256) -> bool:
    """
    @notice Transfer tokens to a specified address
    @dev Vyper does not allow underflows, so attempting to transfer more
         tokens than an account has will revert
    @param _to The address to transfer to
    @param _value The amount to be transferred
    @return Success boolean
    """
    self._transfer(msg.sender, _to, _value)
    return True


@external
def transferFrom(_from : address, _to : address, _value : uint256) -> bool:
    """
    @notice Transfer tokens from one address to another
    @dev Vyper does not allow underflows, so attempting to transfer more
         tokens than an account has will revert
    @param _from The address which you want to send tokens from
    @param _to The address which you want to transfer to
    @param _value The amount of tokens to be transferred
    @return Success boolean
    """
    assert self.allowances[_from][msg.sender] >= _value, "Insufficient allowance"
    self.allowances[_from][msg.sender] -= _value
    self._transfer(_from, _to, _value)
    return True


@external
def wrap(_tokenId: uint256) -> bool:
    """
    @notice Wrap a single ERC721 token as an ERC20 token
    @dev Vyper does not allow underflows, so attempting to transfer more
         tokens than an account has will revert
    @param _tokenId The token ID you want to transfer
    @return Success boolean
    """

    assert ERC721(self.linked721).getApproved(_tokenId) == self, "Insufficient allowance"
    ERC721(self.linked721).transferFrom(msg.sender, self, _tokenId)
    self.balances[msg.sender] += 10**self.decimals
    self.ownedTokens[self.currentCounter] = _tokenId
    self.currentCounter += 1

    return True


@external
def unwrap() -> bool:
    """
    @notice Unwrap a single wrapped ERC721 (LIFO) 
    @dev Requires sufficient balance (quantity x 10 ** decimals)
    @return Success boolean
    """

    assert self.balances[msg.sender] >= 10**self.decimals, "Insufficient balance"
    assert self.currentCounter > 0, "Supply drained"
   
    ERC721(self.linked721).transferFrom(self, msg.sender, self.ownedTokens[self.currentCounter])
    self.balances[msg.sender] -= 10**self.decimals
    self.ownedTokens[self.currentCounter] = 0
    self.currentCounter -= 1

    return True


