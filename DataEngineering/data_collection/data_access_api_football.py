import copy

import requests
from rapid_api_key import x_rapidapi_key
from id_league_tuples import league_ids


def send_request(url, url_keys):
    response = requests.request("GET", url, headers=headers, params=url_keys)
    json_response = response.json()["response"]
    return json_response


def try_request(url, url_keys):
    i = 0
    while i <= 15:
        try:
            response = send_request(url, url_keys)
            return response
        except KeyError as e:
            print(f'Request failure {i}')
            i+=1
    raise KeyError('Request failed!')


if __name__ == "__main__":
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"

    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': x_rapidapi_key
    }


    match_day_data = [] # league | year | matchday

    year_league_array = [(league[0], league[1], season) for league in league_ids for season in league[2]] # id | league | year
    i = 0 # iteration counter
    for league_year in year_league_array[0:70]:
        print(league_year)
        url_keys = {"season": league_year[2],
                    "league": league_year[0]}
        rounds = try_request(url, url_keys)

        for round in rounds[2:4]:
            print(round)
            url_keys = {"season": league_year[2],
                        "league": league_year[0],
                        "round": round}
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            fixtures = try_request(url, url_keys)

            # get match statistics
            match_storing_dict = {
                'id': int,
                'league': str,
                'date': str,
                'team home': str,
                'team away': str,
                'statistics': [dict]
                # 'Shots on Goal': [int, int],  # first value is home team
                # 'Shots off Goal': [int, int],
                # 'Total Shots': [int, int],
                # 'Blocked Shots': [int, int],
                # 'Shots insidebox': [int, int],
                # 'Fouls': [int, int],
                # 'Corner Kicks': [int, int],
                # 'Offsides': [int, int],
                # 'Ball Possession': [float, float],
                # 'Yellow Cards': [int, int],
                # 'Red Cards': [int, int],
                # 'Goalkeeper Saves': [int, int],
                # 'Total passes': [int, int],
                # 'Passes accurate': [int, int],
                # 'Passes per cent': [float, float]
            }

            stat_url = url + '/statistics'
            for fixture in fixtures:
                match_dict = copy.deepcopy(match_storing_dict)
                match_dict['statistics'] = []
                match_dict['id'] = int(fixture['fixture']['id'])
                match_dict['league'] = fixture['league']['name']
                match_dict['date'] = fixture['fixture']['date']
                match_dict['team home'] = fixture['teams']['home']['name']
                match_dict['team away'] = fixture['teams']['away']['name']
                for team in [fixture['teams']['home']['id'], fixture['teams']['away']['id']]:
                    url_keys = {"fixture": int(fixture['fixture']['id']), "team": int(team)}
                    #url_keys = {"fixture": 215662, "team": 463}
                    stats = try_request(stat_url, url_keys)
                    i += 1
                    print(f'iteration {i}')
                    if len(stats) == 0:
                        print(f'no statistics found for {url_keys}')
                        print(f'{league_year} failed!')
                        break
                    else:
                        print(f'saving statistics')
                        print(f'{league_year} success!')
                        match_dict['statistics'].append(stats[0]['statistics'])


    # TODO: write matchday data array in file

    # TODO: iterate over matchday data array and append statistics for every match in data file

    # resp_dict = dict(response.json())["response"]
    #
    # print(resp_dict[0].keys())




    """
    plan how to access all data:
    1. get league ids
    2. get years
    3. get rounds for league and year
    4. for every round (+league id, year/season) : get fixture -> match data
    """