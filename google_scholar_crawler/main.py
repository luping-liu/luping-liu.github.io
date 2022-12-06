from scholarly import scholarly
from github import Github
import jsonpickle
import json
from datetime import datetime
import sys
import os

author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
name = author['name']
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']:v for v in author['publications']}
print(json.dumps(author, indent=2))
os.makedirs('results', exist_ok=True)
with open(f'results/gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author['citedby']}",
}
with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)


all_json = {}

for item in author['publications']:
    print(item, author['publications'][item]['num_citations'])
    all_json[item] = author['publications'][item]['num_citations']

    
g = Github(os.environ['GITHUB_TOKEN'])
for repo in g.get_user().get_repos():
    stars = repo.stargazers_count
    if stars > 0:
        print(repo.full_name, stars)
        all_json[repo.full_name] = stars

with open('results/google_github_data.json', 'w') as outfile:
    json.dump(all_json, outfile, ensure_ascii=False)
