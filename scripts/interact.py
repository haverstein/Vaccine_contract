from brownie import Vaccine
from scripts.helpful_scripts import get_account, convert_to_date_time
import datetime
import time

minimum_age = 18
account = get_account()


def deploy():
    print("Vaccine Contract coming soon!")
    vaccine_contract = Vaccine.deploy(minimum_age, {"from": account})
    print("Deployed the vaccine!")
    return vaccine_contract


def register_citizen(citizen, age, vaccine_contract):
    if age > minimum_age:
        print(f"Registering {citizen}!")
        tx = vaccine_contract.addCitizen(age, citizen, {"from": account})
        tx.wait(1)
        print(f"Added {citizen} successfully!")
        return tx
    else:
        print(f"{citizen} not old enough!")


def first_doze(citizen, vaccine_contract):
    tx = vaccine_contract.firstDoze(citizen, {"from": account})
    tx.wait(1)
    print(f"Congratulations! {citizen} have taken the first doze!")
    buffer_duration = tx.events["FirstDoseDone"]["buffer_duration"]
    deadline_duration = tx.events["FirstDoseDone"]["deadline_duration"]
    (buffer_year, buffer_month, buffer_day) = convert_to_date_time(buffer_duration)
    print(
        f"You can take your second doze after {buffer_day}th {buffer_month}, {buffer_year}"
    )
    (deadline_year, deadline_month, deadline_day) = convert_to_date_time(
        deadline_duration
    )
    print(
        f"You should take your second doze before {deadline_day}th {deadline_month}, {deadline_year} , otherwise you have to take the first doze and then the second one!"
    )
    return (tx, buffer_duration, deadline_duration)


def second_doze(citizen, vaccine_contract):
    tx = vaccine_contract.SecondDoze(citizen, {"from": account})
    tx.wait(1)
    try:
        if tx.events["DeadlineViolated"]:
            print(
                f"{citizen} have violated his/her deadline. You have to take the first doze again and then the second doze"
            )
    except:
        print(f"{citizen} have completed his vaccines! Well done!")
    return tx


def check_status(citizen, vaccine_contract):
    (vaccine_count, buffer, deadline) = vaccine_contract.checkstatus(
        citizen, {"from": account}
    )
    st = " vaccine"
    if vaccine_count > 0:
        st = " vaccines"
    print(f"You have taken {vaccine_count} {st}")
    (buffer_year, buffer_month, buffer_day) = convert_to_date_time(buffer)
    print(
        f"You have to take your second doze after {buffer_day}th {buffer_month}, {buffer_year}"
    )
    (deadline_year, deadline_month, deadline_day) = convert_to_date_time(deadline)
    print(
        f"Your deadline to take the second doze is {deadline_day}th {deadline_month}, {deadline_year}"
    )


def check_owner(vaccine_contract):
    owner = vaccine_contract.checkOwner({"from": account})
    print(f"{owner} is the owner of this contract!")


def main():
    deploy()
    STATIC_AGE = 45
    vaccine_contract = Vaccine[-1]
    check_owner(vaccine_contract)
    register_citizen(account, STATIC_AGE, vaccine_contract)
    first_doze(account, vaccine_contract)
    time.sleep(3)
    check_status(account, vaccine_contract)
    second_doze(account, vaccine_contract)
    check_status(account, vaccine_contract)
