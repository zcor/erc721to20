# ERC 721 to 20

Proof of concept script to wrap an NFT and use as an ERC-20 token.

Based on a bare-bones implementation of the Ethereum [ERC-20 standard](https://eips.ethereum.org/EIPS/eip-20), written in [Vyper](https://github.com/vyperlang/vyper).

[Further Details](https://curve.substack.com/p/august-27-2021-fungible-nfts-)

## Testing

To run the tests:

```bash
brownie test --network mainnet-fork
```

The unit tests included in this mix are very generic and should work with any ERC721 compliant smart contract. To use them in your own project, all you must do is modify the deployment logic in the [`tests/conftest.py`](tests/conftest.py) fixture.

## License

This project is licensed under the [MIT license](LICENSE).
