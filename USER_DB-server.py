from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {}<br>".format(artist)
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def new_album():
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    # Запросим список альбомов этого артиста
    album_list = album.find(album_data["artist"])
    # Получим список названий этих альбомов
    album_names = [album.album for album in album_list]
    # Если альбом, который хотим добавить, есть в списке, то вернем ошибку
    if album_data["album"] in album_names:
        message = "Альбом с таким названием уже имеется в базе."
        response = HTTPError(409, message)
    else:
        # Тут были перепутаны названия, восстановил по смыслу всё
        if not album.data_stack_valid(album_data):
            message = "Не все требуемые данные были введены."
            response = HTTPError(449, message)
        elif not album.year_valid(album_data["year"]):
            message = "Указанное значение не может быть годом."
            response = HTTPError(400, message)
        else:
            new_album = album.add_album(album_data)
            album.save_album(new_album)
            response = "Альбом успешно сохранен."

    return response
    # resource_path = save_album(album_data)
    # print("Albums saved at: ", resource_path)

    # return "Данные успешно сохранены"

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)