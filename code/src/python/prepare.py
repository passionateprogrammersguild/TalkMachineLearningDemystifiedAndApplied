import pandas as pd
import numpy as np

import random, sys, os, math, datetime, collections, itertools, calendar, dateutil.relativedelta, time, re

def extract_event_id(row):
    full_event_name = row['event_name']
    
    name = None

    try:
        name = re.match('UFC\s?\d+', full_event_name).group(0)
        sys.stdout.write(".")
    except:
        sys.stdout.write("X")
        name = full_event_name    

    return name

def win(row):
    return row['f1fid'] if row['f1result'] == 'win' else row['f2fid']

if __name__ == "__main__":
    # reproduce
    random.seed(1)
    np.random.seed(1)

    # unpack
    datadir = sys.argv[1]
    modeldir = sys.argv[2]

    df_fights = pd.read_table(os.path.join(datadir, "ALL_UFC_FIGHTS_2_23_2016.tsv"), sep='\t')
    df_fighters = pd.read_table(os.path.join(datadir, "ALL_UFC_FIGHTERS_2_23_2016.tsv"), sep='\t')
    df_payouts = pd.read_table(os.path.join(datadir, "ufc_ppv_payouts.tsv"), sep='\t')

    #add EVENTS column to df_fights dataframe to join in the payouts
    df_fights['EVENT'] = df_fights.apply(lambda row: extract_event_id(row), axis=1)    
    df_fights_with_payouts = pd.merge(df_fights, df_payouts, on='EVENT', how='left')
    df_fights_with_payouts['IS_PAYOUT_ERROR'] = df_fights_with_payouts['event_name'] == df_fights_with_payouts['EVENT']

    #remove unnecessary columns
    del df_fighters['fid']
    del df_fighters['name']

    #join in fighter datadir
    df_f1 = df_fighters.rename(columns={'url': 'f1pageurl', 'nick': 'f1nick', 'birth_date': 'f1birth_date', 'height': 'f1height', 'weight': 'f1weight', 'association': 'f1association', 'class': 'f1class',	'locality': 'f1locality',	'country': 'f1country'})
    df_f2 = df_fighters.rename(columns={'url': 'f2pageurl', 'nick': 'f2nick', 'birth_date': 'f2birth_date', 'height': 'f2height', 'weight': 'f2weight', 'association': 'f2association', 'class': 'f2class',	'locality': 'f2locality',	'country': 'f2country'})

    df_f1_full = pd.merge(df_fights_with_payouts, df_f1, on='f1pageurl', how='left')
    df_full = pd.merge(df_f1_full, df_f2, on='f2pageurl', how='left')

    df_full['IS_F1_ERROR'] = df_full['f1height'] == None
    df_full['IS_F2_ERROR'] = df_full['f2height'] == None

    #add a column with the id of the fighter that won the fight
    df_full['win'] = df_fights.apply(lambda row: win(row), axis=1)    
    
    #find payouts that are not in the fights
    print "\nTOTAL FIGHTS", len(df_fights)
    print "TOTAL UNIQUE FIGHTS", len(pd.unique(df_fights['event_name']))

    df_fights_with_payouterror = df_fights_with_payouts[(df_fights_with_payouts['IS_PAYOUT_ERROR'] == True)]
    print "TOTAL UNIQUE FIGHTS WITH NULL BUYRATE", len(pd.unique(df_fights_with_payouterror['EVENT']))

    df_f1_error = df_full[(df_full['IS_F1_ERROR'] == True)]
    df_f2_error = df_full[(df_full['IS_F2_ERROR'] == True)]

    print "TOTAL F1 ERRORS", len(pd.unique(df_f1_error['EVENT']))
    print "TOTAL F2 ERRORS", len(pd.unique(df_f2_error['EVENT']))

    df_subset = df_full[['f1name', 'f1height', 'f1weight', 'f2name', 'f2height', 'f2weight', 'f1fid', 'f2fid', 'win']]
    print df_subset[:10]
