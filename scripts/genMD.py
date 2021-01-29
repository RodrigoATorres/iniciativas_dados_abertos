from dotenv import load_dotenv
load_dotenv()

import os
import csv
import re
import requests
import jinja2


templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)

def getRepoInfo(repoUrl):
    info = {}
    api_path = 'https://api.github.com/repos/' + re.search('github.com\/([^\/]*\/[^\/^\?]*)', repoUrl)[1]
    for key in ['languages']:
        info[key] = requests.get(api_path + '/' + key, headers={'Authorization': 'token ' + os.getenv("GITHUB_TOKEN")} ).json()
    for key in ['contributors', 'stargazers', 'commits', 'issues']:
        tmp_res = requests.get(api_path + '/' + key + '?per_page=1&anon=true', headers={'Authorization': 'token ' + os.getenv("GITHUB_TOKEN")} )
        if 'link' in tmp_res.headers.keys():
            info[key] = int(re.findall('\&page=([0-9]*)', tmp_res.headers['link'])[1])
        else:
            info[key] = 1

    info['last_commit'] = requests.get(api_path + '/commits?per_page=1&anon=true', headers={'Authorization': 'token ' + os.getenv("GITHUB_TOKEN")} ).json()[0]['commit']['author']['date']
    info['lang_percs'] = list( map( lambda x: [x, round(info['languages'][x]/sum(info['languages'].values())* 100) ], info['languages'].keys()) )
    info['lang_percs'].sort(key = lambda x: x[1],reverse=True)
    info['lang_percs'] = info['lang_percs'][:3]

    return info


with open('projects.csv') as f:
    repo_info = {}

    for proj_info in csv.DictReader(f):
        repo_info.setdefault(proj_info['category'], [])
        tmp_info = {**getRepoInfo(proj_info['url']), **proj_info}
        repo_info[proj_info['category']].append(tmp_info)

    print(repo_info)
        
    template = templateEnv.get_template('readme_template.md')
    cat_names = list(repo_info.keys())
    cat_names.sort()
    print( cat_names)
    readme_text = template.render(all_info = repo_info, cat_names = cat_names)

    with open('readme.md', 'w') as f:
        f.write(readme_text)

