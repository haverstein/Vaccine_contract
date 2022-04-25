// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Vaccine {
    struct Citizen {
        uint256 age;
        uint256 VaccineCount;
        uint256 buffer_period;
        uint256 deadline;
    }
    mapping(address => Citizen) public Record;
    uint256 public minimum_age;
    uint256 public constant buffer = 84 days;
    uint256 public constant deadline = 28 days;
    address public owner;

    event FirstDoseDone(
        address citizen,
        uint256 buffer_duration,
        uint256 deadline_duration
    );
    event SecondDoseDone(address citizen);

    event DeadlineViolated(address citizen);

    constructor(uint256 _minimum_age) {
        minimum_age = _minimum_age;
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only Owner Can call");
        _;
    }

    function addCitizen(uint256 _age, address citizen) public {
        require(citizen != address(0), "Impossible!");
        require(Record[citizen].age == 0, "Citizen already registered!");
        require(_age >= minimum_age, "Not Eligible for vaccination");
        Record[citizen].age = _age;
        Record[citizen].VaccineCount = 0;
    }

    function firstDoze(address citizen) public onlyOwner {
        require(
            Record[citizen].VaccineCount == 0,
            "Not Eligible For First Dose"
        );
        require(
            Record[citizen].age >= minimum_age,
            "Not Eligible for vaccination"
        );
        Record[citizen].VaccineCount += 1;
        uint256 buffer_duration = block.timestamp + buffer;
        Record[citizen].buffer_period = buffer_duration;
        uint256 deadline_duration = block.timestamp + buffer + deadline;
        Record[citizen].deadline = deadline_duration;
        emit FirstDoseDone(citizen, buffer_duration, deadline_duration);
    }

    function checkstatus(address citizen)
        public
        view
        returns (
            uint256 VaccineCount,
            uint256 _buffer,
            uint256 _deadline
        )
    {
        return (
            Record[citizen].VaccineCount,
            Record[citizen].buffer_period,
            Record[citizen].deadline
        );
    }

    function checkOwner() external view returns (address) {
        return owner;
    }

    function SecondDoze(address citizen) public onlyOwner {
        require(
            Record[citizen].VaccineCount == 1,
            "Not Eligible For Second Dose"
        );
        require(
            block.timestamp > Record[citizen].buffer_period,
            "Not Ready for second Doze"
        );
        if (block.timestamp > Record[citizen].deadline) {
            Record[citizen].VaccineCount = 0;
            emit DeadlineViolated(citizen);
        } else {
            Record[citizen].VaccineCount += 1;
            emit SecondDoseDone(citizen);
        }
    }
}
