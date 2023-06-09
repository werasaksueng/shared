## pip install dropbox

import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

## https://www.dropbox.com/developers/apps
## Expire daily
ACCESS_TOKEN = 'sl.Bf-2GqhrZIvR0ofiZ-CsiW0ED5WfavnyOkaAuhKZTzFJ1ZHslmTYTwwGAZfEGLl_dkYcvE4CnD9OFpPtNJ6a3DR745Dytb6dbedZHGSv4a7hV0WF9P3T0wxEae2kmw3O2FzDya8'

def connect():
    try:
        return dropbox.Dropbox(ACCESS_TOKEN)
    except AuthError as e:
        print('Error: ' + str(e))
# print(connect())

import os
def download(dir_):
    try:
        names = []
        dbx = connect()
        res = dbx.files_list_folder('/' + dir_)
        for en in res.entries:
            names.append(en.name)

        os.mkdir(dir_)
        for n in names:
            file = dir_ + '/' + n
            print(file)
            dbx.files_download_to_file(download_path=file, path='/'+file)
    except Exception as e:
        print(e)
download('software')
