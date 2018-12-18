# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 12:39:35 2018

@author: Dillon

These are tools for maintaining some of the back end fundamentals data, such as updating the master list after an election.

"""

import pandas as pd
import dicts
import numpy as np

def canlister (df,contribs):
    xcanlist = pd.DataFrame()
    for office in dicts.offices:
        x = df[df.off_trim == office]
        xcanlist = xcanlist.append(x)
    df = pd.DataFrame()
    df["CF_ID"] = pd.Series([], dtype=int)
    for index, row in xcanlist.iterrows():
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2008all'])]
        row['2008all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2010all'])]
        row['2010all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2012all'])]
        row['2012all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2014all'])]
        row['2014all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2016all'])]
        row['2016all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2018all'])]
        row['2018all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2008p'])]
        row['2008p'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2010p'])]
        row['2010p'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2012p'])]
        row['2012p'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2014p'])]
        row['2014p'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2016p'])]
        row['2016p'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2018p'])]
        row['2018p'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        df=df.append(row)
    return df

def ml_updater(results,year,masterlist):
    ml = pd.DataFrame()
    for index, row in masterlist.iterrows():
        last = 'Incum_' + str(year-2)
        best = row[last],0
        for ind, candidate in results.iterrows():
            if row.name == candidate.Office:
                if candidate.Total > best[1]:
                    best = [candidate.Name,candidate.Total]
                    
        index = 'Incum_' + str(year)
        row[index]= best[0]
        ml = ml.append(row)
    return ml
            
def inc_checker(results,year,masterlist):
    data = []
    last = 'Incum_' + str(year - 2002)
    for index, row in results.iterrows():
        row.Incumbent = 0
        if (fuzz.ratio(row.Name , masterlist.loc[row.Office, last]) > 80):
            row.Incumbent = 1
        data.append(row)
    return pd.DataFrame(data)    
    
def won_checker(results, method):
    df = pd.DataFrame()
    if method == 0:
        for party in ['D','R']:
            pool = results[results.Party == party]
            for office in dicts.offices:
                candidates = pool[pool.Office == office]
                candidates = candidates.sort_values('Percent', ascending=False)
                candidates=candidates.reset_index(drop=True)
                candidates.loc[0,'Won'] = 1
                df = df.append(candidates)  
    if method == 1:
        for office in dicts.offices:
            candidates = results[results.Office == office]
            candidates = candidates.sort_values('Percent', ascending=False)
            candidates=candidates.reset_index(drop=True)
            candidates.loc[0,'Won'] = 1
            df = df.append(candidates)
    df = df.dropna(subset=['Name'])
    return df
        
def inc_updater(masterlist,year,cand):
    index = 'Incum_' + str(year)
    masterlist.loc[cand.Office,index] = cand.Name
    return
    
def inc_insurance(year,masterlist):
    incum = 'Incum_' + str(year)
    last = 'Incum_' + str(year-2)
    for index, row in masterlist.iterrows():
        masterlist[incum] = masterlist[last]
    return