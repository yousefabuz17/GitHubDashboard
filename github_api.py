import asyncio
import json

from aiohttp import ClientSession
from pathlib import Path
from pprint import pprint

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
                        'account_created': main_json.get('created_at', None),
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
            # Only fetching repo data for now
            async def parse_repo_apis(repo_data, session):
                async with session.get(repo_data.get('repos_url'), headers=headers) as response:
                    try:
                        repos_data = json.loads(json.dumps(await response.json()))
                        # repos_json = open(Path.cwd() / 'repos_data.json', 'w', encoding='utf-8')
                        pprint(repos_data, sort_dicts=False)
                    except:pass

            await parse_repo_apis(api_data, session)
        
        
        
        # ** Create separate modules to handle data processing, analytics, and visualization.
        # TODO for GitHub API Integration:
            # ? Implement methods in this class to fetch:
            # ? repository details, commit history, pull requests, and other relevant information.
            # ? Once data is all fetched and organized, follow up with data processing and analytics
            
            

async def main():
    async with ClientSession() as session:
        git_user_data = GitUserData()
        await asyncio.gather(
            git_user_data.parse_main_git(session)
        )

if __name__ == '__main__':
    asyncio.run(main())









    
