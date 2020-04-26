import os
import time

from sanic import Sanic
from sanic.response import json, file_stream
from xxhash_cffi import xxh64
import aiofiles

app = Sanic('App Name')

# 提供文件夹`static`里面的文件到URL `/static`的访问。
app.static('/static', './static')

BASE_UPLOAD_FOLDER = './upload'


@app.route('/')
async def index_page(request):
    return await file_stream('static/index.html')


@app.route('/files/')
async def files_page(request):
    return await file_stream('static/files.html')


@app.route('/api/files/')
async def files_page(request):
    datalist = [
        {'file': 'https://cattalk.in/static/catlogo.gif', 'url': 'https://cattalk.in/static/catlogo.gif', 'create_at': '-', 'type': 'image'},
        {'file': 'https://cattalk.in/static/catlogo.gif', 'url': 'https://cattalk.in/static/catlogo.gif', 'create_at': '-', 'type': 'image'},
        {'file': 'https://cattalk.in/static/catlogo.gif', 'url': 'https://cattalk.in/static/catlogo.gif', 'create_at': '-', 'type': 'image'},
        {'file': 'https://cattalk.in/static/catlogo.gif', 'url': 'https://cattalk.in/static/catlogo.gif', 'create_at': '-', 'type': 'image'},
        {'file': 'https://cattalk.in/static/catlogo.gif', 'url': 'https://cattalk.in/static/catlogo.gif', 'create_at': '-', 'type': 'image'},
        {'file': 'https://cattalk.in/static/catlogo.gif', 'url': 'https://cattalk.in/static/catlogo.gif', 'create_at': '-', 'type': 'image'},
        {'file': 'https://cattalk.in/static/catlogo.gif', 'url': 'https://cattalk.in/static/catlogo.gif', 'create_at': '-', 'type': 'image'},
    ]
    return json({'data': datalist, 'code': 0})


async def write_file(path, body):

    async with aiofiles.open(path, 'wb') as f:
        await f.write(body)
    f.close()


@app.route('/upload', methods=['POST'])
async def upload_api(request):
    upload_file = request.files.get('file')
    name = request.form.get('name')

    folder_path = '{}/{}'.format(
        BASE_UPLOAD_FOLDER,
        str(time.time())
    )
    file_path = '{}/{}'.format(folder_path, name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    await write_file(file_path, upload_file.body)

    return json(True)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
