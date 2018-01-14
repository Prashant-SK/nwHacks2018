pragma solidity ^0.4.18;

contract Patient {

   string publicID;
   string fName;
   string lName;
   string DOB;
   string gender;
   string homeAddress;
   string email;
   string homePhone;
   uint age;

   function setPatient(string _publicID, string _fName, string _lName, string _DOB, string _gender, string _homeAddress, string _email, string _homePhone, uint _age) public {
       publicID = _publicID;
       fName = _fName;
       lName = _lName;
       DOB = _DOB;
       gender = _gender;
       homeAddress = _homeAddress;
       email = _email;
       homePhone = _homePhone;
       age = _age;
   }

   function getPatientInfoOne() public constant returns (string, string, string, string, string ) {
       return (publicID, fName, lName, DOB, gender);
   }

    function getPatientInfoTwo() public constant returns (string, string, string, uint) {
       return (homeAddress, email, homePhone, age);
   }
}
