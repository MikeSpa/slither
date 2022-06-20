from slither.slither import Slither

slither = Slither("StakingContract.sol")
staking_contract = slither.get_contract_from_name("StakingContract")[0]
whitelist = [
    "constructor(address,address)",
    "owner()",
    "getUserTotalValue(address)",
    "getUserSingleTokenValue(address,address)",
    "getTokenValue(address)",
    "stakeTokens(uint256,address)",
    "unstakeTokens(address)",
    "tokenIsAllowed(address)",
]

for function in staking_contract.functions:
    if function.full_name in whitelist:
        continue
    if function.visibility in ["public", "external"]:
        if not "onlyOwner()" in [m.full_name for m in function.modifiers]:
            print(function.full_name)
