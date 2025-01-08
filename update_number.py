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

def schedule_task():
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    
    # Format the time in HH:mm format (24-hour format)
    scheduled_time = f"{random_hour:02d}:{random_minute:02d}"

    # Use Task Scheduler to run the Python script at the random time
    task_name = "UpdateNumberTask"
    task_command = f"python {os.path.join(script_dir, 'update_number.py')}"

    # Command to create the scheduled task
    task_schedule_command = f'SchTasks /Create /SC DAILY /TN "{task_name}" /TR "{task_command}" /ST {scheduled_time}'
    subprocess.run(task_schedule_command, shell=True)
    
    print(f"Task scheduled to run at {scheduled_time} daily.")

def main():
    current_number = read_number()
    new_number = current_number + 1
    write_number(new_number)

    git_commit()
    git_push()

    schedule_task()

if __name__ == "__main__":
    main()
