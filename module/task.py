from typing import Optional

from utils import data_input, pause
from .command import Command


# noinspection PyMethodMayBeStatic
class Task:
    def __init__(self):
        self.banner()
        self.username = self.ask_username()

        # Tasks
        self.tasks = []
        self.completed_tasks = []
        self.today_tasks = []  # Numbers only for indexing `tasks`

        # Scope
        self.scope = None

    def banner(self):
        # R1
        print("-" * 35)
        print("| Welcome to the SCE To-Do List~! |")
        print("-" * 35)

    def ask_username(self) -> str:
        # R2
        username = data_input(
            prompt="Please input your name",
            empty_err_msg="Empty username is not supported. Please enter again."
        )
        print(f"Welcome, {username}.")
        return username

    def set_scope(self, scope: Optional[str] = None):
        self.scope = scope

    def cmd_entry(self):
        while True:
            match self.scope:
                case None:
                    # R3
                    print(f"+{'-' * 11}+")
                    print("| Main menu |")
                    print(f"+{'-' * 11}+")
                    # R4
                    print(", ".join((
                        f"Hi {self.username}",
                        f"you have {len(self.tasks)} to-do(s)",
                        f"{len(self.today_tasks)} task(s) for today",
                        f"and completed {len(self.completed_tasks)} task(s)."
                    )))
                case "today":
                    # R10
                    print(f"+{'-' * 30}+")
                    print("| Main menu -> Tasks for today |")
                    print(f"+{'-' * 30}+")
                    print(self.list(today=True))

            print(f"Command options: {Command._command_list(self.scope)}")
            raw_cmd = data_input(
                not_empty=True,
                prompt="\nPlease input your command",
                empty_err_msg="Invalid command. Please input again."
            ).strip()
            cmd = Command(raw_cmd, self, self.scope)
            result, err_code, extra = cmd._run_command()
            if not result:
                if err_code == "NOT_FOUND":
                    msgs = ["Invalid command. Please input again."]
                    if not self.scope:
                        msgs.append("\nTips: You can use `help` to see available commands.")
                    print("\n".join(msgs))
                elif err_code == "INVALID_PARAM":
                    print("Invalid Parameter.")
                continue
            # R6
            if err_code != "SKIP_PAUSE":
                pause()

    def list(self, banner=True, completed=False, today=False):
        result = []
        task_list = self.completed_tasks if completed else self.tasks

        if today:
            task_list = self.today_tasks

        if today:
            msg = f"You have {len(task_list)} task"
        else:
            msg = f"You have {'completed ' if completed else ''}{len(task_list)} to-do"

        if len(task_list) > 1:
            msg += "s"
        if today:
            msg += " for today"
        msg += ":"

        if banner:
            result.append(msg)

        for index, task in enumerate(task_list):
            result.append(f"{index}: {task}")
        if not task_list:
            if today:
                result.append("No task is assigned for today.")
            else:
                result.append("No to-dos outstanding.")

        return "\n".join(result)
