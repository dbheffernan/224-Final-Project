# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 17:44:56 2018

@author: Dillon
"""
x = input('input and clean 2018 expense data (y/n)')
if(x=='y'):
    state_expend18 = pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\expend18.csv")
    
    state_expend18 = state_expend18.drop(['Payee Address Line 1','Payee Address Line 2', 
                                              'Payee City','Payee Zip','Expense Method','Fixed Asset'], axis=1)
    
    state_expend18.columns = state_expend.columns
    state_expend18 = state_expend18.dropna(subset=['CF_ID'])
    state_expend18.CF_ID = state_expend18.CF_ID.astype(int)
    se18 = state_expend18[state_expend18.Filing_Period == '2017 Annual']
    se18 = state_expend18[state_expend18.Filing_Period == '2017 Annual']
    se18 = se18.append(state_expend18[state_expend18.Filing_Period == '2018 Annual'])
    se18 = se18.append(state_expend18[state_expend18.Filing_Period == '2018 30 Day Primary'])
    se18 = se18.append(state_expend18[state_expend18.Filing_Period == '2018 8 Day Primary'])
    se18 = se18.append(state_expend18[state_expend18.Filing_Period == '2018 30 Day General'])
    se18 = se18.append(state_expend18[state_expend18.Filing_Period == '2018 8 Day General'])
    
    se18.Filing_Period = se18.Filing_Period.map(period_18_dict)
    state_expend18 = se18
    
    state_expend18.Amount = state_expend18.Amount.astype(float)
    smalls = state_expend18[state_expend18.Payee_Type == 'Total of Expenditures not exceeding $100']
    smalls.Payee_Name = 'small'
    smalls.Payee_State = 'DE'
    state_expend18 = state_expend18[state_expend18.Payee_Type != 'Total of Expenditures not exceeding $100']
    state_expend18 = state_expend18.append(smalls)
    state_expend18 = state_expend18.dropna()
    state_expend18.Expenditure_Date =  pd.to_datetime(state_expend18.Expenditure_Date)
    state_expend18.Payee_State = state_expend18.Payee_State.str.upper()
    state_expend18.Payee_Type = state_expend18.Payee_Type.map(dicts.contrib_dict)
    
    state_expend18['type'] = le.transform(state_expend18.Payee_Type)
    state_expend18['Month'] = state_expend18['Expenditure_Date'].dt.month
    state_expend18['Category'] = state_expend18.Expense_Purpose.map(purp_dict)
    
    good = state_expend18[state_expend18.Category != 'X']
    ugly = state_expend18[state_expend18.Category == 'X']
    ugly = ugly[(ugly.Expense_Category != 'Other Expenses') & (ugly.Expense_Category != 'Data Conversion')]
    bad = state_expend18[state_expend18.Category == 'X']
    bad = bad[(bad.Expense_Category == 'Other Expenses') | (bad.Expense_Category == 'Data Conversion')]
    ugly['Category'] = ugly.Expense_Category.map(purp_dict)
    good = good.append(ugly)
    ok = good.append(bad)
    ok = ok.dropna()
    ok['Guess'] = le2.transform(ok.Category)
    good = good.dropna()
    good['Guess'] = le2.transform(good.Category)
    
    expend_prepared = expend_prepared.transform(bad[features])
    bad['Category'] =  le2.inverse_transform(final.predict(expend_prepared))
    real_good = good.append(bad)
    state_expend18 = real_good.drop(['Guess','Month','type'],axis=1)
    state_expend18.Expense_Category = state_expend18.Category
    
x = input('input and clean 2018 contribution data (y/n)')
if(x=='y'):
    state_contrib18 = pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\contribs17.csv")
    state_contrib18 = state_contrib18.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\contribs18.csv"))
    state_contrib18 = state_contrib18.drop(['Contribution Date', 'Contributor Name', 'Contributor Address Line 1',
       'Contributor Address Line 2', 'Contributor City',
       'Contributor Zip', 'Employer Name',
       'Employer Occupation',
       'Receiving Committee',
       'Fixed Asset', 'Unnamed: 17','Contribution Type'],axis=1)
    state_contrib18.columns = ['Contributor_State', 'Contributor_Type', 'Contribution_Amount', 'CF_ID',
       'Filing_Period', 'Office']
    state_contrib18 = state_contrib18.dropna(subset = ['Office','Contributor_State'])
    sc18a = state_contrib18[state_contrib18.Filing_Period == '2017 Annual']
    sc18b = state_contrib18[state_contrib18.Filing_Period == '2018 2018 Primary 09/06/2018 30 Day']
    sc18c = state_contrib18[state_contrib18.Filing_Period == '2018 2018 Primary 09/06/2018 8 Day']
    sc18d = state_contrib18[state_contrib18.Filing_Period == '2018 2018 General 11/06/2018 30 Day']
    sc18e = state_contrib18[state_contrib18.Filing_Period == '2018 2018 General 11/06/2018 8 Day']
    sc18f = state_contrib18[state_contrib18.Filing_Period == '2018 Annual']
    sc18a.Filing_Period = 31
    sc18b.Filing_Period = 32
    sc18c.Filing_Period = 33
    sc18d.Filing_Period = 34
    sc18e.Filing_Period = 35
    sc18f.Filing_Period = 36 
    state_contrib18 = sc18a.append(sc18b).append(sc18c).append(sc18d).append(sc18e).append(sc18f)
    state_contrib18.Contributor_State = state_contrib18.Contributor_State.str.upper()
    state_contrib18.Contributor_Type = state_contrib18.Contributor_Type.map(dicts.contrib_dict)
    state_contrib18.Office = state_contrib18.Office.map(dicts.office_dict)
    state_contrib18 = state_contrib18[state_contrib18.Office != 'X']
    state_contrib18.CF_ID = state_contrib18.CF_ID.astype(int)
    state_contrib18.Contribution_Amount = state_contrib18.Contribution_Amount.astype(float)
    canlist = canlister(canlist,state_contrib18)

x = input('ugh, matching (y/n)')
if(x=='y'):
    results18p = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\18resultsp.txt")
    results18g = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\18resultsg.txt")
    p18 = text_match(results18p,canlist,state_contrib18,'2018p')
    p18 = p18.drop(['Absentee','Incumbent', 'Machine',
       'Office', 'Party', 'Percent', 'Total', 'Won', 'match'],axis=1)
    g18 = text_match(results18g,canlist,state_contrib18,'2018all')
    g18 = g18.drop(['Absentee','Incumbent', 'Machine',
       'Office', 'Party', 'Percent', 'Total', 'Won', 'match'],axis=1)
    match_list18 = p18.append(g18).drop(['total'],axis=1).drop_duplicates()
    
x = input('final processing')
if(x=='y'):
    r18p = results_processing(results18p,0,2018,state_contrib18,canlist,state_expend18,masterlist,match_list18)
    r18g = results_processing(results18g,1,2018,state_contrib18,canlist,state_expend18,masterlist,match_list18)