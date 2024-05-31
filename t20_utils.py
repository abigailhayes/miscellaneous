import json
import numpy as np
import pandas as pd


def get_ident_split():
    """ Get the training, validation and test match identities"""
    records = np.loadtxt('t20s_json/README.txt', delimiter='-', skiprows=24, 
                         dtype={'names': ('year', 'month', 'day', 'level', 'type', 'gender', 'ident', 'teams'),
                                'formats': ('f4', 'f2', 'f2', 'U14', 'U4', 'U7', 'f8', 'U32')})
    output = {'train': [str(int(records[i]['ident'])) for i in range(len(records)) if records[i]['year'] in range(2005,2023)],
              'validate': [str(int(records[i]['ident'])) for i in range(len(records)) if records[i]['year'] == 2023],
              'test': [str(int(records[i]['ident'])) for i in range(len(records)) if records[i]['year'] == 2024]}
    return output


def data_cumul_wickets(match_data, innings):
    """The cumulative wickets at the end of each over in an innings"""
    output = {}
    count = 0
    max_over = 0
    for over in match_data['innings'][innings-1]['overs']:
        for delivery in over['deliveries']:
            if 'wickets' in delivery:
                count += 1
        output[str(over['over'])] = count
        max_over = over['over']
    if max_over < 19:
        for extra_over in range(max_over,20):
            output[str(extra_over)] = 0
    return output 


def data_target_info(match_data):
    """The target set by the first team batting"""
    try:
        return match_data['innings'][1]['target']
    except (IndexError, KeyError):
        return {'overs': 0, 'runs': 0}


def data_match_info(match_data):
    """Gather general match information"""
    try:
        city = match_data['info']['city']
    except KeyError:
        city = ''
    return {'city': city,
            'gender': match_data['info']['gender'],
           'month': int(match_data['info']['dates'][0][5:7]),
           'first_team': match_data['innings'][0]['team'],
           'second_team': [i for i in match_data['info']['teams'] if i!=match_data['innings'][0]['team']][0],
           'venue': match_data['info']['venue']}


def data_get_winner(match_data):
    """Get correct label for the match result"""
    if 'winner' in match_data['info']['outcome']:
        winner = match_data['info']['outcome']['winner']
        if winner == match_data['innings'][0]['team']:
            return 1 # Team batting first won
        else:
            return 2 # Team batting second won
    else:
        return 0 # No winner


def data_load_match(match_id):
    """Function to load in and organise the data for a single match"""
    # Load data
    with open(f't20s_json/{match_id}.json') as json_data:
        match_data = json.load(json_data)

    return match_data


def data_load_id_matches(id_list):
    """Load all data for the match ids in the list"""
    output = {}
    for match_id in id_list:
        output[match_id] = data_load_match(match_id)
    return output


def data_load_all():
    """Load all the match data, split by use"""
    output = {}
    ids = get_ident_split()
    for dataset in ids:
        output[dataset] = data_load_id_matches(ids[dataset])
    return output


def data_runs(match_data, innings):
    """Getting the number of runs in an innings"""
    output = 0
    for over in match_data['innings'][innings-1]['overs']:
        for delivery in over['deliveries']:
            output += delivery['runs']['total']
    return output


def data_overs(match_data, innings):
    """Getting the number of overs in an innings"""
    output = 0
    for over in match_data['innings'][innings-1]['overs']:
        for delivery in over['deliveries']:
            output += delivery['runs']['total']
    return output


