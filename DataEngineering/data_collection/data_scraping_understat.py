"""
scaping data from uderstat.com
credits to: https://www.sergilehkyi.com/2019/06/web-scraping-advanced-football-statistics/
"""
import json
import os
from bs4 import BeautifulSoup, element
import requests
import enum
import re
from dataclasses import dataclass, field, asdict


class ErrorCodeEnum(enum.Enum):
    OK = 200
    NOT_FOUND = 404


test_url = 'https://understat.com/match/23171'

match_url = 'https://understat.com/match/'



@dataclass
class Match:
    id: int = 0
    league: str = ""
    date: str = ""
    team_home: str = ""
    team_away: str = ""
    chances: [int, int] = field(default_factory=list)  # home, away + 100 - sum(home, away)
    goals: [int, int] = field(default_factory=list)  # home, away
    xG: [float, float] = field(default_factory=list)
    shots: [int, int] = field(default_factory=list)
    shots_on_target: [int, int] = field(default_factory=list)
    deep: [int, int] = field(default_factory=list)
    ppda: [float, float] = field(default_factory=list)
    xPTS: [float, float] = field(default_factory=list)


def collect_all_data():
    total_matches = 0
    data = []
    try:
        for i in range(29896, 50000):
            print("\r Progress: {}% iteration: {}".format(round(i/(50000-80) * 100, 3), i), end='')
            request_errors = 0
            while True:
                try:
                    req = requests.get(match_url + str(i))
                    break
                except Exception as e:
                    print(str(e))
                    request_errors += 1
                    if request_errors > 5:
                        raise PermissionError('Failed connection after 5th attempt!')

            if req.status_code == ErrorCodeEnum.NOT_FOUND.value:
                continue
            elif req.status_code != ErrorCodeEnum.OK.value:
                print(f'Error code {req.status_code} for matchcode {i}')
                continue

            soup = BeautifulSoup(req.text, 'lxml')
            league_year, date = find_league_year_and_date(soup)
            total_matches += 1

            match = Match(i, league_year, date)
            find_match_stats(match, soup)
            data.append(asdict(match))

    except Exception as e:
        print(str(e))
        print(f"Access failed in iteration {i} with a total of matches: {total_matches}")

    finally:
        json_data = json.dumps(data)
        cwd = os.getcwd()
        with open(os.path.join(cwd, 'data.json'), "a") as outfile:
            outfile.write(json_data)

    return


def find_data_for_url(url: str):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    league_year, date = find_league_year_and_date(soup)
    match = Match(0, league_year, date)
    find_match_stats(match, soup)
    print(asdict(match))


def find_match_stats(match: Match, soup: BeautifulSoup):
    progress_bars = soup.find_all("div", class_='progress-bar')

    # team names
    team_divs = progress_bars[0].find_all_next("div", class_='progress-value')
    home_team = filter_html_tag_value(team_divs[0])
    away_team = filter_html_tag_value(team_divs[1])
    # print(f"match {home_team} against {away_team}")
    match.team_home = home_team
    match.team_away = away_team

    # chances
    iterator = re.findall('title=".*"', str(progress_bars[1]))
    chances_array = []
    for group in iterator:
        regex_group = re.search('".*"', group)
        chances_array.append(regex_group.group()[1:-2])
    # print(f"chances separation per team: {chances_array}")
    match.chances = chances_array

    # goals
    regex_goals = re.findall("[0-9]+", progress_bars[2].getText())
    # print(f"match score: {regex_goals[0]} : {regex_goals[1]}")
    match.goals = regex_goals


    # xG
    regex_xG = re.findall("[0-9]+.[0-9]+", progress_bars[3].getText())
    match.xG = regex_xG

    # shots
    regex_shots = re.findall("[0-9]+", progress_bars[4].getText())
    # print(f"shots per team: {regex_shots[0]} : {regex_shots[1]}")
    match.shots = regex_shots

    # shots on target
    regex_shots_target = re.findall("[0-9]+", progress_bars[5].getText())
    # print(f"shots on target per team: {regex_shots_target[0]} : {regex_shots_target[1]}")
    match.shots_on_target = regex_shots_target

    # deep
    regex_deep = re.findall("[0-9]+", progress_bars[6].getText())
    # print(f"shots on target per team: {regex_deep[0]} : {regex_deep[1]}")
    match.deep = regex_deep

    # ppda
    ppda = re.findall("[0-9]+.[0-9]+", progress_bars[7].getText())
    # print(f"ppda per team: {ppda[0]} : {ppda[1]}")
    match.ppda = ppda

    # xpts
    xpts = re.findall("[0-9]+.[0-9]+", progress_bars[8].getText())
    # print(f"xpts per team: {xpts[0]} : {xpts[1]}")
    match.xPTS = xpts

    return


def find_league_year_and_date(soup: BeautifulSoup):
    navigation_line = soup.find_all("ul", class_='breadcrumb')
    if len(navigation_line) != 1:
        print('Parsing error navigation line!')
        return
    links = navigation_line[0].find_all_next('li')

    league_year_regex = re.search('".*"', str(links[1]))
    league_year = league_year_regex.group()[1:-1].removeprefix('league/').replace("/", "")

    date_regex = re.search('>.*<', str(links[2])).group()
    date = date_regex[1:-1]

    return league_year, date


def filter_html_tag_value(html_text: element.PageElement) -> str:
    regex = re.search('>.*<', str(html_text))
    if len(regex.group()) != 0:
        return regex.group()[1:-1]


def main():
    collect_all_data()
    # find_data_for_url('https://understat.com/match/6344')


if __name__ == "__main__":
    main()
