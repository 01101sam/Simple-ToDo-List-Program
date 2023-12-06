from typing import Optional, Union, Type


def data_input(not_empty: bool = True, data_type: Union[Type[str], Type[int]] = str,
               allow_negative: bool = False,
               allow_zero: bool = False,
               max_number: Union[int, float, None] = None,
               prompt: Optional[str] = None,
               empty_err_msg: Optional[str] = None,
               _external_input=None
               ):
    """
    This function is used to get input from the user.

    :param not_empty: Whether the input can be empty or not. (str: "", int: 0, float: 0.0, bool: False, obj: {})
    :param data_type: The type of the data that the user is inputting.
    :param allow_negative: Whether the input can be negative or not. (Only works when data type is number type)
    :param allow_zero: Whether the input can be zero or not. (Only works when data type is number type)
    :param max_number: The maximum number that the user can input. (Only works when data type is number type)
    :param prompt: The prompt that will be displayed to the user. (If empty, only a colon will be displayed)
    :param empty_err_msg: The error message that will be displayed to the user if the input is empty.
    :param _external_input: This parameter is only used when user's input is from external function.
    :return: The data that the user inputted.
    """
    if not prompt:
        prompt = ""
    prompt += ": "

    while True:
        data: str
        if _external_input is not None:
            print(f"{prompt}{_external_input}")
            data = _external_input
        else:
            data = input(prompt)
        if not_empty and not data and data_type is not bool:
            print(empty_err_msg or "Error. Input can not be empty, please try again.")
            continue
        try:
            if data_type is bool:
                # Change y(es) / n(o) / 1 / 0 to True / False
                if data.lower() in ("y", "yes", "1"):
                    data = True  # noqa
                elif data.lower() in ("", "n", "no", "0"):
                    data = False  # noqa
            data = data_type(data)
        except ValueError:
            print("Error. Expected a number input.")
            continue
        if data_type in (int, float):
            data: Union[int, float]
            if not allow_negative and data < 0:
                print("Error. Expected a positive number input.")
                continue
            if not allow_zero and data == 0:
                print("Error. Expected a non-zero number input.")
                continue
            if max_number is not None and data >= max_number:
                print("Error. Out of range task number.")
                continue

        return data


def pause():
    input("\nPress Enter to return.")


def get_version() -> str:
    """
    This function is used to get the version of the program.

    :return: The version of the program.
    """
    return "1.1"
