from slither.slither import Slither

slither = Slither("StakingContract.sol")
staking_contract = slither.get_contract_from_name("StakingContract")[0]
Ownable_transferOwnership = staking_contract.get_function_from_signature(
    "transferOwnership(address)"
)

for contract in slither.contracts:
    if staking_contract in contract.inheritance:

        transfer_ownership = contract.get_function_from_signature(
            "transferOwnership(address)"
        )
        if (
            transfer_ownership.contract != staking_contract
            and transfer_ownership.id != Ownable_transferOwnership.id
        ):
            print(
                f"Error: {transfer_ownership.contract} overrides {transfer_ownership}"
            )
