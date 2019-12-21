from github import Github
import pygit2
import sys, getopt
import os

token = ""
repos_to_delete = ["test_script"]

project_codes = {
    "py": "Python",
    "pyAt": "Python\\Automation"
}


def delete_repos(user):
    for repo_name in repos_to_delete:
        try:
            repo_to_delete = user.get_repo(repo_name)
            repo_to_delete.delete()
            print("Deleted repo '{}' successfully. \n".format(repo_name))
        except:
            print("Repo '{}' doesn't exist or some other error has occured.".format(repo_name))

def create_github_repo(user):
    repo = None
    valid_name = False

    while valid_name == False:
        repo_name = input("Enter project name: ")

        print("\nInit Github Repository: {} \n".format(repo_name))

        try:
            repo = user.create_repo(repo_name, auto_init=True)
            valid_name = True
        except:
            print("This repository name isn't available. Please try again. \n")

        print("Repository '{}' created successfully. \n".format(repo_name))

    return repo

def init_project_repo(project_location, project_type: str):
    
    name_of_file = "main"

    if "py" in project_type:
        name_of_file = "main" + ".py"

        complete_name = os.path.join(project_location, name_of_file)

        # Create main.py
        with open(complete_name, 'w') as the_file:
            the_file.write("# TODO: Start Working")

        # Path to local .vscode folder
        vscode_directoy = os.path.join(project_location, '.vscode')
        
        os.makedirs(vscode_directoy)

        settings_json_file = os.path.join(vscode_directoy, 'settings.json')
        
        # Add vscode settings to include anaconda path to correct env
        with open(settings_json_file, 'w') as the_file:
            the_file.write("""{
                "python.pythonPath": "C:\\Anaconda\\envs\\automation\\python.exe"
            }""")

        gitignore_file = os.path.join(project_location, '.gitignore')

        with open(gitignore_file, 'w') as the_file:
            the_file.write('.vscode\n__pycache')


def clone_and_init_github_repo(repo):
    project_location = input("Enter project location [Leave blank to init at default dir]: ")
    project_type = input("\nEnter project type: ")

    if project_location == "":
        root_dir = os.path.join("D:\\Projects", project_codes[project_type])
        project_location = os.path.join(root_dir, repo.name)

    print("\nProject Location: {} \n".format(project_location))

    print("Cloning repo {} -> {} ...\n".format(repo.git_url, project_location))

    repo_clone = pygit2.clone_repository(repo.git_url, project_location)

    init_project_repo(project_location, project_type)
    
    return repo_clone, project_location



def main():
    with open('token_github', 'r') as token_file:
        token = token_file.readline()

    print("Init Github client...\n")
    github_client = Github(token)

    # Github CLient User Object
    user = github_client.get_user()

    # Test Method to delete repos
    delete_repos(user)

    # Create Github repository: repo (github object)
    repo = create_github_repo(user)

    # Clone Github repository: repo_clone (pygit2 object), project_location (str)
    repo_clone, project_location = clone_and_init_github_repo(repo)

    # Open VSCode
    print("Opening VSCode at {} ...\n\n".format(project_location))
    os.system("code {}".format(project_location))






if __name__ == "__main__":
    main()