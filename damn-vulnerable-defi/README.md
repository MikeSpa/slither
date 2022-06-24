# Vulnerabilities found by Slither in DamnVunerableDeFi

## 1) Unstoppable

Slither's detectors found the vulnerability:
```solidity
assert(poolBalance == balanceBefore);
```

UnstoppableLender.flashLoan(uint256) (unstoppable/UnstoppableLender.sol#32-53) uses a dangerous strict equality:
        - assert(bool)(poolBalance == balanceBefore) (unstoppable/UnstoppableLender.sol#39)
Reference: https://github.com/crytic/slither/wiki/Detector-Documentation#dangerous-strict-equalities

## 2) Naive Receiver

Detector can't find the vulnerability but we can write a simple script that check whether the contract has an accessable function (`public`, `external` with no `onlyOwner()` modifier) that makes a risky call, i.e. `transfer()` or `approve()`.

## 3) Truster

Slither give us a hint:
TrusterLenderPool.flashLoan(uint256,address,address,bytes) (truster/TrusterLenderPool.sol#23-40) ignores return value by target.functionCall(data) (truster/TrusterLenderPool.sol#36)
Reference: https://github.com/crytic/slither/wiki/Detector-Documentation#unused-return

But the script for the last challenge show us the call that allow the exploit:
```solidity
target.functionCall(data);
```

## 4) Side Entrance

Here there is not much we can do with Slither.

## 5) The Rewarder

Not applicable

## 6) Selfie

Not applicable

## 7) Compromised

Not applicable

## 10) Free Rider

Slither immediately detects the main vulnerability: Detect the use of msg.value inside a loop.

```solidity
function buyMany(uint256[] calldata tokenIds) external payable nonReentrant {
    for (uint256 i = 0; i < tokenIds.length; i++) {
        _buyOne(tokenIds[i]);
    }
}

function _buyOne(uint256 tokenId) private {       
    uint256 priceToPay = offers[tokenId];
    require(priceToPay > 0, "Token is not being offered");

    // HERE
    require(msg.value >= priceToPay, "Amount paid is not enough");

    amountOfOffers--;

    // transfer from seller to buyer
    token.safeTransferFrom(token.ownerOf(tokenId), msg.sender, tokenId);

    // pay seller
    payable(token.ownerOf(tokenId)).sendValue(priceToPay);

    emit NFTBought(msg.sender, tokenId, priceToPay);
}    
```
The contract should track msg.value through a local variable and decrease its amount on every iteration/usage.


FreeRiderNFTMarketplace._buyOne(uint256) (free-rider/FreeRiderNFTMarketplace.sol#68-83) use msg.value in a loop: require(bool,string)(msg.value >= priceToPay,Amount paid is not enough) (free-rider/FreeRiderNFTMarketplace.sol#72)
Reference: https://github.com/crytic/slither/wiki/Detector-Documentation/#msgvalue-inside-a-loop
