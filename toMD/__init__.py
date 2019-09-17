# # -*- coding: utf-8 -*-
#
# from flask import Flask, Blueprint, jsonify
# from flask_docs import ApiDoc
# from flask_bootstrap import Bootstrap
# # from flask_moment import Moment


# !/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, jsonify, Blueprint
from flask_bootstrap import Bootstrap
from flask_docs import ApiDoc
from . import views, errors

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
bootstrap = Bootstrap(app)

# Local loading
# app.config['API_DOC_CDN'] = False

# Disable document pages
# app.config['API_DOC_ENABLE'] = False

# Api Document needs to be displayed
app.config['API_DOC_MEMBER'] = ['doc']

ApiDoc(app)


@app.route('/doc', methods=['POST'])
def get_markdown():
    """自动生成 MarkDown格式参数列表

        @@@
        ## function:

        - ##### describe:
        > 根据json自动生成 MarkDown格式参数列表
        - ##### Content-Type : ` application/json `

        ## request:


        - ### args
        从上到下依次为

        | args | descript | note |
        |:------:|:-----:|:-----:|
        | 左上文本框 (type) | 额外参数域的类型 |   用逗号分隔不同的域          |
        | 右上文本框 (value)| 额外参数域的默认值 | 与额外域是一一对应关系,损有余补不足|
        | 中间文本框 (json)| 需要的json格式数据 | 也可以为Python的dict/list |


        - ####  The sample

        ##### No.1
        type=null

        value=null

        json: {"1":"false"}

        | args | type |
        | :----:|:----: |
        |   1  |  str  |

        ##### No.2
        type=str,list

        value=2

        json: {"1":"false"}

        | args | type | str | list |
        | :----:|:----:|:----:|:----: |
        | 1 | str |   |    |


        @@@
        """
    return jsonify({'api': 'add data'})









