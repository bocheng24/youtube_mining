# import pprint
from os import environ
from dotenv import load_dotenv
from sys import exit
from time import sleep, perf_counter
from api.client import *
import colorama
from colorama import Fore, Style


load_dotenv()
API_KEY = environ['API_KEY']

def main():

    # colorama.init(autoreset=True)


    limit_quota = int(input(f'{Fore.BLUE}{Style.BRIGHT}Enter how many quota do you want to consume youtube API:\n{Fore.RESET}{Style.RESET_ALL}'))

    api_client = Client(API_KEY, limit_quota)

    choices = {
        1: api_client.search_wflow,
        2: api_client.search_query,
        3: api_client.channel_query,
        4: api_client.playlistitems_query,
        5: api_client.search_query,
        6: api_client.channel_query,
    }

    ui = {
        '1': 'Full search workflow: search -> get all channels -> get all video ids -> get all videos details',
        '2': 'Search Only',
        '3': 'Query Channel Details only',
        '4': 'Query Playlist items only',
        '5': 'Search Only',
        '6': 'Query Channel Details only'
    }

    choice = ''

    while not choice:
        print(f'{Fore.BLUE}{Style.BRIGHT}Choose 1 of the following options:\n')

        for k, v in ui.items():
            message = f'{k}: {v}'
            print(message)

        choice = input(f'Type {', '.join(ui.keys())}: {Style.RESET_ALL}')

        if choice not in ui.keys():
            choice = ''

    choice = int(choice)

    func = choices[choice]
    func()
    print(f'{Fore.CYAN}quota used: {api_client.quota}')


if __name__ == '__main__':
    main()