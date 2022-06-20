//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.5.0;

contract Coin {
    address owner = msg.sender;

    mapping(address => uint256) balances;

    // _mint must not be overriden
    function _mint(address dst, uint256 val) internal {
        require(msg.sender == owner);
        balances[dst] += val;
    }

    function mint(address dst, uint256 val) public {
        _mint(dst, val);
    }
}

contract MyCoin is Coin {
    event Mint(address, uint256);

    function _mint(address dst, uint256 val) internal {
        balances[dst] += val;
        emit Mint(dst, val);
    }
}

contract MyCoin2 is MyCoin {
    function set(address dst, uint256 val) internal {
        balances[dst] = val;
    }
}

contract MyCoin3 is Coin {
    function set(address dst, uint256 val) internal {
        balances[dst] = val;
    }
}

contract MyCoin4 {
    function _mint(address dst, int256 val) public {}
}

contract NotCoin {
    address notowner;

    function _mint(address dst, uint256 val) internal {}
}
