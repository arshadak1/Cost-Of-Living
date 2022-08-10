from decimal import Decimal
from django.contrib.auth.models import User
from .models import Data
import json, datetime, re

# regex for email validation
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# regex for password validation
PASS_REGEX = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,35}$"

MONTHS = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 
            7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

# check whether the email is valid or not
def emailValidation(email):
    return True if re.fullmatch(EMAIL_REGEX, email) else False

# check whether the password meets the criteria
def _passValidation(password):
    return True if re.match(PASS_REGEX, password) else False

# helper function to fetch data for populating the profile form
def _updateProfile(request, curr_data, curr_user):

    # datas that entered by the user in the profile form
    username = request.POST['username']
    email = request.POST['email']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    password = request.POST['password']
    confirm_password = request.POST['confirm-password']

    # checking whether user changed the existing username
    if curr_user.username != str(username).strip():
        # checking whether the newly entered username is unique or not
        if not User.objects.filter(username=username).exists():
            curr_user.username = str(username).strip()
        else:
            # if newly enterd username is not unique, there should be a username error
            curr_data['usernameError'] = True

    # checking whether user changed the existing email
    if curr_user.email != str(email).strip():
        # checking whether the newly entered email is unique or not
        if not User.objects.filter(email=email).exists():
            if emailValidation(str(email).strip()):
                curr_user.email = email
            else:
                curr_data['emailMsg'] = 'Please enter a valid email!'
                curr_data['emailError'] = True

        else:
            # if newly enterd email is not unique, there should be a email error
            curr_data['emailMsg'] = 'Email already exist!'
            curr_data['emailError'] = True

    # checking the password
    if password != confirm_password:
        curr_data['passSameErr'] = True
    
    # checking whether the password meets the criteria
    elif str(password).strip() != '' and _passValidation(password):
        curr_data['passValidErr'] = True

    # when there is an emailError or usernameError we have stop the form being updated to the database
    if curr_data['emailError'] or curr_data['usernameError'] or curr_data['passSameErr'] or curr_data['passValidErr']:
        # sending the error msg and cls
        curr_data['form_message'] = 'Something went wrong!'
        curr_data['form_msg_class'] = 'form-msg failure-alert'

        # populating the profile field with all the things that user entered
        curr_data['username'] = str(username).strip()
        curr_data['email'] = str(email).strip()
        curr_data['firstname'] = str(firstname).strip()
        curr_data['lastname'] = str(lastname).strip()

        # we return the data here as we have to break the function before saving the data to database
        return curr_data

    # if there is no errors then we just show a success msg
    else:
        curr_data['form_message'] = 'Successfully updated!'
        curr_data['form_msg_class'] = 'form-msg success-alert'

    # updating the user informations
    curr_user.first_name = firstname
    curr_user.last_name = lastname
    if str(password).strip() != '' and password == confirm_password:
        curr_user.set_password(password)
    
    #saving the user information
    curr_user.save()

    # updating the context variable
    curr_data['username'] = str(username).strip()
    curr_data['email'] = str(email).strip()
    curr_data['firstname'] = str(firstname).strip()
    curr_data['lastname'] = str(lastname).strip()

    return curr_data

# helper function to get the data required for plotting the graph
def _graph_data(request):
    TODAY = datetime.date.today()
    graph_context = {}
    # data assoiciated with the current logged in user
    data_list = Data.objects.filter(user=request.user)
    graph_context['data_list'] = data_list
    income = 0
    expense = 0
    # Data required for 'chartJS'
    doughnut_js_data = {}
    smallest_date = TODAY
    for data in data_list:
        if data.per == 'month':
            data.value *= 12
        elif data.per == 'week':
            data.value *= 52
        elif data.per == 'day':
            data.value *= 365
        
        
        doughnut_js_data[data.title] = (str(data.value), data.is_expense)
        if data.is_expense == 'Expense':
            expense += data.value
        else:
            income += data.value
        
        if data.Date < smallest_date:
            smallest_date = data.Date

    monthly_js_data = {}
    currDate = smallest_date
    month_number = TODAY.month
    data_to_be_repeated = []
    
    while month_number > 0 and currDate <= TODAY:
        month_exceeded = False 
        total_expense_curr_month = 0
        nextMonth = (currDate.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        if nextMonth > TODAY or currDate == TODAY:
            month_exceeded = True
            nextMonth = TODAY
        data_monthly_list = Data.objects.filter(user=request.user, Date__gte=currDate, Date__lt=nextMonth, is_expense='Expense')
        for repeated_data in data_to_be_repeated:
            total_expense_curr_month += repeated_data
        for data in data_monthly_list:
            if data.per == 'month':
                data_to_be_repeated.append(data.value)
                total_expense_curr_month += data.value
            elif data.per == 'week':
                data_to_be_repeated.append(data.value * 4)
                total_expense_curr_month += data.value * 4

            elif data.per == 'day':
                data_to_be_repeated.append((data.value) * Decimal(30.42))
                total_expense_curr_month += (data.value) * Decimal(30.42)
            elif data.per == 'year':
                data_to_be_repeated.append(data.value / 12)
                total_expense_curr_month += data.value / 12
            else:
                total_expense_curr_month += data.value

        monthly_js_data[currDate.month] = str(total_expense_curr_month)
        if month_exceeded:
            currDate = TODAY + datetime.timedelta(days=5)

        else:    
            currDate = nextMonth
        month_number -= 1
    monthly_js_data = json.dumps(monthly_js_data)
    doughnut_js_data = json.dumps(doughnut_js_data)
    graph_context['monthly_js_data'] = monthly_js_data 
    graph_context['total_net_income'] = income
    graph_context['total_net_expense'] = expense
    graph_context['doughnut_js_data'] = doughnut_js_data

    return graph_context


def humanReadableNumber(number):
    human_readable = number
    if 1000 <= number < 1000000:
        number /= 1000
        number = round(number, 2)
        human_readable = f'{number}k'
    elif 1000000 <= number < 1000000000:
        number /= 1000000
        number = round(number, 2)
        human_readable = f'{number}m'
    elif 1000000000 <= number < 1000000000000:
        number /= 1000000000
        number = round(number, 2)
        human_readable = f'{number}b'
    elif number >= 1000000000000:
        number /= 1000000000000
        number = round(number, 2)
        human_readable = f'{number}t'
    
    return human_readable
    