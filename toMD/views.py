# -*- coding: utf-8 -*-
import json

from flask import redirect, url_for, render_template, flash

from toMD import app
from toMD.forms import MDForm
from toMD.doc2md import MDConvertor


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MDForm()
    if form.validate_on_submit():
        # 传进来的数据初始状态为字符串
        inputs = form.packets.data
        if not inputs:
            flash('你还没有输入数据')
            return render_template('index.html', form=form)
        # feed in string
        convertor = MDConvertor(inputs.strip())
        des = form.des.data
        args = form.args.data
        ultra = form.ultra.data
        # ''.split(',') -> ['']
        bonus_values = args.split(",")  # 实际类型
        title = ultra.split(",")  # 类型域
        bonus_values = list(filter(None, bonus_values))
        title = list(filter(None, title))  # 去除空白字符
        markdown = convertor.gimmeThat(des, bonus_values, title)
        return render_template("index.html", form=form, markdown=markdown, set_tab=1)

    return render_template("index.html", form=form)

# # 首先确保需要确保js为python的dict/list数据格式,但不能是空列表
# try:
#     # 如果来自表单的数据为dict格式
#     inputs = eval(inputs)
# except (NameError, SyntaxError):
#     try:
#         # the JSON object must be str, bytes or bytearray, not dict
#         inputs = json.loads(inputs)  # 如果正确执行,此时js已经成为dict
# # 执行失败,说明来自表单的数据本身已经为dict
#     except (NameError, json.decoder.JSONDecodeError, SyntaxError): # 再次捕获异常,说明数据格式不对
#         flash('输入的数据格式不对,看是否括号/引号不匹配')
#         return render_template('index.html', form=form)
# else:
#     if not inputs:
#         flash('你不能输入一个空列表')
#         return render_template('index.html', form=form)
#
# args = form.args.data
# ultra = form.ultra.data
#
# # ''.split(',') -> ['']
# bonus_values = args.split(",")    # 实际类型
# title = ultra.split(",")   # 类型域
# bonus_values = list(filter(None, bonus_values))
# title = list(filter(None, title)) # 去除空白字符
# # return str(title)
#
# markdown = JsonToMDTable(data=inputs, bonus_values=bonus_values, bonus_titles=title).core()
