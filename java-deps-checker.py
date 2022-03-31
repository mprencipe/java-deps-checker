import sys, base64
from github import Github, ContentFile, Repository
from xml.dom import minidom
from typing import Dict

access_token = sys.argv[1]
organization = sys.argv[2]
group_id = sys.argv[3]
artifact_id = sys.argv[4]

POM = 'pom.xml'
GRADLE = 'build.gradle'

DEPENDENCY_FILES = [POM, GRADLE]

g = Github(access_token)

def report_found(file: ContentFile, repo: Repository):
    print(f'Found in repository {repo.name}, file {file.name}')

def find_in_pom(file: ContentFile, repo: Repository, dep: Dict):
    doc = minidom.parseString(base64.b64decode(file.content).decode('utf-8'))
    pom_deps = doc.getElementsByTagName('dependency')
    for pom_dep in pom_deps:
        artifact_id = pom_dep.getElementsByTagName('artifactId')[0].firstChild.data
        group_id = pom_dep.getElementsByTagName('groupId')[0].firstChild.data
        if dep['artifact_id'] == artifact_id and dep['group_id'] == group_id:
            report_found(file, repo)

def find_in_gradle(file: ContentFile, repo: Repository, dep: Dict):
    for line in base64.b64decode(file.content).decode('utf-8').splitlines():
        if f"{dep['group_id']}:{dep['artifact_id']}" in line:
            report_found(file, repo)

def process_dependencies(file: ContentFile, repo: Repository, dep: Dict, g: Github):
    if file.name == POM:
        find_in_pom(file, repo, dep)
    elif file.name == GRADLE:
        find_in_gradle(file, repo, dep)
    else:
        raise Exception(f'Unknown file {file.name}')

def process_org_repos(org: str, dep: Dict, g: Github):
    org = g.get_organization(org)
    org_repos = org.get_repos()
    for repo in org_repos:
        files = repo.get_contents('.')
        for file in files:
            if file.name in DEPENDENCY_FILES:
                process_dependencies(file, repo, dep, g)

print(f'Starting search in GitHub organization {organization} for artifact {group_id}:{artifact_id}')
process_org_repos(organization, {'group_id': group_id, 'artifact_id': artifact_id}, g)
