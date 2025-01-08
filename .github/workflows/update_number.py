import os
import random
import subprocess
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def read_number():
    with open('number.txt', 'r') as f:
        return int(f.read().strip())

def write_number(num):
    with open('number.txt', 'w') as f:
        f.write(str(num))

def git_commit():
    subprocess.run(['git', 'add', 'number.txt'])
    date = datetime.now().strftime('%Y-%m-%d')
    commit_message = f"Update number: {date}"
    subprocess.run(['git', 'commit', '-m', commit_message])

def git_push():
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)

def update_task_scheduler_with_random_time():
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    task_name = "UpdateNumberTask"
    script_path = os.path.join(script_dir, 'update_number.py')

    # Remove the existing task
    os.system(f"schtasks /delete /tn {task_name} /f >nul 2>&1")

    # Create a new task
    os.system(
        f'schtasks /create /tn {task_name} /tr "python {script_path}" /sc daily /st {random_hour:02d}:{random_minute:02d}'
    )
    print(f"Task Scheduler updated to run at {random_hour:02d}:{random_minute:02d}.")

def main():
    current_number = read_number()
    new_number = current_number + 1
    write_number(new_number)
    git_commit()
    git_push()
    update_task_scheduler_with_random_time()

if __name__ == "__main__":
    main()
