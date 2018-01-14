pragma solidity ^0.4.18;

contract Doctor {

   event NewPatient(uint id, string name);

   string doctorID;
   string fName;
   string lName;
   string DOB;
   string gender;
   string homeAddress;
   string email;
   string homePhone;
   uint age;

   struct Patient {
        string name;
        uint id;
    }

    Patient[] public newPatients;
    mapping (uint => address) public idToPatient;

    function _createPatient(string _name, uint _id) private {
         uint id = newPatients.push(Patient(_name, _id)) - 1;
         ombieToOwner[id] = msg.sender;
         NewPatient(id, _name);
     }
}
