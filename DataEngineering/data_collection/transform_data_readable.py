import json
import os
import git
import csv


def main():
    git_root = git.Repo(os.getcwd(), search_parent_directories=True).git.rev_parse("--show-toplevel")
    read_file_path = os.path.join(git_root, 'data/raw_data/understat_data.json')
    print(read_file_path)

    data_list = []
    with open(read_file_path) as file:
        data = json.load(file)['data']
        for wrapped_set in data:
            for datapoint in wrapped_set:
                data_list.append(datapoint)

    header_line = ['id', 'league', 'date', 'team_home', 'team_away', 'chances', 'goals', 'xG', 'shots', 'shots_on_target', 'deep', 'ppda', 'xPTS']
    write_file_path = os.path.join(git_root, 'data/raw_data/understat_data.csv')

    with open(write_file_path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=header_line, delimiter=';')
        writer.writeheader()
        writer.writerows(data_list)


if __name__ == "__main__":
    main()
