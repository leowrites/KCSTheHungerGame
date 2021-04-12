import player
import numpy as np
import random

# game related utility functions
# only return game values, player attributes are directly changed using getter/setter

# max amount of death per round
max_death = 5

food_dict = {
    "chicken club": 5,
    "farmer's wrap": 2,
    "Ice Cap": 1,
    "Hot Lunch": 10
}

misc_kill_str = np.array([
    "{} was burnt out from five English assignments",
    "{} was got hit by a car on the way to Ferrara's",
    "{} failed physics and died.",
    "{} asked too many questions and died.",
    "{} had gay thoughts and died.",
    "{} talked to the grade 10s and died.",
])

dir_kill_str = np.array([
    "{} smashed a Foundation of Mathematics and Pre-Calculus 10 textbook into {}'s head, end up killing them",
    "{} turned the volume of {}'s headphone to max and killed them",
    "{} thought {} was the mole that gave away the grad asking list and decided to kill them"
])

morale_factor = np.array([
    ["{} got 7 out of 8 on a 1984 reading assignment and is sad", -5],
    ["{} couldn't do correction for the physics test and is sad", -2],
    ["{} feels really happy after winning a trivia", 5]
     ])

health_factor = np.array([
    ["{} is bleeding for no apparent reason.", -6],
    ["{} is out of breath after Mr.Martins forced them to run around monson five times.", -3],
    ["{} fainted after hearing there is a final for Pre Cal", -3]])

food_list = np.array([
    "chicken club",
    "farmer's wrap",
    "Ice Cap",
    "Hot Lunch"
])

event_list = np.array([
    "food",
    "attack",
    "death",
    "morale",
    "health"
])


# -----------conditional events-----------


def give_stuff(player_name):
    # give either weapon or food, triggered by probability for each character
    # all items will be used in this round
    food = random.choice(food_list)
    food_announcer(player_name, food)
    return food


def death_generator(player1, player2):
    # if max death is reached, this function won't be called
    p_array = np.array([player1, player2])
    np.random.shuffle(p_array)
    dir_death_announcer(p_array[1].name, p_array[0].name)
    p_array[0].alive = False


def random_death(this_player):
    this_player.alive = False
    misc_death_announcer(this_player.name)


def morale_changer(this_player):
    text, value = random.choice(morale_factor)
    if this_player.morale + int(value) > 10:
        this_player.morale = 10
    elif this_player.morale <= 0:
        # loop through all players at the end of the round and remove the dead ones
        this_player.alive = False
        print(f"{this_player.name} died because of low morale")
    else:
        this_player.morale += int(value)
    health_morale_announcer(this_player.name, text)


def health_changer(this_player):
    text, value = random.choice(health_factor)
    if this_player.health + int(value) > 10:
        this_player.health = 10
    elif this_player.health <= 0:
        this_player.alive = False
        print(f"{this_player.name} died because of low health")
    else:
        this_player.health += int(value)
    health_morale_announcer(this_player.name, text)


# -----------must happen functions-----------


def heal(player1, item):
    c_health = player1.health
    if (c_health + food_dict.get(item)) < 10:
        player1.health += food_dict.get(item)
    else:
        player1.health = 10


def consume_food(this_player):
    # maybe don't consume if the player's health is max
    arr = np.array(this_player.inventory)
    if this_player.health != 10 and arr.size != 0:
        for i in this_player.inventory:
            heal(this_player, i)


# -----------utility-----------

def ask_input():
    try:
        size = int(input("How many players do you want?"))
    except ValueError as err:
        print("Error! Please try again", err)
        return ask_input()
    return size


def create_players():
    size = ask_input()
    player_list = []
    for i in range(size):
        new_player = player.Player(input("Input player name here: "))
        player_list.append(new_player)
    player_list = np.array(player_list)
    return player_list


def count_day(day_number):
    day_number += 1
    return day_number


def event_generator(players_left, death_count):
    # we run this for each character
    # first determine the condition of the player, then determine if give stuff
    # something must happen to every player every round
    # each player is passed in individually
    # if there are more than 1 player left, it is possible to trigger a two player event
    if death_count < max_death and players_left.size > 1:
        # if the player is not the last player
        event = random.choices(event_list, weights=(30, 20, 50, 35, 40), k=1)
    else:
        event = np.array(["food"])

    if event[0] == "attack":
        player_involved = np.array([players_left[0], players_left[1]])
        remains = np.delete(players_left, [0, 1], axis=None)
    else:
        player_involved = players_left[0]
        remains = np.delete(players_left, 0, axis=None)
    return event[0], player_involved, remains


def shuffle_players(players):
    return np.random.shuffle(players)


def continue_to_next_round(day):
    input(f'Press any key to continue to Day {day}')


def food_announcer(player_name, food):
    print(f'{player_name} was given a {food} from a sponsor')


def dir_death_announcer(player1_name, player2_name):
    text = random.choice(dir_kill_str)
    print(text.format(player1_name, player2_name))


def misc_death_announcer(player_name):
    text = random.choice(misc_kill_str)
    print(text.format(player_name))


def health_morale_announcer(player_name, text):
    print(text.format(player_name))


def winning(player_alive_array):
    if player_alive_array.size == 1:
        return True
    else:
        return False


def print_alive_name(player_alive):
    print("Registered Players:")
    for i in player_alive:
        print(i.name)


def report(player_alive, player_dead):
    print("Player Alive Status:")
    for i in player_alive:
        print(f'Name: {i.name}\tHealth: {i.health}\tMorale: {i.morale}')
    print("Player Dead: ")
    if player_dead is not None and player_dead.size != 0:
        for i in player_dead:
            print(i)
