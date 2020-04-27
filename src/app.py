import os
import time

from sanic import Sanic
from sanic.response import json, file_stream
from xxhash_cffi import xxh32_hexdigest
import aiofiles

from src.sanic_motor import BaseModel
from src.models import File

MONGODB_URI = os.environ.get('MONGODB_HOST', 'mongodb://127.0.01:27017/filebed')
BASE_URL = 'http://127.0.0.1:8000'


async def get_unix_time():
    return int(time.time())


App = Sanic('filebed')

App.config.update(
    {
        # Motor config
        'MOTOR_URI': MONGODB_URI,
        'LOGO': None,
    }
)


BaseModel.init_app(App)

# 提供文件夹`static`里面的文件到URL `/static`的访问。
App.static('/static', './static')
App.static('/upload', './upload')

BASE_UPLOAD_FOLDER = 'upload'


@App.route('/')
async def index_page(request):
    return await file_stream('static/index.html')


@App.route('/files/')
async def files_page(request):
    return await file_stream('static/files.html')


@App.route('/api/files/')
async def files_page(request):
    qs = await File.find(
        {}, sort='create_at desc'
    )
    datalist = []

    for obj in qs.objects:
        item = {
            'file': BASE_URL + '/' + obj['path'],
            'url':  BASE_URL + '/' + obj['path'],
            'type':obj['type'],
            'name':obj['name'],
            'create_at': obj['create_at']
        }
        datalist.append(item)

    return json({'data': datalist, 'code': 0})


async def write_file(path, body):

    async with aiofiles.open(path, 'wb') as f:
        await f.write(body)
    f.close()


@App.route('/upload', methods=['POST'])
async def upload_api(request):
    upload_file = request.files.get('file')
    name = request.form.get('name')
    ftype = request.form.get('type')

    folder_path = '{}/{}'.format(
        BASE_UPLOAD_FOLDER,
        str(int(time.time()))
    )
    file_type = ftype.split('/')[0]

    file_ext = name.split('.')[-1]

    file_path = '{}/{}'.format(folder_path, xxh32_hexdigest(name).decode('utf-8') + '.{}'.format(file_ext))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    await write_file(file_path, upload_file.body)

    result = await File.insert_one({
        'name': name,
        'type': file_type,
        'path': file_path,
        'create_at': await get_unix_time(),
    })
    mission_id = str(result.inserted_id)

    return json(True)
