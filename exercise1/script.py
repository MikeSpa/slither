from slither.slither import Slither

slither = Slither("coin.sol")
coin_contract = slither.get_contract_from_name("Coin")[0]
print(coin_contract)

for contract in slither.contracts:
    if coin_contract in contract.inheritance:
        mint_fct = contract.get_function_from_signature("_mint(address,uint256)")
        print(mint_fct)
        if mint_fct.contract != coin_contract:
            print(f"A bug is found: {mint_fct.contract} - {mint_fct}")
