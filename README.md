# java-deps-checker
A simple script to go search an organization's Java dependency management files for a particular dependency. Maven pom.xml and Gradle build.gradle are currently supported, though support for the latter can be improved.

## Installation
```
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Usage
```
python3 java-deps-checker.py <your_github_access_token> <github_org_name> <dependency_group_id> <dependency_artifact_id>
```
