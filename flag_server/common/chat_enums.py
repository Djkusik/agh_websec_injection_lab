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
    password_correct = 10
    message_incorrect = 11
    wrong_task = 12
    invalid_flag = 13
    solved_already = 14
    task_solved = 15
    wrong_lab_no = 16
    wrong_stats_mode = 17


class ClientMessage(Enum):
    exit = 1