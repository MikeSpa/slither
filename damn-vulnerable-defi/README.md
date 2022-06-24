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

