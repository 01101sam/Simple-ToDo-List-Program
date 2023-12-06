# Reference:
# https://github.com/TeamPGM/PagerMaid_Plugins_Pyro/blob/v2/pmcaptcha/main.py
# Author: @01101sam (Sam)
# Yes, that's still me.

import inspect
import re
import traceback
from dataclasses import dataclass, field
from typing import Optional, Union, Callable

from utils import get_version, data_input


def _sort_line_number(m):
    try:
        func = getattr(m[1], "__func__", m[1])
        return func.__code__.co_firstlineno
    except AttributeError:
        return -1


# noinspection PyMethodMayBeStatic
@dataclass
class Command:
    """R5 - main menu"""
    raw_cmd: str
    task: "task.Task"
    scope: Optional[str] = None
    command: str = field(init=False)
    parameters: list = field(init=False)

    # Regex
    scope_rgx = r":scope: (.+)"
    alias_rgx = r":alias: (.+)"
    param_rgx = r":param (opt)?\s?(\w+):\s?(.+)"

    # region Helpers

    def __post_init__(self):
        self.command = self.raw_cmd.split(" ")[0]
        self.parameters = self.raw_cmd.split(" ")[1:]

    def __getitem__(self, cmd: str) -> Optional[Callable]:
        # Get subcommand function
        if func := getattr(self, f"{self.scope}_{cmd}" if self.scope else cmd, None):
            return func
        # Check for alias
        if func := self._get_mapped_alias(cmd, "func"):
            return func
        return  # Not found

    @staticmethod
    def _command_list(scope: Optional[str]):
        commands = []
        for name, func in inspect.getmembers(Command, inspect.isfunction):
            if name.startswith("_"):
                continue
            curr_scope = None
            if result := re.search(Command.scope_rgx, func.__doc__ or ""):
                curr_scope = result[1].strip()
            if curr_scope != scope:
                continue
            commands.append(name[len(scope) + 1:] if scope else name)
        return commands

    def _run_command(self):
        if not (func := self[self.command]):
            return False, "NOT_FOUND", self.command
        full_arg_spec = inspect.getfullargspec(func)
        args_len = None if full_arg_spec.varargs else len(full_arg_spec.args)
        cmd_args = self.parameters[:args_len]
        func_args = []
        for index, arg_type in enumerate(
                tuple(full_arg_spec.annotations.values())
        ):  # Check arg type
            if args_len is None:
                func_args = cmd_args
                break
            try:
                if getattr(arg_type, "__origin__", None) == Union:
                    NoneType = type(None)
                    if (
                            len(arg_type.__args__) != 2
                            or arg_type.__args__[1] is not NoneType
                    ):
                        continue
                    if (
                            len(cmd_args) - 1 > index
                            and not cmd_args[index]
                            or len(cmd_args) - 1 < index
                    ):
                        func_args.append(None)
                        continue
                    arg_type = arg_type.__args__[0]
                func_args.append(arg_type(cmd_args[index]))
            except ValueError:
                return (
                    False,
                    "INVALID_PARAM",
                    tuple(full_arg_spec.annotations.keys())[index],
                )
            except IndexError:  # No more args
                self.help(self.command)
                return True, None, None
        should_skip_pause = False
        try:
            should_skip_pause = func(*func_args)
        except Exception as e:
            print(
                f"Error when running command {self.command}: {e}\n{traceback.format_exc()}"
            )
        return True, "SKIP_PAUSE" if should_skip_pause else None, None

    def _extract_docs(self, subcmd_name: str, text: str) -> str:
        extras = []
        if result := re.search(self.param_rgx, text):
            is_optional = (
                "(Optional) " if result[1] else ""
            )
            extras.extend(
                (
                    "Parameter:",
                    f"{is_optional}{result[2].lstrip('_')} - {result[3]}",
                )
            )

            text = re.sub(self.param_rgx, "", text)
        if result := re.search(self.alias_rgx, text):
            alias = result[1].replace(" ", "").split(",")
            alia_text = ", ".join(alias)
            extras.append(f"Alias: {alia_text}")
            text = re.sub(self.alias_rgx, "", text)
        if result := re.search(self.scope_rgx, text):
            extras.append(f"Scope: {result[1]}")
            text = re.sub(self.scope_rgx, "", text)
        len(extras) and extras.insert(0, "")
        cmd_display = self._get_cmd_with_param(subcmd_name).strip()
        return "\n".join(
            [
                cmd_display,
                re.sub(r" {4,}", "", text).strip(),
            ]
            + extras
        )

    def _get_cmd_with_param(self, subcmd_name: str) -> str:
        msg = subcmd_name
        if result := re.search(self.param_rgx, getattr(self, msg).__doc__ or ""):
            param = result[2].lstrip("_")
            msg += f" [{param}]" if result[1] else f" <{param}>"
        return msg

    def _get_mapped_alias(self, alias_name: str, ret_type: str):
        # Get alias function
        for name, func in inspect.getmembers(self, inspect.ismethod):
            if name.startswith("_"):
                continue
            docs = func.__doc__ or ""
            curr_scope = None
            if result := re.search(Command.scope_rgx, docs):
                curr_scope = result[1].strip()
            if curr_scope != self.scope:
                continue
            if (
                    result := re.search(self.alias_rgx, docs)
            ) and alias_name in result[1].replace(" ", "").split(","):
                return func if ret_type == "func" else name

    # endregion

    def version(self):
        """Check current version of the app (Bonus 6)

        :alias: v, ver
        """
        print(f"Current version: {get_version()}")

    def help(self, command: Optional[str], search_str: Optional[str] = None):
        """Show command help message. (Bonus 4&5)
        Use `help search [query]` to search for docs and commands

        :param opt command: Command Name
        :param opt search_str: Content to search, only valid when param is `search`
        """
        help_msg = [f"To-Do List Help:", ""]
        if command == "search":  # Search for commands or docs
            if not search_str:
                return self.help("h")
            search_str = search_str.lower()
            search_results = ["Search Result for `%s`" % search_str]
            have_cmd = False
            have_doc = False
            for name, func in inspect.getmembers(self, inspect.ismethod):
                if name.startswith("_"):
                    continue
                docs = func.__doc__ or ""
                curr_scope = None
                if result := re.search(Command.scope_rgx, docs):
                    curr_scope = result[1].strip()
                if curr_scope != self.scope:
                    continue
                # Search for docs
                if docs.lower().find(search_str) != -1:
                    not have_doc and search_results.append(
                        "Documentation:"
                    )
                    have_doc = True
                    search_results.append(self._extract_docs(func.__name__, docs))
                # Search for commands
                if name.find(search_str) != -1:
                    not have_cmd and search_results.append(
                        "Commands:"
                    )
                    have_cmd = True
                    search_results.append(
                        f"""{f"- `{self._get_cmd_with_param(name)}`".strip()}\n· {re.search('(.+)', docs)[1].strip()}\n"""
                    )
                elif result := re.search(self.alias_rgx, docs):
                    if search_str not in result[1].replace(" ", "").split(","):
                        continue
                    not have_cmd and search_results.append(
                        "Commands:"
                    )
                    have_cmd = True
                    search_results.append(
                        f"""{f"* `{search_str}` -> {self._get_cmd_with_param(func.__name__)}".strip()}\n· {re.search('(.+)', docs)[1].strip()}\n"""
                    )
            len(search_results) == 1 and search_results.append("No result found.")
            return print("\n\n".join(search_results))
        elif command:  # Single command help
            func = getattr(self, command, self._get_mapped_alias(command, "func"))
            return print(
                self._extract_docs(func.__name__, func.__doc__ or "")
                if func
                else f"Command Not Found: `{command}`"
            )
        members = inspect.getmembers(self, inspect.ismethod)
        members.sort(key=_sort_line_number)
        for name, func in members:
            if name.startswith("_"):
                continue
            docs = func.__doc__ or ""
            curr_scope = None
            if result := re.search(Command.scope_rgx, docs):
                curr_scope = result[1].strip()
            if curr_scope != self.scope:
                continue
            if result := re.search(r'(.+)', docs or '(No documentation provided)'):
                help_msg.append(
                    (
                            self._get_cmd_with_param(name).strip()
                            + f"\n· {result[1].strip()}\n"
                    )
                )
        print("\n".join(help_msg))

    def add(self):
        """Add a task to the list (R7)"""
        print(f"+{'-' * 24}+")
        print("| Main menu -> Add to-do |")
        print(f"+{'-' * 24}+")

        task = data_input(
            prompt="Please input new task",
            empty_err_msg="Task should not be empty. Input again."
        )
        self.task.tasks.append(task)
        print(f"Added task: '{task}'")

    def edit(self, task_number: Optional[int] = None):
        """Edit a task (Bonus 3)

        :param opt task_number: Task number to edit
        """

        print(f"+{'-' * 25}+")
        print("| Main menu -> Edit to-do |")
        print(f"+{'-' * 25}+")

        while True:
            print(self.task.list())

            if not self.task.tasks:
                return

            task_number = data_input(
                prompt="Please input task number",
                data_type=int,
                allow_negative=False,
                allow_zero=True,
                max_number=len(self.task.tasks),
                _external_input=task_number
            )
            try:
                task = self.task.tasks[task_number]
            except IndexError:
                print(f"Task number {task_number} does not exist.")
                break

            print(f"Editing task #{task_number}: '{task}'")
            new_task = data_input(
                not_empty=False,
                prompt="Please input task to replace (Leave empty to cancel)",
            )
            if not new_task.strip():
                print("Cancelled.")
                return
            print(f"Edited task #{task_number}: '{task}' -> '{new_task}'")
            self.task.tasks[task_number] = new_task
            if not data_input(
                    prompt="Do you want to edit another task? (y/N)",
                    data_type=bool,
            ):
                return True
            task_number = None

    def delete(self, task_number: Optional[int] = None):
        """Delete a task from the list (Bonus 2)

        :param opt task_number: Task number to delete
        :alias: del, remove
        """
        print(f"+{'-' * 27}+")
        print("| Main menu -> Delete to-do |")
        print(f"+{'-' * 27}+")
        print(self.task.list())

        if not self.task.tasks:
            return

        task_number = data_input(
            prompt="Please input task number",
            data_type=int,
            allow_negative=False,
            allow_zero=True,
            max_number=len(self.task.tasks),
            _external_input=task_number
        )
        try:
            task = self.task.tasks[task_number]
            del self.task.tasks[task_number]
        except IndexError:
            print(f"Task number {task_number} does not exist.")
            return
        print(f"Deleted task #{task_number}:  '{task}'")

    def move(self, completed_task_number: Optional[int] = None):
        """Move a completed task back to to-do list

        :param opt completed_task_number: Completed task to move (identified by number)
        :alias: mv
        """
        print(f"+{'-' * 29}+")
        print("| Main menu -> Move Completed |")
        print(f"+{'-' * 29}+")
        print(self.task.list(completed=True))

        if not self.task.completed_tasks:
            return

        completed_task_number = data_input(
            prompt="Please input completed task number",
            data_type=int,
            allow_negative=False,
            allow_zero=True,
            max_number=len(self.task.completed_tasks),
            _external_input=completed_task_number
        )
        try:
            task = self.task.completed_tasks[completed_task_number]
            del self.task.completed_tasks[completed_task_number]
        except IndexError:
            print(f"Completed task number {completed_task_number} does not exist.")
            return
        self.task.tasks.append(task)
        print(f"Moved completed task #{completed_task_number} to #{len(self.task.tasks) - 1}: '{task}'")

    def list(self):
        """List all to-do tasks (R8)

        :alias: ls
        """
        print(f"+{'-' * 26}+")
        print("| Main menu -> List to-dos |")
        print(f"+{'-' * 26}+")
        print(self.task.list())

    def list_completed(self):
        """List completed task(s) (Bonus 1)

        :alias: list_done, ls_done
        """
        print(f"+{'-' * 29}+")
        print("| Main menu -> List Completed |")
        print(f"+{'-' * 29}+")
        print(self.task.list(completed=True))

    def mark(self, task_number: Optional[int] = None):
        """Mark a task as completed (R9)

        Similar to `delete` command, but the task will be moved to completed list instead of deleting it.

        :param opt task_number: Task number to delete
        :alias: done, complete
        """
        print(f"+{'-' * 29}+")
        print("| Main menu -> Mark Completed |")
        print(f"+{'-' * 29}+")
        print(self.task.list())

        if not self.task.tasks:
            return

        task_number = data_input(
            prompt="Please input task number",
            data_type=int,
            allow_negative=False,
            allow_zero=True,
            max_number=len(self.task.tasks),
            _external_input=task_number
        )
        try:
            task = self.task.tasks[task_number]
            del self.task.tasks[task_number]
        except IndexError:
            print(f"Task number {task_number} does not exist.")
            return
        print(f"Completed task #{task_number}:  '{task}'")
        self.task.completed_tasks.append(task)

    # region Today

    def today(self):
        """Enters task for today's menu (R10)"""
        self.clear()
        self.task.set_scope("today")
        return True

    def today_tag(self, task_number: Optional[int] = None):
        """Tag a task for today (R11)

        :scope: today
        :param opt task_number: Task number to tag
        """
        print(f"+{'-' * 44}+")
        print("| Main menu -> Tasks for today -> Tag a task |")
        print(f"+{'-' * 44}+")
        print("Potential task for tagging.")

        # Original self.task.tasks - self.task.today_tasks (index of tasks, tagged) = untagged tasks
        available_tasks = [
            (idx, task)
            for idx, task in enumerate(self.task.tasks)
            if task not in self.task.today_tasks
        ]

        if not available_tasks:
            print("No task to tag.")
            return

        for index, (idx, task) in enumerate(available_tasks):
            print(f"{index}: {task}")

        task_number = data_input(
            prompt="Please input task number to tag",
            data_type=int,
            allow_negative=False,
            allow_zero=True,
            max_number=len(available_tasks),
            _external_input=task_number
        )
        try:
            task = available_tasks[task_number][1]
            self.task.today_tasks.append(task)
        except IndexError:
            print(f"Task number {task_number} does not exist.")
            return
        print(f"Added task #{task_number} into today list.")

    def today_untag(self, task_number: Optional[int] = None):
        """Untag a task for today (R12)

        :scope: today
        :param opt task_number: Task number to untag
        """
        print(f"+{'-' * 46}+")
        print("| Main menu -> Tasks for today -> Untag a task |")
        print(f"+{'-' * 46}+")
        print(self.task.list(today=True))

        if not self.task.today_tasks:
            print("No task to untag.")
            return

        task_number = data_input(
            prompt="Please input task number to untag",
            data_type=int,
            allow_negative=False,
            allow_zero=True,
            max_number=len(self.task.today_tasks),
            _external_input=task_number
        )
        try:
            del self.task.today_tasks[task_number]
        except IndexError:
            print(f"Task number {task_number} does not exist.")
            return

        print(f"Removed task #{task_number} in today list.")

    def today_mark(self, task_number: Optional[int] = None):
        """Mark a today task as completed (R13)

        :scope: today
        :param opt task_number: Task number to mark
        """
        print(f"+{'-' * 51}+")
        print("| Main menu -> Tasks for today -> Mark a today task |")
        print(f"+{'-' * 51}+")
        print(self.task.list(today=True))

        if not self.task.today_tasks:
            print("Nothing to mark.")
            return

        task_number = data_input(
            prompt="Please input task number to mark",
            data_type=int,
            allow_negative=False,
            allow_zero=True,
            max_number=len(self.task.today_tasks),
            _external_input=task_number
        )
        try:
            task = self.task.today_tasks[task_number]
            task_idx = self.task.tasks.index(task)
            del self.task.today_tasks[task_number]
            del self.task.tasks[task_idx]
        except IndexError:
            print(f"Task number {task_number} does not exist.")
            return

        print(f"Completed task #{task_idx}: '{task}'.")
        self.task.completed_tasks.append(task)

    def today_return(self):
        """Exit today's menu (R14)

        :scope: today
        """
        self.task.set_scope(None)
        print("Return to main menu.")

    # endregion

    def about(self):
        """About this program (R15)"""
        print(f"+{'-' * 20}+")
        print("| Main menu -> About |")
        print(f"+{'-' * 20}+")
        print("\n".join((
            "How to use:",
            "",
            "1. Input your name (Already done, your name is `%s`)" % self.task.username,
            "2. Input command to use the program (If you don't know what to do, use `help`)",
            "(Help command also includes documentation and search function for you to search for commands and docs)",
            "(To search, use `help search [query]`)",
            "3. Enjoy using this program to manage your to-do list",
            "",
            "Features:",
            "",
            "- Basic[R1-R16] (add, list, mark, today, about, quit)",
            "- Bonus[8] (list_completed, remove, move, edit, help (with search), version, clear",
            "",
            "For documentation, do `help` or `help [command]`",
            "To quick search, do `help search [query]`",
        )))
        print("=" * 35)
        print("Author: Sam (https://github.com/01101sam)")

    def clear(self):
        """Clear current console (Bonus 7)

        :alias: cls
        """
        import platform
        import os
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        print("Console cleared.")
        return True

    def quit(self):
        """Quit the program (R16)

        :alias: exit
        """
        to_do_word = "to-do"
        if len(self.task.tasks) > 1:
            to_do_word += "s"
        task_word = "task"
        if len(self.task.completed_tasks) > 1:
            task_word += "s"

        total_tasks = len(self.task.tasks) + len(self.task.completed_tasks)
        completed_tasks = len(self.task.completed_tasks)

        print(f"Goodbye, {self.task.username}. You have {total_tasks} {to_do_word} and"
              f" completed {completed_tasks} {task_word}.")
        exit(0)
