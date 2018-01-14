pragma solidity ^0.4.19;

contract Login {

    string uName;
    string pass;
    
    function setLogin(string _uName, string _pass) {
        uName = _uName;
        pass = _pass;
    }
    
    function verifyLogin(string _uName, string _pass) public returns (bool) {
        require(keccak256(_uName) == keccak256(uName));
        require(keccak256(_pass) == keccak256(pass));
    return true;
    }

}
