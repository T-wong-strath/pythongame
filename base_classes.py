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
        print(colored(c, color), end='',flush=True)
        time.sleep(0.05)
    print(' ',flush=True)
        
    
class Character(object):
    def __init__(self, name, health=50, attack=5, defence=5, inventory=[], inventory_space=3, playable=0, friendly=0):
        self.name = name
        self.health = health
        self.attack = attack
        self.defence = defence
        self.inventory = inventory
        self.inventory_space = inventory_space
        self.playable = playable
        self.friendly = friendly
        
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
    def __init__(self, name, item_class):
        self.name = name
        self.item_class = item_class
        
def begin_combat_encounter(characters):
    turn_order = random.shuffle(characters)
    names_list = []
    friend_list = []
    enemy_list = []
    
    for player in turn_order:
        names_list.append(player.name)
        if player.friendly or player.playable:
            friend_list.append(player.name)
        else:
            enemy_list.append(player.name)
        
    # Turns
    for player in turn_order:
        if player.playable:
            to_user('Who do you target?')
            to_user(enemy_list)
            ##### Take user command ####
            playerTarget = input()
            target = enemy_list.index(playerTarget)
        elif player.friendly:
            target = enemy_list.index(random.choice(enemy_list))
        else:
            target = friend_list.index(random.choice(friend_list))
            
    to_user(target)       
    # Choose target, 
    # Roll damage
    # Check and Add AI damage boosts
    # Check target defence boosts
    # Deduct target damage
    
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
player = Character(user_name, friendly=1)
to_user('I have a sword here for you, what will you name it?')
weapon_name = input()

# Add the weapon to the player inventory
player_weapon = Item(weapon_name, 'weapon')
player.give_item(player_weapon)

# Create an evil boi
enemy = Character('Goblin')
to_user('A wild '+str(enemy.name)+' has appeared!')

# Test comment




