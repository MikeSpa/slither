//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./ERC20.sol";

contract ProjectToken is ERC20 {
    constructor() ERC20("Project Token", "PJTK") {
        _mint(msg.sender, 1 * 10**6 * 10**18);
    }
}
