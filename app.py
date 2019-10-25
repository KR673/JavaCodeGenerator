# -*- coding: UTF-8 -*-
'''
Created on 2018年7月10日
通过模板自动生成java文件,可生成controller,service,dao,entity层等类,提供简单的list,findById,delete,save,update,page方法
@author: JL
'''
import shutil
import os
import json
import time
import tarfile
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)

@app.route('/index')
def index():
    with open('./templates/param_input.txt', 'r', encoding = 'utf-8') as file:
        param = {'param': file.read()}
    return render_template('create_class.html', **param)

@app.route('/createClass', methods=['GET', 'POST'])
def create_class():
    fields = request.form['fields']
    with open('./templates/param_input.txt', 'wb') as file:
        file.write(fields.encode('utf-8'))

    file_name = msg = None
    # {'column': {'age': 'int', 'id': 'String', 'address': 'String', 'name': 'String'}, 'table': 'cc_user'}
    if len(fields) <= 0:
        msg='request data json is null!'
    
    j = json.loads(fields, encoding='utf-8')
    if len(j['class']) <= 0 or len(j['package']) <= 0:
        msg = 'className | package is null!'

    param = set_param(j)

    if not msg or len(msg) <= 0:
        d = time.strftime("%Y-%m-%d", time.localtime())

        entity = request.form.get('entity')
        if entity and len(entity) >= 1:
            print('--- create entity class')
            create_entity(param)

        service = request.form.get('service')
        if service and len(service) >= 1:
            print('--- create service class')
            create_service(param)
            create_service_impl(param)
            
        controller = request.form.get('controller')
        if controller and len(controller) >= 1:
            print('--- create controller class')
            create_controller(param)

    return render_template('create_class.html', msg=msg, file_name=file_name)

def set_param(page_data):
    columns = page_data['column']
    propertys = ''
    if columns:
        for key in columns.keys():
            propertys += '\tprivate %s %s;' % (columns[key], key) + '\n'

    c = {'package': page_data['package'],
         'real_entity_dto_package':page_data['entityPackage'],
         'entity_package': page_data['entityPackage'] + '.' +page_data['class'],
         'entity_dto_package': page_data['entityDtoPackage'] + '.' + page_data['class'] + 'Dto',
         'service_package':page_data['package'] + '.service.' + page_data['class'] + 'Service',
         'dao_package': page_data['daoPackage'] + '.' +page_data['class'] + 'Mapper',
         'class_name': page_data['class'],
         'small_class_name':small_str(page_data['class']),
         'propertys': propertys,
         'description':page_data['function'],
         'author':page_data['author'],
         'date': time.strftime("%Y-%m-%d", time.localtime())}
    return c

# 创建entity
def create_entity(param):
    s = render_template('entity_dto_templates.html', **param)
    create_java_file(param['class_name'] + 'Dto', param['package'] + '.entity', s)

# 创建Service
def create_service(param):
    s = render_template('service_templates.html', **param)
    create_java_file(param['class_name'] + 'Service', param['package'] + '.service', s)

# 创建ServiceImpl
def create_service_impl(param):
    s = render_template('service_Impl_templates.html', **param)
    create_java_file(param['class_name'] + 'ServiceImpl', param['package'] + '.serviceImpl', s)

# 创建controller
def create_controller(param):
    s = render_template('controller_templates.html', **param)
    create_java_file(param['class_name'] + 'Controller', param['package'] + '.controller', s)


# 将首字母转换为小写
def small_str(s):
    if len(s) <= 1:
        return s
    return (s[0:1]).lower() + s[1:]


# 创建java文件
def create_java_file(class_name, package, text, suffix='.java'):
    
    dirs = 'D:/temp/python/' + package.replace('.', '/') + '/'

    if os.path.exists(dirs):
            shutil.rmtree(dirs)

    os.makedirs(dirs, 0o777)

    fd = os.open(dirs + class_name + suffix, os.O_WRONLY | os.O_CREAT)
    os.write(fd, text.encode(encoding="utf-8", errors="strict"))
    os.close(fd)

# #生成tar.gz压缩包
# def make_targz():
#     file_name = 'com.tar.gz'
#     source_dir = 'D:/temp/python/'
#     with tarfile.open(file_name, "w:gz") as tar:
#         tar.add(source_dir, arcname=os.path.basename(source_dir))
#     return file_name

# @app.route("/download/<filename>", methods=['GET'])
# def downloader(filename):
#     # 指定文件下载目录，默认为当前项目根路径
#     dirpath = os.path.join(app.root_path, '')
#     # as_attachment=True 表示下载
#     return send_from_directory(dirpath, filename, as_attachment=True)


if __name__ == '__main__':
    app.run()
