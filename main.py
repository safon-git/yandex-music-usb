from yandex_music import Client
import win32api
import os

token_file = "token.txt"

def check_token():
    try:
        with open('token.txt', 'r') as f:
            token = f.read()
        print("Файл с токеном найден!\nЕсли вы хотите его поменять или удалить, просто удалите файл token.txt в папке с программой.\nПосле чего перезапустите программу.\n")
        return token

    except FileNotFoundError:
        print("Файл с токеном не найден")
        user_token = input('Введите ваш Яндекс токен, гайд на программу в моем ТГК https://t.me/safon_qa:').strip()
        with open('token.txt', 'w') as f:
            f.write(user_token)
        print('Токен сохранен!')
        return user_token

def select_disk():
    alldisk = win32api.GetLogicalDriveStrings().split('\0')
    disks = [valid_disk for valid_disk in alldisk if valid_disk]

    print('Список дисков по номерам:')
    for i, disk in enumerate(disks):
        volume = win32api.GetVolumeInformation(disk)[0]
        print(f'{i}: {disk} - {volume}')

    while True:
        user_select_disc = input('\nНапишите НОМЕР диска на который нужно записать всю музыку из плейлиста "МНЕ НРАВИТСЯ" и нажмите Enter:')
        try:
            user_select_disc = int(user_select_disc)
            if 0<= user_select_disc < len(disks):
                print(f'Вы выбрали диск под номером: {user_select_disc}')
                return_disc = disks[user_select_disc]
                return return_disc
            else:
                print(f'Вы ввели номер неправильно. Пример корректного ввода: 2')
        except ValueError:
                print(f'Вы ввели номер неправильно. Пример корректного ввода: 0')


def main():
    yandex_token = check_token()
    client = Client(yandex_token).init()

    my_like_tracks = client.users_likes_tracks()
    tracks_list = my_like_tracks.tracks

    track_count = len(tracks_list)

    download_folder = select_disk()
    print('Начинаю скачивание всех треков из плейлиста "Мне нравится"')

    for i in range (0, track_count):
        liketrack = client.users_likes_tracks()[i].fetch_track() #сканирую треки в нравиться
        artist_names = []

        for name_artist in liketrack.artists: #записываю всех артистов на треке
            artist_names.append(name_artist.name)

        all_artist_string = ", ".join(artist_names) #преобразовываю список в строку с запятой
        track_name = f'{liketrack.title} - {all_artist_string}'

        full_path = f"{download_folder}/{track_name}.mp3"

        if not os.path.exists(full_path):
            print (f"[СКАЧИВАНИЕ] - '{track_name}'")
            liketrack.download(full_path)
        elif os.path.exists(full_path):
            print(f"[ПРОПУСК] - '{track_name}' (файл уже существует)")
        else:
            liketrack.download(full_path)

main()