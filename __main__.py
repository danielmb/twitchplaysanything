from multiprocessing import Process, Manager, Value, Array
from ahk import AHK
import random
import time


def handleKeyboard(key, input, ahk):
    if (input == True):
        ahk.key_down(key)
    else:
        ahk.key_up(key)


def punch(key, input, ahk):
    if (input == True):
        ahk.click()
    else:
        pass


def get_votes(inputs):
    # generate random votes with w a s d keys  and put it to the list inputs
    while True:
        for i in range(0, random.randint(1, 100)):
            # create a list from keys

            inputs.append(random.choice(['w', 'a', 's', 'd', 'r']))
        time.sleep(0.1)


def handle_votes(inputs):

    # handle the votes and put it to the list outputs
    ahk = AHK(executable_path=r'G:\Program Files\AutoHotkey\AutoHotkey.exe')
    keyHeld = None
    keys = {
        'w': {
            'key': 'w',
            'action': handleKeyboard
        },
        'a': {
            'key': 'a',
            'action': handleKeyboard
        },
        's': {
            'key': 's',
            'action': handleKeyboard
        },
        'd': {
            'key': 'd',
            'action': handleKeyboard
        },
        'r': {
            'key': 'r',
            'action': punch
        }
    }
    while True:
        votes = {}
        for key in keys:
            votes[key] = 0
        for (i, vote) in enumerate(inputs):
            vote = vote.lower()
            if vote in votes:
                votes[vote] += 1
        # get the key with the highest votes
        key = max(votes, key=votes.get)
        # if the key is different from the previous key, print the key
        if key != keyHeld:
            print("key {} won with {} votes".format(key, votes[key]))

            if keyHeld != None:
                keys[keyHeld]['action'](keyHeld, False, ahk)
            keys[key]['action'](keys[key]['key'], True, ahk)
            keyHeld = key
        else:
            print("key {} won with {} votes but is already pressed".format(
                key, votes[key]))

        inputs[:] = []
        time.sleep(0.5)


# run get_votes in parallelwasdwdsw
if __name__ == '__main__':
    manager = Manager()
    inputs = manager.list()

    p1 = Process(target=get_votes, args=(inputs,))
    p2 = Process(target=handle_votes, args=(inputs, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
