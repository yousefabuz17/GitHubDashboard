import asyncio
import json

from aiohttp import ClientSession
from dataclasses import dataclass
from datetime import datetime as dt
from typing import NamedTuple
from pathlib import Path
from pprint import pprint


class ConfigInfo(NamedTuple):
    username: str
    api_key: str


class GitUserData:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key
        self.url = f'https://api.github.com/users/{self.username}'
    
    async def parse_git(self, session):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': 'MyGitHubDashboardProject/1.0'
        }
        async with session.get(self.url, headers=headers) as response:
            main_json = json.loads(json.dumps(await response.json()))
            
            main_data = {
                        'name': main_json.get('name', None),
                        'user_avatar': main_json.get('avatar_url', None),
                        'site_admin': main_json.get('site_admin', False),
                        'company': main_json.get('company', None),
                        'twitter_username': main_json.get('twitter_username', None),
                        'public_repos': main_json.get('public_repos', 0),
                        'public_gists': main_json.get('public_gists', 0),
                        'followers_count': main_json.get('followers', 0),
                        'following_count': main_json.get('following', 0),
                        'account_created': GitUserData.parse_date(main_json.get('created_at', None)),
                        'user_bio': main_json.get('bio', None),
                        'user_blog': main_json.get('blog', None)
                        }

            api_data = { 
                        'main_github_page': main_json.get('html_url', None),
                        'followers_url': main_json.get('followers_url', None),
                        'following_url': main_json.get('following_url', None),
                        'gists_url': main_json.get('gists_url', None),
                        'repos_url': main_json.get('repos_url', None)
                        }
            
            async def parse_url_apis(api_data, session):
                url_info = {}
                async with session as session:
                    for key, url in api_data.items():
                        if url:
                            async with session.get(url, headers=headers) as response:
                                try:
                                    data = json.loads(json.dumps(await response.json()))
                                    url_info[key] = data
                                except:
                                    pass
                return url_info

            api_info = await parse_url_apis(api_data, session)
        full_data = {**main_data, **api_info}
        self.dump_data(full_data)
        return full_data
    
    def dump_data(self, full_data):
        path = open(Path(__file__).parent.absolute() / 'full_data.json', 'w')
        json.dump(full_data, path, indent=4)

    @staticmethod
    def load_json(file):
        return json.load(open(Path(__file__).parent.absolute() / file))
    
    @staticmethod
    def parse_date(date_):
        if not date_:
            return None
        
        date_ = ' '.join(date_.split('T'))[:-1]
        return dt.strptime(date_, '%Y-%m-%d %H:%M:%S').strftime('%I:%M:%S%p %m-%d-%Y')
        
        
        # ** Create separate modules to handle data processing, analytics, and visualization.
        # TODO for GitHub API Integration:
            # ? Implement methods in this class to fetch:
            # ? repository details, commit history, pull requests, and other relevant information.
            # ? Once data is all fetched and organized, follow up with data processing and analytics
            # ? Make a large sql database containing all information on each repo
            

async def main():
    config_file = GitUserData.load_json('config.json')
    config = ConfigInfo(*config_file.values())
    
    async with ClientSession() as session:
        git_user_data = GitUserData(*config)
        await asyncio.gather(
            git_user_data.parse_git(session)
        )

if __name__ == '__main__':
    asyncio.run(main())









    
