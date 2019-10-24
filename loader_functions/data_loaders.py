import os
import shelve

def save_game(player, entities, game_map, message_log, game_state):
    with shelve.open('save', 'n') as data_file:
        data_file['player_index']=entities.index(player)
        data_file['entities']=entities
        data_file['game_map']=game_map
        data_file['message_log']=message_log
        data_file['game_state']=game_state

def load_game():
    if not os.path.isfile('save.dat'):
        raise FileNotFoundError

    with shelve.open('save', 'r') as data_file:
        player_index=data_file['player_index']
        entities=data_file['entities']
        player=entities[player_index]
        game_map=data_file['game_map']
        message_log=data_file['message_log']
        game_state=data_file['game_state']
    
    return player, entities, game_map, message_log, game_state