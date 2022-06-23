# check if a function in a given contract is external or public and send funds to the outside

from slither.slither import Slither

slither = Slither("naive-receiver/FlashLoanReceiver.sol")
receiver = slither.get_contract_from_name("FlashLoanReceiver")[0]

# list of calls that may send contract's funds outside
risky_calls = [
    "transfer(",
    "send(",
    "sendValue(",
    "selfdestruct(",
    "approve(",
    "call(",
    "call{",
    "functionCall(",
    "functionCallWithValue",
]
for function in receiver.functions:

    if function.visibility in ["public", "external"]:
        if not "onlyOwner()" in [m.full_name for m in function.modifiers]:
            for n in function.nodes:
                for risky_call in risky_calls:
                    if risky_call in str(n.expression):
                        print(f"Risk: {n.expression}")
