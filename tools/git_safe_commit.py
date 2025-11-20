import subprocess, os, time

def create_branch_and_commit(message='karen-auto', files=None, branch_prefix='karen/auto'):
    files = files or []
    if not os.path.exists('.git'):
        return {'error':'no_git_repo'}
    branch = f"{branch_prefix}/{int(time.time())}"
    subprocess.run(['git','checkout','-b',branch], check=False)
    cmd = ['git','add'] + files if files else ['git','add','.']
    subprocess.run(cmd, check=False)
    subprocess.run(['git','commit','-m',message], check=False)
    subprocess.run(['git','push','--set-upstream','origin',branch], check=False)
    return {'branch':branch}
