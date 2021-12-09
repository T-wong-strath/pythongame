# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 22:10:03 2021

@author: Timothy
"""

"""
1. Implement a map

"""

from termcolor import colored
import time
import random

messages_dict = {
    "narrator" : "yellow",
    "enemy" : "cyan",
    "friendly" : "blue"
    }

def to_user(message,message_type="narrator"):
    color = messages_dict[message_type]
    for c in message:
        print(colored(c, color), end='')
        time.sleep(0.05)
    print(' ')
        
    
class Character(object):
    def __init__(self, name, health=50, attack=5, defence=5, inventory=[], inventory_space=3, playable=0, friendly=0, equipped=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.defence = defence
        self.inventory = inventory
        self.inventory_space = inventory_space
        self.playable = playable
        self.friendly = friendly
        self.equipped = equipped
        
    def equip_item(self, item):
        if self.equipped is None:
            self.equipped = item
            to_user(item.name + ' has been equipped.')
        else:
            to_user(self.equipped.name + ' is currently equipped.')
            to_user('Do you want to replace it with ' + item.name + '? [Y/N]')
            
            while True:
                equip = input()
                if equip == 'Y':
                    self.equipped == item
                    to_user(item.name + ' has been equipped.')
                    break
                elif equip == 'N':
                    to_user(item.name + ' has not been equipped.')
                    break
                else:
                    to_user('Speak up traveller, please say Y or N')

        
    def give_item(self, item):
        if isinstance(item,Item):
            self.inventory.append(item)
            to_user(str(item.name)+' has been added to your inventory!')
        elif len(self.inventory) >= self.inventory_space:
            to_user('Your inventory is full!')
        else:
            to_user('You can\'t put that in your inventory!')
    
    # def remove_item(self, item):
    #     item_names_in_inventory = []
    #     for owned_item in self.inventory:
    #         item_names_in_inventory.append(owned_item.name)
    #     if item in item_named_in_inventory:
    #         self.inventory.
        
class Item(object):
    def __init__(self, name, item_class, attackRange=[0,2]):
        self.name = name
        self.item_class = item_class
        self.attackRange = attackRange
        
def begin_combat_encounter(turn_order):
    random.shuffle(turn_order)
    names_list = []
    friend_list = []
    enemy_list = []
    
    for player in turn_order:
        names_list.append(player.name)
        if player.friendly or player.playable:
            friend_list.append(player.name)
        else:
            enemy_list.append(player.name)
        
    
    for player in turn_order:
        
        # Choose target
        if player.playable:
            to_user('Who do you target?')
            to_user(enemy_list)
            ##### Take user command ####
            playerTarget = input()
            target_idx = names_list.index(playerTarget)
        elif player.friendly:
            to_user(player.name + ' is taking a turn')
            target_idx = names_list.index(random.choice(enemy_list))
        else:
            to_user(player.name + ' is taking a turn')
            target_idx = names_list.index(random.choice(friend_list))
            
        target = turn_order[target_idx]
        to_user(player.name + ' targets ' + target.name)
        
        # Roll damage
        if player.equipped is not None:
            attkRange = player.equipped.attackRange
            attack = player.attack + random.randint(attkRange[0],attkRange[1])
        else:
            attack = player.attack
        ### Check attack augments ###
        
        # Check target defence
        if target.defence >= attack:
            damage = 0
        else:
            damage = attack - target.defence
        ### Check defence boosts ###
        to_user(player.name + ' deals ' + str(damage) + ' damage!')
       
        # Deduct target health 
        target.health -= damage
        print(target.name + '\'s new health is: ' + str(target.health))

    # CHECK HEALTH STATUS 
    # REMOVE DEAD FROM LIST
    # IF ENEMYLIST NOT EMPTY, TAKE NEW TURN
    return


"""
Game run code
"""        
# Game welcome message and prompt for user name input
to_user('Welcome to the best game in the land')
to_user('Please enter thine name:')
user_name = input()

# Reply and ask for weapon name
to_user('Hello '+user_name+'!')
player = Character(user_name, friendly=1, playable =1)
to_user('I have a sword here for you, what will you name it?')
weapon_name = input()

# Add the weapon to the player inventory
player_weapon = Item(weapon_name, 'weapon', attackRange=[5,10])
player.give_item(player_weapon)

# Equip item
to_user('Let\'s equip ' + player_weapon.name)
player.equip_item(player_weapon)

# Create an evil boi
enemy = Character('Goblin')
to_user('A wild '+str(enemy.name)+' has appeared!')

# Begin combat
characters = [player,enemy]
begin_combat_encounter(characters)


