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
import sys

messages_dict = {
    "narrator" : "yellow",
    "enemy" : "cyan",
    "friendly" : "blue"
    }

def to_user(message,message_type="narrator"):
    color = messages_dict[message_type]
    for c in message:
        print(colored(c, color), end='')
        #time.sleep(0.05)
    print(' ')
        
    
class Character(object):
    def __init__(self, name, player=0, health=50, attack=5, defence=5, inventory=[], inventory_space=3, playable=0, friendly=0, equipped=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.defence = defence
        self.inventory = inventory
        self.inventory_space = inventory_space
        self.player = player
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
        
    while enemy_list:
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
            
            # Take damage or die
            if damage >= target.health:
                if target.player:
                    to_user('~ You died ~')
                    sys.exit('Thanks for playing')
                else:
                    # Kill target
                    to_user(target.name + ' is dead.')
                    
                    # Remove from player lists
                    turn_order.pop(names_list.index(target.name))
                    names_list.pop(names_list.index(target.name))
                    if target.name in friend_list:
                        friend_list.pop(friend_list.index(target.name))
                    elif target.name in enemy_list:
                        enemy_list.pop(enemy_list.index(target.name))
    
                    # Check if no more enemies
                    if not enemy_list:
                        break
            else:
                # Deduct target health 
                target.health -= damage
                to_user(target.name + '\'s new health is: ' + str(target.health))
    
    # Victory message
    to_user('You have vanquished all foes and lived to tell the tale')

        
    return 

def generate_characters(characterType):
    health = 0
    attack = 0
    defence = 0
    
    if characterType == 'friendly':
        friendly = 1
    else:
        friendly = 0
        
    # Generate character attribute dict
    # Spawn chance, health limits, attack limits, defence limits
    attributesDict = {
        'Goblin' : [[80],[20,30],[10,15],[0,5]],
        'Elf' : [[40],[40,60],[20,25],[5,10]],
        'Dragon':[[5],[200,230],[100,150],[30,50]],
        }
    
    while health==0:
        # Roll spawn chance
        spawn_roll = random.randint(0,100)
        
        # Randomly select mob type
        mob_choice = random.choice(list(attributesDict.items()))
        # Check acceptance
        if spawn_roll <= mob_choice[1][0]:
            # Spawn attributes
            health = random.randint(mob_choice[1][1][0],mob_choice[1][1][1])
            attack = random.randint(mob_choice[1][2][0],mob_choice[1][2][1])
            defence = random.randint(mob_choice[1][3][0],mob_choice[1][3][1])

    name = mob_choice[0]+random.randint(0,10)
    characterClass = Character(name=name, attack=attack, health=health, defence = defence, friendly=friendly)
    
    return characterClass
"""
Game run code
"""        
# Game welcome message and prompt for user name input
to_user('Welcome to the best game in the land')
to_user('Please enter thine name:')
user_name = input()

# Reply and ask for weapon name
to_user('Hello '+user_name+'!')
player = Character(user_name, health=100, friendly=1, playable =1, player=1)
to_user('I have a sword here for you, what will you name it?')
weapon_name = input()

# Add the weapon to the player inventory
player_weapon = Item(weapon_name, 'weapon', attackRange=[15,20])
player.give_item(player_weapon)

# Equip item
to_user('Let\'s equip ' + player_weapon.name)
player.equip_item(player_weapon)

# Create an evil boi
# enemy = Character('Goblin', attack=5)
# to_user('A wild '+str(enemy.name)+' has appeared!')

# # Begin combat
# characters = [player,enemy]
# begin_combat_encounter(characters)

#-----------------

# Create an evil boi
enemy = Character('Goblin', attack=45,health=100)
to_user('A wild '+str(enemy.name)+' has appeared!')

# Create friend
friend = Character('Fred', attack=1, health=1, friendly=1)
to_user('But have no fear, ' + str(friend.name)+ ' has appeared!')

# Begin combat
characters = [player,enemy,friend]
begin_combat_encounter(characters)
