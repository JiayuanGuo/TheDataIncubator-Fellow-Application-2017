import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime

#read and concat the dataset of 2014 and 2015
loan_2014 = pd.read_csv('LoanStats3c_2014.csv',header = 1, low_memory=False)
loan_2015 = pd.read_csv('LoanStats3d_2015.csv',header = 1, low_memory=False)
loan = pd.concat([loan_2014.iloc[:-2],loan_2015.iloc[:-2]]).reset_index(drop = True)

#--------------------------------------
#What is the median loan amount?
#1st calculate median  13750.0
median_loan_amnt = np.median(loan['loan_amnt'])

#--------------------------------------
#Each loan is categorized into a single purpose. What fraction of all loans are for the most common purpose?

#get purpose list
start = time.time()

purpose_list = []
for i in range(len(loan)):
    if loan['purpose'][i] not in purpose_list:
        purpose_list.append(loan['purpose'][i])

print(purpose_list)

end = time.time()
run_time = end - start
print(run_time)

#get purpose counts
purpose_count_dict = {}
for i in purpose_list:
    purpose_count = len(loan[loan['purpose'] == i])
    purpose_count_dict['%s' % i] = purpose_count
purpose_count_dict

#calculate the fraction of the most common purpose
frac_common_purpose = max(purpose_count_dict.values())/sum(purpose_count_dict.values())
frac_common_purpose

#--------------------------------------
#Calculate the average interest rate across loans for each purpose.
# What is the ratio of minimum average rate to the maximum average rate? (The ratio should be less than 1.)

#calculate the average interest rate for each purpose
avg_int_rate_dict = {}
for j in purpose_list:
    purpose_df = loan[loan['purpose'] == j]
    int_rate_list = []
    for i in purpose_df['int_rate']:
        int_rate = float(i.split('%')[0].split()[0])
        int_rate_list.append(int_rate)
    avg_int_rate = np.mean(int_rate_list)
    #avg_int_rate_list.append(avg_int_rate)
    avg_int_rate_dict['%s' % j] = avg_int_rate

#calculate the ratio of minimum average rate to the maximum average rate 0.63997977670622108
min_int_rate = min(list(avg_int_rate_dict.values()))
max_int_rate = max(list(avg_int_rate_dict.values()))
ratio = min_int_rate/max_int_rate


#--------------------------------------
#What is the difference in the fraction of the loans with a 36-month term between 2014 and 2015?
# The fraction of the loans with a 36-month term in 2014
term_36_2014 = 0
for i in loan_2014.iloc[:-2]['term']:
    if i.split()[0] == '36':
        term_36_2014 += 1

frac_36_2014 = term_36_2014 / len(loan_2014.iloc[:-2])

# he fraction of the loans with a 36-month term in 2015
term_36_2015 = 0
for i in loan_2015.iloc[:-2]['term']:
    if i.split()[0] == '36':
        term_36_2015 += 1

frac_36_2015 = term_36_2015 / len(loan_2015.iloc[:-2])

#calculate the difference in the fraction of the loans with a 36-month term between 2014 and 2015?
dif_frac = frac_36_2014 - frac_36_2015

#--------------------------------------
#We will consider all loans that are not in the 'Fully Paid', 'Current', 'In Grace Period' statuses to be in default.
# Calculate the ratio of the time spent paying the loan, defined as the difference between the last payment date
# and the issue date, divided by the term of loan.
# What is the standard deviation of this ratio for all the loans in default?
#replace all loans that are not in the 'Fully Paid', 'Current', 'In Grace Period' statuses to be in default.
non_default_status = ['Fully Paid','Current','In Grace Period']

default_status = []
for i in loan['loan_status']:
    if i not in non_default_status and i not in default_status:
        default_status.append(i)

loan['loan_status'].replace(default_status, 'Default',inplace=True)

# the data of the last payment date is in column 'last_pymnt_d'
# the data of the issue date is in column 'issue_d'
# select default loan data and drop NaN in column 'last_pymnt_d'
df_1 = loan[loan['loan_status'] == 'Default'][['last_pymnt_d','issue_d','term']].dropna().reset_index(drop=True)

#change date format from 'Aug-2016' to '08-2016'
org_month_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
new_month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']

new_pymnt_dlist = []
for i in df_1['last_pymnt_d']:
    month_index = org_month_list.index(i.split('-')[0])
    new_format_d = new_month_list[month_index] + '-' + i.split('-')[1]
    new_pymnt_dlist.append(new_format_d)
df_1['new_last_pymnt_d'] = new_pymnt_dlist

new_issue_dlist = []
for i in df_1['issue_d']:
    month_index = org_month_list.index(i.split('-')[0])
    new_format_d = new_month_list[month_index] + '-' + i.split('-')[1]
    new_issue_dlist.append(new_format_d)
df_1['new_issue_d'] = new_issue_dlist

# calculate ratio
ratio_list = []
for i in range(len(df_1.iloc[:100])):
    f = "%m-%Y"
    datetime_1 = datetime.strptime(df_1['new_last_pymnt_d'][i], f)
    datetime_2 = datetime.strptime(df_1['new_issue_d'][i], f)
    delta = datetime_1 - datetime_2
    delta_month = int(delta.days / 30)

    loan_term = int(df_1['term'][i].split()[0])
    ratio = delta_month / loan_term

    ratio_list.append(ratio)

#calculate standard deviation 0.19551464218477854
std = np.std(ratio_list)


#--------------------------------------
#Let's find a loan purpose that shows up abnormally often in one state.
# Call A the probability of a loan going to a specific purpose nationwide.
# Call B the probability of a loan going to a specific purpose for each state.
# Out of all (state, purpose) pairs with at least 10 loans,
# what is the highest ratio of B / A (i.e. the most surprising)?

#get the probability of a loan going to a specific purpose nationwide
purpose_prob_nation_dict = {}
for i in purpose_count_dict:
    purpose_prob_nation = purpose_count_dict[i]/sum(purpose_count_dict.values())
    purpose_prob_nation_dict[i] = purpose_prob_nation

#get states list
start = time.time()

states_list = []
for i in range(len(loan)):
    if loan['addr_state'][i] not in states_list:
        states_list.append(loan['addr_state'][i])

print(states_list)

end = time.time()
run_time = end - start
print(run_time)

# get the probability of a loan going to a specific purpose for each state
start = time.time()

df_state_prob = pd.DataFrame()
pair_list = []
statecount_list = []
stateprob_list = []
for i in states_list:

    df_state = loan[loan['addr_state'] == i]

    sub_pair_list = []
    sub_statecount_list = []
    sub_stateprob_list = []
    for j in purpose_list:
        pair = (i, '%s' % j)
        sub_pair_list.append(pair)

        statecount = len(df_state[df_state['purpose'] == j])
        sub_statecount_list.append(statecount)

        stateprob = statecount / len(df_state)
        sub_stateprob_list.append(stateprob)

    pair_list.extend(sub_pair_list)
    statecount_list.extend(sub_statecount_list)
    stateprob_list.extend(sub_stateprob_list)

df_state_prob['pair'] = pair_list
df_state_prob['count'] = statecount_list
df_state_prob['prob'] = stateprob_list

end = time.time()
run_time = end - start
print(run_time)

#select df with (state, purpose) pairs with at least 10 loans
df_selected = df_state_prob[df_state_prob['count'] >= 10].reset_index(drop = True)

pair_prob_dict = dict(zip(df_selected['pair'], df_selected['prob']))

#calculate the highest ratio of B / A (i.e. the most surprising)
max_ratio_list = []
for j in purpose_list:
    A = purpose_prob_nation_dict[j]
    ratio_list = []
    for i in states_list:
        if (i,j) in list(df_selected['pair']):
            B = pair_prob_dict[(i,j)]
            ratio_BA = B/A
            ratio_list.append(ratio_BA)
    if ratio_list != []:
        max_ratio = max(ratio_list)
        max_ratio_list.append(max_ratio)
highest_ratio = max(max_ratio_list)




