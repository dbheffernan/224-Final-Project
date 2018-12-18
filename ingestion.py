# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 17:43:41 2018

@author: Dillon
"""

import numpy as np
import pandas as pd
import dicts
import doe_parse
import utilities
import processing

x = input('input candidate list? (y/n)')
if(x=='y'):
    canlist = pd.read_csv(r"canlistv3.csv")
    canlist = canlist.drop(['Committee_Type','Office','Committee_Status','Registered_Date','Amended_Date','Treasurer_Name','Treasurer_Address','County'],axis=1)
    canlist = canlist.drop_duplicates()
    
x = input('input master list? (y/n)')
if(x=='y'):
     masterlist = pd.read_csv(r"masterli.csv",index_col ='Office')
x = input('input state contribution data? (y/n)')
if(x=='y'):
    state_contribs = pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\contribs08.csv")
    state_contribs = state_contribs.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\contribs10.csv"))
    state_contribs = state_contribs.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\contribs12.csv"))
    state_contribs = state_contribs.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\contribs13.csv"))
    state_contribs = state_contribs.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\contribs14.csv"))
    state_contribs = state_contribs.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\contribs15.csv"))
    state_contribs = state_contribs.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\contribs16.csv"))
    

x = input('clean state contrib data? (y/n)')
if(x=='y'):    
    state_contribs = state_contribs.drop(['Contribution Date', 'Contributor Name', 'Contributor Address Line 1',
       'Contributor Address Line 2', 'Contributor City',
       'Contributor Zip', 'Employer Name',
       'Employer Occupation',
       'Receiving Committee',
       'Fixed Asset', 'Unnamed: 17','Contribution Type'],axis=1)
    state_contribs.columns = ['Contributor_State', 'Contributor_Type', 'Contribution_Amount', 'CF_ID',
       'Filing_Period', 'Office']
    state_contribs = state_contribs.dropna(subset = ['Office','Contributor_State'])
    data = pd.DataFrame()
    for index, item in dicts.periods.iteritems():
        period = state_contribs[state_contribs.Filing_Period == item]
        period.Filing_Period = index
        data = data.append(period, ignore_index = True)
    state_contribs = data
    state_contribs.Contributor_State = state_contribs.Contributor_State.str.upper()
    state_contribs.Contributor_Type = state_contribs.Contributor_Type.map(dicts.contrib_dict)
    state_contribs.Office = state_contribs.Office.map(dicts.office_dict)
    state_contribs = state_contribs[state_contribs.Office != 'X']
    state_contribs.CF_ID = state_contribs.CF_ID.astype(int)
    state_contribs.Contribution_Amount = state_contribs.Contribution_Amount.astype(float)

x = input('update candidate list with contributions (y/n)')
if(x=='y'):
    canlist = utilities.canlister(canlist,state_contribs)
    
x = input('input raw state expend data?')
if(x=='y'): 
    state_expend = pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\08expend.csv")
    state_expend = state_expend.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\09expend.csv"))
    state_expend = state_expend.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\10expend.csv"))
    state_expend = state_expend.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\11expend.csv"))
    state_expend = state_expend.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\12expend.csv"))
    state_expend = state_expend.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\13expend.csv"))
    state_expend = state_expend.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\14expend.csv"))
    state_expend = state_expend.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\15expend.csv"))
    state_expend = state_expend.append(pd.read_csv(r"C:\Users\Dillon\Documents\chris_data\16expend.csv"))
x = input('clean state expend data? (y/n)')
if(x=='y'):     
    #ystate_expend = state_expend.append(state_expend18)
    state_expend.CF_ID = state_expend.CF_ID.astype(int)
    data = pd.DataFrame()
    for index, item in dicts.periods2.iteritems():
        period = state_expend[state_expend.Filing_Period == item]
        period.Filing_Period = index
        data = data.append(period, ignore_index = True)
    state_expend = data
    state_expend.Amount = state_expend.Amount.astype(float)
    smalls = state_expend[state_expend.Payee_Type == 'Total of Expenditures not exceeding $100']
    smalls.Payee_Name = 'small'
    smalls.Payee_State = 'DE'
    state_expend = state_expend[state_expend.Payee_Type != 'Total of Expenditures not exceeding $100']
    state_expend = state_expend.append(smalls)
    state_expend = state_expend.dropna()
    state_expend.Expenditure_Date =  pd.to_datetime(state_expend.Expenditure_Date)
    state_expend.Payee_State = state_expend.Payee_State.str.upper()
    state_expend.Payee_Type = state_expend.Payee_Type.map(dicts.contrib_dict)
if(x==2): 
    state_expend = pd.read_csv(r'C:\Users\Dillon\Desktop\New folder\model\corrected_expends.csv')
    
x = input('input results data? (y/n)')
if(x=='y'): 
    results08p = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\08resultsp.txt")
    results08g = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\08resultsg.txt")
    results10p = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\10resultsp.txt")
    results10g = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\10resultsg.txt")
    results12p = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\12resultsp.txt")
    results12g = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\12resultsg.txt")
    results14p = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\14resultsp.txt")
    results14g = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\14resultsg.txt")
    results16p = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\16resultsp.txt")
    results16g = doe_parse.parser(r"C:\Users\Dillon\Documents\chris_data\16resultsg.txt")
    results_pack = [results08p, results08g,results10p, results10g,results12p, results12g,results14p, results14g,results16p, results16g,]
    for results in results_pack:
        results = results.drop(['Absentee','Machine','Total'],axis=1)
        
x = input('process results data? (y/n)')
if(x=='y'):         
    primaries = processing.results_processing(results08p,0,2008,state_contribs,canlist,state_expend,masterlist,match_list)
    primaries = primaries.append(processing.results_processing(results10p,0,2010,state_contribs,canlist,state_expend,masterlist,match_list))
    primaries = primaries.append(processing.results_processing(results12p,0,2012,state_contribs,canlist,state_expend,masterlist,match_list))
    primaries = primaries.append(processing.results_processing(results14p,0,2014,state_contribs,canlist,state_expend,masterlist,match_list))
    primaries = primaries.append(processing.results_processing(results16p,0,2016,state_contribs,canlist,state_expend,masterlist,match_list))
    general = processing.results_processing(results08g,1,2008,state_contribs,canlist,state_expend,masterlist,match_list)
    general = general.append(processing.results_processing(results10g,1,2010,state_contribs,canlist,state_expend,masterlist,match_list))
    general = general.append(processing.results_processing(results12g,1,2012,state_contribs,canlist,state_expend,masterlist,match_list))
    general = general.append(processing.results_processing(results14g,1,2014,state_contribs,canlist,state_expend,masterlist,match_list))
    general = general.append(processing.results_processing(results16g,1,2016,state_contribs,canlist,state_expend,masterlist,match_list))    
        
        
        