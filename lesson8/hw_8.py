import requests
import pygal
from pygal.style import LightColorizedStyle, LightenStyle, RotateStyle
from datetime import datetime
import subprocess
import os


def get_github_most_starred():
    params = {
        'q': 'language:python',
        'sort': 'starts'
    }
    url = 'https://api.github.com/search/repositories'
    r = requests.get(url, params=params)
    print("Status code:", r.status_code)

    return r.json()


def get_data():
    _names, _plot_dicts = [], []
    for repo_dict in get_github_most_starred()['items']:
        _names.append(repo_dict['name'])

        plot_dict = {
            'value': int(repo_dict['stargazers_count']),
            'label': str(repo_dict['description']),
            'xlink': str(repo_dict['html_url']),
        }
        _plot_dicts.append(plot_dict)
    return _names, _plot_dicts

names, plot_dicts = get_data()

grath_style = RotateStyle('#117788', base_style=LightColorizedStyle)

graph_config = pygal.Config()
graph_config.x_label_rotation = 45
graph_config.show_legend = False
graph_config.title_font_size = 24
graph_config.label_font_size = 14
graph_config.major_label_font_size = 18
graph_config.truncate_label = 15
graph_config.show_y_guides = False
graph_config.width = 1000

bar_chart = pygal.Bar(graph_config, style=grath_style)
bar_chart.title = 'Most-Starred Python Projects on GitHub'
bar_chart.x_labels = names

bar_chart.add(str(datetime.now()), plot_dicts)

OUT_FILE = 'python_most_starred.svg'

bar_chart.render_to_file(OUT_FILE)

try:
    subprocess.Popen(f'"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" "{os.path.abspath(OUT_FILE)}"')
except FileNotFoundError:
    print(f'Chart in {os.path.abspath(OUT_FILE)}')
