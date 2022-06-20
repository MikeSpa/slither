from slither.slither import Slither

slither = Slither("coin.sol")
coin = slither.get_contract_from_name("Coin")[0]
whitelist = ["balanceOf(address)", "constructor()"]

for function in coin.functions:
    if function.full_name in whitelist:
        continue
    if function.visibility in ["public", "external"]:
        if not "onlyOwner()" in [m.full_name for m in function.modifiers]:
            print(function.full_name)
