import asyncio
import json


from aiohttp import ClientSession
from pathlib import Path



def fetch_user():
    git_user = json.load(open(Path.cwd() / 'git_user.json'))
    username = git_user.get('username', 'Input username')
    api_key = git_user.get('api_key', 'Input api_key')
    return username, api_key



class GitUserData:
    def __init__(self):
        self.username = fetch_user()[0]
        self.api_key = fetch_user()[1]
        self.url = f'https://api.github.com/users/{self.username}/'
    
    async def parse_main_git(self, session):
        async with session.get(self.url) as response:
            await response.json()
            
            return
    
    
        
        

async def main():
    async with ClientSession() as session:
        git_user_data = GitUserData()
        await asyncio.gather(
            git_user_data.parse_main_git(session)
        )

if __name__ == '__main__':
    asyncio.run(main())