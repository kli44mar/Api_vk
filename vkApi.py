import argparse
import requests


def get_friends(first_name, last_name, user_ids, access_token, count='100'):
    print(f'Список друзей {first_name} {last_name}:')
    url = 'https://api.vk.com/method/friends.get?user_id={user_ids}&fields=city,country&count={count}&access_token={access_token}&v=5.92'
    url_formatted = url.format(user_ids=user_ids, count=count, access_token=access_token)
    res_friends = requests.get(url_formatted).json()
    for friend in res_friends["response"]["items"]:
        try:
            print(
                f'{friend["first_name"]} {friend["last_name"]} {friend["city"]["title"]} {friend["country"]["title"]}')
        except KeyError:
            print(
                f'{friend["first_name"]} {friend["last_name"]}')


def get_wall(first_name, last_name, user_ids, access_token, count=100):
    url = 'https://api.vk.com/method/wall.get?owner_id={user_ids}&count={count}&access_token={access_token}&v=5.92'
    url_formatted = url.format(user_ids=user_ids, count=count, access_token=access_token)
    res_wall = requests.get(url_formatted).json()
    print(f'Текст записей {first_name} {last_name}:')
    for post in res_wall["response"]['items']:
        try:
            if post["text"]:
                print(post["text"])
        except KeyError:
            print('Нет текста у записей')


def get_groups(first_name, last_name, user_ids, access_token, count=100):
    url = 'https://api.vk.com/method/groups.get?user_id={user_ids}&extended=1&count={count}&access_token={access_token}&v=5.92'
    url_formatted = url.format(user_ids=user_ids, count=count, access_token=access_token)
    res_groups = requests.get(url_formatted).json()
    print(f'Название сообществ {first_name} {last_name}:')
    for group in res_groups["response"]['items']:
        try:
            print(group['name'])
        except KeyError:
            print('Нет сообществ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Api Вконтакте')
    parser.add_argument('access_token', type=str, help='Access token')
    parser.add_argument('user_ids', type=str, help='Id пользовател')
    parser.add_argument('-f', '--friends', action="store_true", help='Список друзей')
    parser.add_argument('-w', '--wall', action="store_true", help='Текст записей')
    parser.add_argument('-g', '--groups', action="store_true", help='Список групп')
    parser.add_argument('-c', '--count', type=int, help="Кол-во")
    args = parser.parse_args()
    try:
        res_users = requests.get(
            f'https://api.vk.com/method/users.get?user_ids={args.user_ids}&name_case=gen&access_token={args.access_token}&v=5.92')
        person = res_users.json()["response"][0]

        first_name = person["first_name"]
        last_name = person["last_name"]
        if args.friends:
            get_friends(first_name, last_name, args.user_ids, args.access_token, args.count)
        if args.wall:
            get_wall(first_name, last_name, args.user_ids, args.access_token, args.count)
        if args.groups:
            get_groups(first_name, last_name, args.user_ids, args.access_token, args.count)
    except requests.exceptions.ConnectionError:
        print("Нет подключение к интернету.")
    except:
        print('Неправильно введены данные')
