from yandex_music import Client
import win32api
import os

token_file = "token.txt"

def check_token():
    try:
        with open('token.txt', 'r') as f:
            token = f.read()
        print(
            "\nФайл с токеном найден!\n\nЕсли вы хотите его поменять или удалить, просто удалите файл token.txt в папке с программой.\nПосле чего перезапустите программу.\n")
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
    disk_list = []
    for i, disk in enumerate(disks):
        volume = win32api.GetVolumeInformation(disk)[0]
        full_name_disk = (f'{i}: {disk} - {volume}')
        disk_list.append(full_name_disk)
    for n in range(len(disk_list)):
        print(disk_list[n])

    while True:
        user_select_disc = input(
            '\nНапишите НОМЕР диска на который хотите записать всю музыку из плейлиста "МНЕ НРАВИТСЯ" и нажмите Enter:')
        try:
            user_select_disc = int(user_select_disc)
            if 0 <= user_select_disc < len(disks):
                print(f'Вы выбрали диск под номером: {user_select_disc}')
                return_disc = disks[user_select_disc]
                return return_disc
            else:
                print(f'\nВы ввели номер неправильно. Пример корректного ввода: 2')
                for n in range(len(disk_list)):
                    print(disk_list[n])
        except ValueError:
            print(f'\nВы ввели номер неправильно. Пример корректного ввода: 0')
            for n in range(len(disk_list)):
                print(disk_list[n])


def main():
    yandex_token = check_token()
    client = Client(yandex_token).init()

    liked_tracks_short = client.users_likes_tracks()
    tracks_list = liked_tracks_short.tracks
    track_count = len(tracks_list)

    if track_count == 0:
        print("У вас нет ни одного трека в плейлисте 'Мне нравится'.")
        return

    download_folder = select_disk()
    print(f'Начинаю скачивание {track_count} треков из плейлиста "Мне нравится"...')

    for i, track_short in enumerate(tracks_list):
        print(f"Обработка трека {i + 1}/{track_count}...")

        # Этот блок try...catch отлавливает ошибки на этапе ПОДГОТОВКИ трека
        try:
            liketrack = track_short.fetch_track()

            artist_names = [name_artist.name for name_artist in liketrack.artists]
            all_artist_string = ", ".join(artist_names)
            track_name = f'{liketrack.title} - {all_artist_string}'

            # Заменяем символы, недопустимые в имени файла
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                track_name = track_name.replace(char, '_')

            full_path = os.path.join(download_folder, f"{track_name}.mp3")

            # Если файл уже есть, просто пропускаем его и переходим к следующему
            if os.path.exists(full_path):
                print(f"[ПРОПУСК] - '{track_name}' (файл уже существует)")
                continue

            # --- НАЧАЛО БЛОКА ПОВТОРНЫХ ПОПЫТОК ---
            max_retries = 3  # Максимальное количество попыток
            retry_delay = 10  # Пауза между попытками в секундах

            for attempt in range(max_retries):
                try:
                    print(f"[СКАЧИВАНИЕ] - '{track_name}' (Попытка {attempt + 1}/{max_retries})")
                    liketrack.download(full_path)
                    print(f"[УСПЕХ]")
                    break  # Если скачалось успешно, выходим из цикла попыток

                except Exception as e:
                    print(f"!!! Ошибка при скачивании: {e}")
                    # Если это не последняя попытка, ждем и пробуем снова
                    if attempt < max_retries - 1:
                        print(f"!!! Повторная попытка через {retry_delay} секунд...")
                        time.sleep(retry_delay)
                    else:
                        # Если это последняя попытка, сообщаем о неудаче
                        print(
                            f"!!! Не удалось скачать трек '{track_name}' после {max_retries} попыток. Переходим к следующему.")
            # --- КОНЕЦ БЛОКА ПОВТОРНЫХ ПОПЫТОК ---

        except Exception as e:
            # Этот блок сработает, если ошибка произошла еще до скачивания (например, не удалось получить инфу о треке)
            print(f"!!! Критическая ошибка при обработке трека на позиции {i + 1}: {e}")
            print("!!! Переходим к следующему треку.")
            continue

    print("\nСкачивание завершено!")


main()