# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 19:14:12 2018

@author: Dillon
"""
import utilities
import dicts
from fuzzywuzzy import fuzz, process
import pandas as pd
import numpy as np

def results_processing(results,election_type,year,state_contribs,canlist,state_expend,masterlist,match_list):
    results = results.drop(['Absentee','Machine','Total'],axis=1)
    results.Party = results.Party.astype('category')
    results.Percent = results.Percent.astype('float')
    results['Percent'] = results.groupby(['Name', 'Office'])['Percent'].transform('sum')
    results['Year'] = year
    results = results.drop_duplicates(subset=['Name'])
    results = utilities.won_checker(results,election_type)
    results = utilities.inc_checker(results,year,masterlist)
    periods = str(year)+dicts.type_dict[election_type]
    results = pd.merge(results,match_list, on='Name')
    results = filler(results, periods, state_contribs,state_expend)
    return results
    
def filler(results_data, periods, contrib_list,expend_list):
    df = pd.DataFrame()
    for index, row in results_data.iterrows():
        print(row.Name)
        contrib = get_contrib(row.CF_ID, periods, contrib_list)
        expend = get_expend(row.CF_ID,periods, expend_list)
        details = pd.merge(contrib,expend, on='CF_ID')
        df = df.append(details)
    merged = pd.merge(results_data,df, on='CF_ID')
    return merged

def get_contrib(CF_ID,periods,contrib_list):
    df= contrib_list[contrib_list.CF_ID == CF_ID]
    df = df[df.Filing_Period.isin(dicts.period_dict[periods])]
    total = sum(df['Contribution_Amount'])
    add = pd.DataFrame([[0]*9],columns=set(list(dicts.contrib_dict.values())))
    for index, row in df.iterrows():
        ct1 = row.Contributor_Type
        if(ct1 == 'Individual' and row['Contributor_State'] == 'DE'):
            ct1 = 'Ind_DE'
        if(row['Contribution_Amount'] < 101):
            ct1 = 'sub_100'
        add.loc[0,ct1]=add.loc[0,ct1]+row['Contribution_Amount']    
    add['Contrib_Total'] = total
    add['CF_ID'] = CF_ID
    return add

def get_expend(CF_ID,periods,expend_list):
    df= expend_list[expend_list.CF_ID == CF_ID]
    df = df[df.Filing_Period.isin(dicts.period_dict[periods])]
    total = sum(df['Amount'])
    add = pd.DataFrame([[0]*10],columns=dicts.mod_purp_dict)
    for cat in dicts.mod_purp_dict:
        cat = str(cat)
        df1 = df.loc[df.Expense_Category == cat]
        tot = sum(df1.Amount)
        add[cat] = add[cat] + tot

    add['Expend_Total'] = total
    add['CF_ID'] = CF_ID
    return add

def text_match(results,canlist,contributions,periods):
    print(periods)
    limited_contribs = contributions[contributions.Filing_Period.isin(dicts.period_dict[periods])]
    df1 = pd.DataFrame()
    df1["CF_ID"] = pd.Series([], dtype=int)
    for index, candidate in results.iterrows():
        try:
            potential_committees = canlist[canlist.off_trim == candidate.Office]
            df = pd.DataFrame()
            df["CF_ID"] = pd.Series([], dtype=int)
            for index, row in potential_committees.iterrows():
                limited_contrib= limited_contribs[limited_contribs.CF_ID == row.CF_ID]
                row['Total_Raised'] = limited_contrib.Contribution_Amount.sum()
                guess = candidate.Name
                row['Match_Score'] = fuzz.partial_token_set_ratio(guess,row.Committee_Name) #* (row.Total_Raised * .2)
                if(row.CF_ID != np.isnan):
                    df = df.append(row)
            df = df.sort_values('Total_Raised', ascending=False).drop_duplicates('Match_Score')
            df =df.sort_values('Match_Score', ascending=False)
            df=df.reset_index(drop=True)
            head = df.loc[0,]
            if(head.Match_Score < 50):
                print("Low match score, something might be up\n Committee name:", head.Committee_Name,  
                      "\n Candidate Name: ",candidate.Name, 
                      "\n Candidate Party: ",candidate.Party, 
                      "\n Candidate Percentage: ",candidate.Percent, 
                      '\n How about:\n')
                guesses = process.extract(candidate.Name, canlist.Committee_Name, scorer =fuzz.token_set_ratio, limit =10)
                
                guesses = pd.DataFrame(guesses,columns = ['Committee_Name','Match_Score','number'])
                guesses['Total_Raised'] = canlist.loc[guesses.number][periods].tolist()
                print(guesses)
                guesses['CF_ID'] =  canlist.loc[guesses.number]['CF_ID'].tolist()
                x = input('Look good? Enter number or \'n\' if not')
                if (x == 'n' or x == 'N'):
                    candidate['CF_ID'] = 0
                    candidate['Committee_Name'] =  'UNKNOWN COMMITTEE'
                    candidate['total'] = 0
                    candidate['match'] = 0
                else:
                    x = int(x)
                    head=guesses.loc[x]
                    candidate['CF_ID'] = head.CF_ID
                    candidate['Committee_Name'] =  head.Committee_Name
                    candidate['total'] = head.Total_Raised
                    candidate['match'] = head.Match_Score 
            else:
                candidate['CF_ID'] = head.CF_ID
                candidate['Committee_Name'] =  head.Committee_Name
                candidate['total'] = head.Total_Raised
                candidate['match'] = head.Match_Score
            df1 = df1.append(candidate)
        except Exception as ex:
            print (getattr(ex, 'message', repr(ex)))
            print('match failed', candidate.Name)       
    return df1