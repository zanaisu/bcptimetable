import subprocess
import os
import datetime
import sys

def run_command(command, verbose=True):
    """Run a shell command and return its output"""
    if verbose:
        print(f"Running: {command}")
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if verbose:
        if stdout:
            print(stdout.decode('utf-8'))
    
    if process.returncode != 0:
        print(f"Error: {stderr.decode('utf-8')}")
        return False
    return stdout.decode('utf-8')

def update_github():
    """Commit and push changes to GitHub"""
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("Error: Not a git repository. Initialize with 'git init' first.")
        print("Setting up git repository...")
        run_command('git init')
        
    # Check git status
    status = run_command('git status', verbose=False)
    if not status:
        print("Failed to check git status. Aborting.")
        return False
        
    # Check if remote exists
    remotes = run_command('git remote -v', verbose=False)
    if not remotes:
        print("No remote repository found.")
        repo_url = input("Enter your GitHub repository URL: ")
        if repo_url:
            run_command(f'git remote add origin {repo_url}')
        else:
            print("No URL provided. Skipping remote setup.")
            
    # Add all changes
    print("\nAdding all changes...")
    run_command('git add .')
    
    # Commit changes with timestamp
    print("\nCommitting changes...")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Update project - {timestamp}"
    commit_result = run_command(f'git commit -m "{commit_message}"')
    
    if "nothing to commit" in commit_result if commit_result else False:
        print("Nothing to commit. Repository is up to date.")
        return True
    
    # Push changes
    print("\nPushing changes...")
    branch_name = run_command('git rev-parse --abbrev-ref HEAD', verbose=False).strip()
    if not branch_name:
        branch_name = "main"  # Default to main if branch detection fails
        
    push_result = run_command(f'git push -u origin {branch_name}')
    
    if push_result:
        print("\n✅ Successfully pushed changes to GitHub!")
        return True
    else:
        print("\n❌ Failed to push changes.")
        print("\nPossible solutions:")
        print("1. Make sure you have the correct permissions for the repository")
        print("2. Try setting up SSH keys for GitHub: https://docs.github.com/en/authentication/connecting-to-github-with-ssh")
        print("3. For first-time push, try: git push --set-upstream origin main")
        print("4. If you're getting conflicts, try: git pull --rebase origin main")
        return False

if __name__ == "__main__":
    print("GitHub Update Script")
    print("====================")
    success = update_github()
    if not success:
        sys.exit(1)
