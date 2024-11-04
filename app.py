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
        2: api_client.channels_wflow,
        3: api_client.playlistitems_wflow,
        4: api_client.videos_wflow
    }

    ui = {
        '1': 'Full search workflow: search -> get all channels -> get all video ids -> get all videos details',
        '2': 'Channels workflow: get all channels -> get all video ids -> get all videos details',
        '3': 'Video IDs workflow: get all video ids -> get all videos details',
        '4': 'Videos details workflow: get all videos details',
    }

    choice = ''

    while not choice:
        print(f'{Fore.BLUE}{Style.BRIGHT}Choose 1 of the following options:\n')

        for k, v in ui.items():
            message = f'{k}: {v}'
            print(message)

        choice = input(f'Type 1, 2, 3, 4: {Style.RESET_ALL}')

        if choice not in ui.keys():
            choice = ''

    choice = int(choice)

    func = choices[choice]
    func()


if __name__ == '__main__':
    main()