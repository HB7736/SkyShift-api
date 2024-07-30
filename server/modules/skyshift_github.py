import requests
from modules.project import identify_language

class GithubRepo:
    def __init__(self, owner, repo, branch):
        self.owner = owner
        self.repo = repo
        self.branch = branch

    def get_info(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/{self.branch}?recursive=1"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            repo_size = sum(item['size'] for item in data['tree'] if item['type'] == 'blob')
            executables_size = sum(item['size'] for item in data['tree'] if self.is_executable(item['path']))
            files = [item for item in [item['path'] for item in data['tree'] if item['type'] == 'blob'] if not item.count("/")]
            directories = [item for item in [item['path'] for item in data['tree'] if item['type'] == 'tree']  if not item.count("/")]
            return {"repo_size": repo_size, "executables_size": executables_size, "files": files, "directories": directories}
        else:
            return {"Error":"Failed to fetch repository"}

    def is_executable(self, filename):
        executable_extensions = {'.py', '.js', '.sh', '.bat', '.exe', '.cmd', '.pl', '.rb', '.php', '.java', '.cpp', '.c', '.h', '.css', '.html', '.xml', '.json', '.ts', '.tsx', '.jsx'}
        return any(filename.endswith(ext) for ext in executable_extensions)

def get_user_repositories_info(owner):
    try:
        url = f"https://api.github.com/users/{owner}/repos"
        response = requests.get(url)
        if response.status_code == 200:
            repositories = response.json()
            reponames = []
            for repo in repositories:
                reponames.append(repo["name"])
            return {"repos":reponames}
        elif response.status_code == 404:
            return {"Error":"Username not found."}
        else:
            return {"Error":"Failed to Fetch Repositories"}
    except Exception as e:
        return {"Error":e}

def get_repo_info(owner,repo_name,branch_name):
    github_repo = GithubRepo(owner=owner,repo=repo_name,branch=branch_name)
    repo_info = github_repo.get_info()
    repo_info.update(identify_language(repo_info))
    return repo_info