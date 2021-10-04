import commands
import setup


def program():
    userInput = setup.voice()

    if "create" and "user" in userInput:
        commands.createUser()

    elif "shutdown" or "quit" or "end" or "bye" in userInput:
        commands.endProgram()


if __name__ == "__main__":
    while True:
        program()
