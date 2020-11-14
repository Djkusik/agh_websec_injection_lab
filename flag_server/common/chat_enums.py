from enum import Enum

class ServerMessage(Enum):
    exit = 1
    nick_taken = 2
    nick_invalid = 3
    nick_correct = 4
    connection_established = 5
    password_empty = 6
    user_already_registered = 7
    registered = 8
    password_incorrect = 9
    message_incorrect = 10
    wrong_task = 11
    invalid_flag = 12
    solved_already = 13
    task_solved = 14
    wrong_lab_no = 15
    wrong_stats_mode = 16


class ClientMessage(Enum):
    exit = 1