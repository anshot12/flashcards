import os
import random
import re
import logging
import shutil
import sys
import argparse
logging.basicConfig(format="%(message)s", filename="hardest card.txt", filemode="a", level="INFO")
parser = argparse.ArgumentParser()

parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()


class LoggerOut:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.filename = filename

    def write(self, message):
        self.terminal.write(message)
        with open(self.filename, "a") as file:
            print(message, file=file, flush=True, end='')

    def flush(self):
        pass


class LoggerIn:
    def __init__(self, filename):
        self.terminal = sys.stdin
        self.filename = filename

    def readline(self):
        entry = self.terminal.readline()
        with open(self.filename, "a") as file:
            print(entry.rstrip(), file=file, flush=True)
        return entry


default_log = 'default.txt'
sys.stdout = LoggerOut(default_log)
sys.stdin = LoggerIn(default_log)


def convert_log(statistic):
    with open("hardest card.txt", "r", encoding="utf-8") as statistic_file:
        all_error_cards = []
        count_error = statistic
        count_error.clear()
        for line in statistic_file:
            error_card = re.sub(r"C>\S+\s", "", line).replace("W>", "")
            error_card = error_card.replace("\n", "")
            all_error_cards.append(error_card)
        for error_card in all_error_cards:
            if error_card == "":
                del error_card
            else:
                count_error.setdefault(error_card, 0)
                count_error[error_card] += 1
    return count_error


def hardest_card(statistic):
    counter = 0
    errors = []
    for error, values in statistic.items():
        if values == (max(statistic.values())):
            errors.append(error)
            counter += 1
    if counter == 0:
        print("There are no cards with errors.")
    elif counter == 1:
        print(f'The hardest card is "{errors[0]}". You have {statistic[errors[0]]} errors answering it')
    elif counter == 2:
        print(f'The hardest cards are "{errors[0]}", "{errors[1]}".You have {statistic[errors[0]]} errors answering them')


def log(statistic):
    file = input("File name:\n")
    shutil.copy("default.txt", file)
    print("The log has been saved.")


def reset(statistic):
    with open("hardest card.txt", "w", encoding="utf-8") as statistic_file:
        count_error = statistic
        count_error.clear()
        statistic_file.writelines("")
    return count_error, print("Card statistics have been reset.")


def add(have_cards):
    new_key = input(f"The term for new card:\n")
    while new_key in have_cards.keys():
        new_key = input(f'The card "{new_key}" already exists. Try again:\n')
    new_value = input(f"The definition for new card:\n")
    while new_value in have_cards.values():
        new_value = input(f'The definition "{new_value}" already exists. Try again:\n')
    else:
        new_card = {new_key: new_value}
    return print(f'The pair ("{new_key}":"{new_value}") has been added\n'), have_cards.update(new_card)


def remove(have_cards):
    old_card = input("Which card?\n")
    if old_card in have_cards.keys():
        have_cards.pop(old_card)
        print("The card has been removed.\n")
    else:
        print(f'Can\'t remove "{old_card}": there is no such card.\n')
    return have_cards


def export(new_cards):
    if args.export_to:
        file = args.export_to
    else:
        file = input("File name:\n")
    with open(file, "w", encoding="utf-8") as file_open:
        for card, value in new_cards.items():
            print(f"{card} - {value}", file=file_open)
    print(f"{len(new_cards)} cards have been saved")


def importing(have_cards):
    if args.import_from:
        file = args.import_from
    else:
        file = input("File name:\n")
    count = 0
    if os.path.isfile(file):
        with open(file, "r", encoding="utf-8") as file_open:
            for line in file_open:
                card = re.sub(r" - \S+\s", "", line)
                defenition = re.sub(r"\S+ - ", "", line).replace("\n", "")
                importing_card = {card: defenition}
                have_cards.update(importing_card)
                count += 1
            convert_log(statistics)
            return print(f"{count} cards have been loaded.\n"), have_cards
    else:
        print("File not found.\n")


def ask(have_cards):
    have_cards = cards
    num_of_card = int(input("How many times to ask?\n"))
    term = 0
    while term != num_of_card:
        card = random.choice(list(have_cards.keys()))
        answer = input(f'Print the definition of "{card}":\n')
        if answer == have_cards[card]:
            print("Correct!"), logging.info(f"C>{card}")
        elif answer in list(have_cards.values()) and answer != have_cards[card]:
            print(f'Wrong. The right answer is "{have_cards[card]}", but your definition is correct for '
                  f'"{list(have_cards.keys())[list(have_cards.values()).index(answer)]}"'), logging.info(f"W>{card}")
        else:
            print(f'Wrong. The right answer is "{have_cards[card]}"'), logging.info(f"W>{card}")
        term += 1
    convert_log(statistics)


def exits(have_cards):
    with open("hardest card.txt", "w", encoding="utf-8") as exit_file:
        exit_file.writelines("")
    exit_stats = statistics
    exit_stats.clear()
    pass


info_card = {}
cards = {}
statistics = {}
actions = {"add": add, "remove": remove, "import": importing, "export": export, "ask": ask,
           "exit": exits, "log": log, "hardest card": hardest_card, "reset stats": reset}
while True:
    if args.import_from:
        actions["import"](cards)
    key = input(f"Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
    if key in actions.keys():
        if key == "exit":
            actions[key](statistics)
            print("Bye bye!")
            if args.export_to:
                actions["export"](cards)
            break
        elif key == "convert":
            actions[key](statistics)
        elif key == "hardest card":
            actions[key](statistics)
        elif key == "ask":
            actions[key](cards)
        elif key == "reset stats":
            actions[key](statistics)
        else:
            actions[key](cards)


