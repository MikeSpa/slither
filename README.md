# Slither

repo to learn/test the static analysis tools slither.


## [Usage](https://github.com/crytic/slither/wiki/Usage)

```bash
slither .
```
Slither runs all its [detectors](https://github.com/crytic/slither/wiki/Detector-Documentation) by default.

By default, no [printers](https://github.com/crytic/slither/wiki/Printer-Documentation) are run.


### Configuration

Some options can be set through a json configuration file. By default, slither.config.json is used if present (it can be changed through --config-file file.config.json).

Options passed via the CLI have priority over options set in the configuration file.

The following flags are supported:
```json
{
    "detectors_to_run": "detector1,detector2",
    "printers_to_run": "printer1,printer2",
    "detectors_to_exclude": "detector1,detector2",
    "exclude_informational": false,
    "exclude_low": false,
    "exclude_medium": false,
    "exclude_high": false,
    "json": "",
    "disable_color": false,
    "filter_paths": "file1.sol,file2.sol",
    "legacy_ast": false
}
```

# Vunerabilities found in StakingContract

## Uncheck-transfer
[Docs](https://github.com/crytic/slither/wiki/Detector-Documentation#unchecked-transfer)

Several tokens do not revert in case of failure and return false. If one of these tokens is used in `stakeTokens()`, it will not revert if the transfer fails, and an attacker can increase its `stakingBalance` for free.

```solidity
function stakeTokens(uint256 _amount, address _token) external {
    //...
    IERC20(_token).transferFrom(msg.sender, address(this), _amount);
    stakingBalance[_token][msg.sender] =
        stakingBalance[_token][msg.sender] +
        _amount;

    //...
}
```
Fix:
```solidity
function stakeTokens(uint256 _amount, address _token) external {
    //...
    require(
        IERC20(_token).transferFrom(msg.sender, address(this), _amount),
        "StakingContract: transferFrom() failed"
    );
    stakingBalance[_token][msg.sender] =
        stakingBalance[_token][msg.sender] +
        _amount;

    //...
}
```

## Unused-return
[Docs](https://github.com/crytic/slither/wiki/Detector-Documentation#unused-return)

Similar to uncheck-transfer except more general. The return value of an external call is not stored in a local or state variable.

## Reentrancy-benign
[Docs](https://github.com/crytic/slither/wiki/Detector-Documentation#reentrancy-vulnerabilities-2)  
Reentrancy that acts as a double call:

```solidity
function stakeTokens(uint256 _amount, address _token) external {
    require(_amount > 0, "StakingContract: Amount must be greater than 0");
    require(
        tokenIsAllowed(_token),
        "StakingContract: Token is currently no allowed"
    );
    require(
        IERC20(_token).transferFrom(msg.sender, address(this), _amount),
        "StakingContract: transferFrom() failed"
    );
    _updateUniqueTokensStaked(msg.sender, _token);
    stakingBalance[_token][msg.sender] =
        stakingBalance[_token][msg.sender] +
        _amount;

    // add user to stakers list pnly if this is their first staking
    if (uniqueTokensStaked[msg.sender] == 1) {
        stakers.push(msg.sender);
    }

    //deposit on lending protocol
    lendingProtocol.deposit(_token, _amount, address(this));
    emit TokenStaked(_token, msg.sender, _amount);
}
```
But you cannot really exploit this reentrancy plus the external call `transferFrom()` is only executed on trusted and pre-approved token addresses.

## Reentrancy-events
[Docs](https://github.com/crytic/slither/wiki/Detector-Documentation#reentrancy-vulnerabilities-3)  
Reentrancies leading to out-of-order events.

```solidity
function addAllowedTokens(address _token) external onlyOwner {
    allowedTokens.push(_token);
    require(
        IERC20(_token).approve(address(lendingProtocol), type(uint256).max),
        "StakingContract: approve() failed"
    );
    emit TokenAdded(_token);
}
```
Here again, external calls are always on approved token addresses.

# Optimizations in StakingContract

## External-function
[Docs](https://github.com/crytic/slither/wiki/Detector-Documentation#public-function-that-could-be-declared-external)  
public functions that are never called by the contract should be declared external to save gas.

`function unstakeTokens(address _token) external` intead of `function unstakeTokens(address _token) public`.

## Costly-loop
[Docs](https://github.com/crytic/slither/wiki/Detector-Documentation#costly-operations-inside-a-loop)

Costly operations inside a loop might waste gas, so optimizations are justified.
```solidity
for (uint256 i = 0; i < stakers.length; i++) {
    if (stakers[i] == msg.sender) {
        stakers[i] = stakers[stakers.length - 1];
        stakers.pop(); //expensive
        break;
    }
}
```
But even though the costly operation is in a loop, we only do it once. But we can add a `break` to exit the loop earlier



# Vunerabilities found in AaveLending

## Unchecked-transfer

Similar to StakingContract.

## Unused-return

```solidity
function withdraw(address _token,uint256 _amount,address _to)
    external
    override(ILendingProtocol)
    onlyStakingContract
    returns (uint256)
{
    
    pool.withdraw(_token, _amount, _to); //unsued return value

    return _amount_;
}
```
Fix:
```solidity
function withdraw(address _token,uint256 _amount,address _to)
    external
    override(ILendingProtocol)
    onlyStakingContract
    returns (uint256)
{
    
    uint256 amountWithdrawn = pool.withdraw(_token, _amount, _to);

    return amountWithdrawn;
}
```
We need to use the return value of `withdraw()` to return it to `StakingContract`. `_amount` is not always the amount of funds that is withdrawn.


# Optimizations found in AaveLending

## Events-access
[Docs](https://github.com/crytic/slither/wiki/Detector-Documentation#missing-events-access-control)

Detect missing events for critical access control parameters.  
setStakingContract() has no event, so it is difficult to track off-chain staking contract changes.
```solidity
function setStakingContract(address _stakingContract) external onlyOwner {
    stakingContract = _stakingContract;
}
```
Fix:
```solidity
event StakingContractChange(address newContract);
function setStakingContract(address _stakingContract) external onlyOwner {
    stakingContract = _stakingContract;
    emit StakingContractChange(_stakingContract);
}
```
## Missing-zero-check
[Docs](https://github.com/crytic/slither/wiki/Detector-Documentation#missing-zero-address-validation)

Detect missing zero address validation.

```solidity
function setStakingContract(address _stakingContract) external onlyOwner {
    stakingContract = _stakingContract;
    emit StakingContractChange(_stakingContract);
}
```
Fix:
```solidity
function setStakingContract(address _stakingContract) external onlyOwner {
    require(
        _stakingContract != address(0),
        "AaveLending: address given is 0x0"
    );
    stakingContract = _stakingContract;
    emit StakingContractChange(_stakingContract);
}
```
We simply add a check to make sure the new address is not 0x0.

## External-function

Similar to StakingContract.


