import utility
import numpy as np


class Game:
    day = 0
    death_count = 0
    player_alive = None
    player_dead = np.array([], dtype=str)
    running = True

    def __init__(self):
        self.player_alive = utility.create_players()
        utility.print_alive_name(self.player_alive)
        self.game_loop()

    def game_loop(self):
        while self.running:
            if utility.winning(self.player_alive):
                print(f'{self.player_alive[0].name} is the winner!')
                exit(0)
                break
            self.death_count = 0
            self.day = utility.count_day(self.day)
            utility.continue_to_next_round(self.day)
            print(f'\n\n----------Day {self.day}----------')
            np.random.shuffle(self.player_alive)
            remains = self.player_alive
            for player in self.player_alive:
                if player in remains:
                    event, player_involved, remains = utility.event_generator(remains, self.death_count)
                    if event == "food":
                        player_involved.inventory.append(utility.give_stuff(player_involved.name))
                    elif event == "attack":
                        utility.death_generator(player_involved[0], player_involved[1])
                        self.death_count += 1
                    elif event == "death":
                        utility.random_death(player_involved)
                        self.death_count += 1
                    elif event == "morale":
                        utility.morale_changer(player_involved)
                    elif event == "health":
                        utility.health_changer(player_involved)
                    if player.alive:
                        utility.consume_food(player)
            # remove dead players
            for player in self.player_alive:
                if not player.alive:
                    self.player_alive = np.delete(self.player_alive, np.argwhere(self.player_alive == player))
                    self.player_dead = np.append(self.player_dead, player.name)

            utility.report(self.player_alive, self.player_dead)
