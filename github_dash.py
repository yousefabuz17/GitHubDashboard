import asyncio
import json
import re

from aiohttp import ClientSession
from pathlib import Path
from bs4 import BeautifulSoup


def fetch_user():
    git_user = json.load(open(Path.cwd() / 'git_user.json'))
    username = git_user.get('username', 'Input username')
    api_key = git_user.get('api_key', 'Input api_key')
    return username, api_key



class GitUserData:
    def __init__(self):
        self.username = fetch_user()[0]
        self.api_key = fetch_user()[1]
        self.url = f'https://api.github.com/users/{self.username}'
    
    async def parse_main_git(self, session):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': 'MyGitHubDashboardProject/1.0'
        }
        async with session.get(self.url, headers=headers) as response:
            main_json = json.loads(json.dumps(await response.json()))

            name, site_admin, company, twitter_username, public_repos, followers_count, \
            following_count, account_created, user_bio = (
                main_json.get('name', 'No Name'),
                main_json.get('site_admin', False),
                main_json.get('company'),
                main_json.get('twitter_username'),
                main_json.get('public_repos', 0),
                main_json.get('followers', 0),
                main_json.get('following', 0),
                main_json.get('created_at', None),
                main_json.get('bio', None)
            )

            values = ' '.join([str(i) for i in main_json.values()]).split()
            all_values_with_apis = list(filter(lambda i: re.findall(rf'https://|{self.url}/(\w+)', i), values)) #Trying to use re more frequently

    #async def parse_value_gits(self, session):

        
            
    
    
        
        

async def main():
    async with ClientSession() as session:
        git_user_data = GitUserData()
        await asyncio.gather(
            git_user_data.parse_main_git(session)
        )

if __name__ == '__main__':
    asyncio.run(main())









    
