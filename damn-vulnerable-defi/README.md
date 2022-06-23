# Vulnerabilities found by Slither in DamnVunerableDeFi

## 1) Unstoppable

Slither's detectors found the vulnerability:
```solidity
assert(poolBalance == balanceBefore);
```

UnstoppableLender.flashLoan(uint256) (unstoppable/UnstoppableLender.sol#32-53) uses a dangerous strict equality:
        - assert(bool)(poolBalance == balanceBefore) (unstoppable/UnstoppableLender.sol#39)
Reference: https://github.com/crytic/slither/wiki/Detector-Documentation#dangerous-strict-equalities

