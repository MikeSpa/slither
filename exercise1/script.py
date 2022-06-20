from slither.slither import Slither

slither = Slither("coin.sol")
coin = slither.get_contract_from_name("Coin")[0]
coin_mint_function = coin.get_function_from_signature("_mint(address,uint256)")

for contract in slither.contracts:
    if coin in contract.inheritance:

        mint_fct = contract.get_function_from_signature("_mint(address,uint256)")
        # add the id comparison so MyCoin3 is not detected as overiding the _mint function
        if mint_fct.contract != coin and mint_fct.id != coin_mint_function.id:
            print(f"Error: {mint_fct.contract} overrides {mint_fct}")
