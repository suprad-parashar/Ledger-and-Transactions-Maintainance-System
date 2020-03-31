import re as regex
# A lambda function to check if the email address passed is valid or not.
isEmailValid = lambda email: True if email == "" else regex.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email)

# A method to check if a given date is valid.
def isDateValid(date):
    if date == "":
        return True
    isLeapYear = lambda year: (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
    try:
        dates = list(map(int, date.split("/")))
        if dates[1] == 2:
            if isLeapYear(dates[2]) and dates[0] in range(1, 30):
                return True
            elif (not isLeapYear) and dates[0] in range(1, 29):
                return True
            else:
                return False
        elif dates[1] in [1, 3, 5, 7, 8, 10, 12] and dates[0] in range(1, 32):
            return True
        elif dates[1] not in [1, 3, 5, 7, 8, 10, 12] and dates[0] in range(1, 31):
            return True
        else:
            return False
    except:
        return False

# A method to check if the passed phone number is valid or not.
def isPhoneValid(phone):
    if phone == "":
        return True
    if phone[0] not in ['6', '7', '8', '9']:
        return False
    elif len(phone) != 10:
        return False
    else:
        for c in phone:
            if not c.isdigit():
                return False
        return True