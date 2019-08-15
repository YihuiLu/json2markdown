# -*- coding: utf-8 -*-
"""
Convert the api blueprint/request+response string to
    the markdown-formatted string
Author: Yunbo Chen
Email: chen-robert@163.com
"""
import re
from toMD.jsontotable import JsonToMDTable


# sample API blueprint:
# # POST /pinstreet/promote/egg_edu/api/v1/exchange
#
# + Request (application/json; charset=utf-8)
#
#     + Headers
#
#             uid: super_YH
#
#     + Body
#
#             {
#                 "ea_id": "64",
#                 "exchange_info": "9"
#             }
#
# + Response 400 (application/json)
#
#         {"error_code": 1000,
#         "msg": {"exchange_info": ["This field is required."]},
#         "request": "POST /pinstreet/promote/egg_edu/api/v1/exchange"}


class MDConvertor:
    # api blueprint的Markdown模板
    api_blueprint_template = """{0}

@@@
## function:

- ##### Description:
    > {0}
- ##### Login authentication :   ` True `


## API Blueprint:

```
{1}
```


## request:


- ### headers

| args | nullable | type | remark |
|:------:|:-----:|:-----:|:------:|
| token  | false | str   | token  |


- ### args

{2}                                             |


## return:
- ### args

{3}


@@@
        """
    # sample request/response json:
    # {
    #       "proposal_list" :[{"id":"146","approve":"1"}]
    #   }
    # {
    #       "error_code": 0,
    #       "msg": "success",
    #       "request": "POST /pinstreet/bms/api/update_proposal_approve"
    #   }

    # 原版的Mardown模板
    original_template = """{0}

@@@
## function:

- ##### Description:
    > {0}
- ##### Login authentication :   ` True `
- ##### Content-Type : ` application/json `


## request:

- ### headers

| args | nullable | type | remark |
|:------:|:-----:|:-----:|:------:|
| token  | false | str   | token  |


- ### args

{1}                                             |

- #### Request the sample:
```
{2}
```
    
## return:
- ### args

{3}

- #### responseType: ` json `
```
{4}
```
@@@

"""
    # original string
    original_str = ""
    # flag to indicate whether it's api template or the original one
    # api_template_flag = True
    # extracted jsons
    extracted_jsons = []
    # regex string
    regexStr_header = r'^#[^+]+\s+\+ Request[^+]+\+ Headers[^+]+\+ Body[^+]+\+ Response[^+]+$'
    regexStr_noheader = r'^#[^+]+\s+\+ Request[^+]+\+ Response[^+]+$'
    empty_responseTable = """| args | type | remark |
|:------:|:-----:|:-----:|
"""

    # 检查是不是两个JSON的格式并提取JSON
    def check2jsons(self, originStr):
        if originStr[0] != '{':
            # 第一个字符必须是{
            return False
        jsonstr = "{"
        stack = ['{']
        try:
            for s in originStr[1:]:
                if s == '{':
                    stack.append('{')
                elif s == '}':
                    stack.pop()
                    if len(stack) == 0:
                        # 一个大JSON结束，一共应该2个
                        self.extracted_jsons.append(jsonstr + s)
                        jsonstr = ""
                        continue
                jsonstr += s
            # 结束应该没有多的括号而且一共两个大Json
            if len(stack) == 0 and (len(self.extracted_jsons) == 1 or 2):
                return True
            else:
                return False
        except:
            return False

    # 检查是不是API Blueprint的格式并提取JSON
    def checkAPIFormat(self, originstr):
        # 第一位必须是'#'
        if originstr[0] != '#':
            return False
        if re.match(self.regexStr_noheader, originstr):
            # without header
            # get request  Json
            bodytag = re.search(r'\+ Request[^{]+', originstr)
            bodystr = bodytag.group(0)
        elif re.match(self.regexStr_header, originstr):
            # with header and body
            # get Body Json
            bodystr = "+ Body"
        else:
            # not valid
            return False
        startpos = originstr.find(bodystr) + len(bodystr)
        endpos = originstr.find("+ Response")
        self.extracted_jsons.append(originstr[startpos:endpos])
        # get response json
        bodytag = re.search(r'\+ Response[^{]+', originstr)
        bodystr = bodytag.group(0)
        startpos = originstr.find(bodystr) + len(bodystr)
        self.extracted_jsons.append(originstr[startpos:])
        return True

    # init, set up everything, initial check
    def __init__(self, originStr):
        self.error_msg = ""
        self.error_flag = False
        self.original_str = originStr
        # extracted jsons
        self.extracted_jsons = []
        self.api_template_flag = True
        self.one_json = False
        # check the string type first
        if self.check2jsons(originStr.strip()):
            self.api_template_flag = False
            if len(self.extracted_jsons) == 1:
                self.one_json = True
        elif not self.checkAPIFormat(originStr.strip()):
            # format is not working
            self.error_flag = True
            self.error_msg = "输入的数据格式不对,看是否括号/引号不匹配"
        elif len(self.extracted_jsons) != 2:
            # something is wrong,
            # can't extract exactly two (request and response) jsons
            print("length of extracted json: {}".format(len(self.extracted_jsons)))
            self.error_flag = True
            self.error_msg = "输入的request/response JSON格式不对,看是否括号/引号不匹配"

    # 自动帮newline indent
    def autoIndent(self, strr, level):
        ret = ""
        for s in strr:
            if s == '\n':
                ret += '\n'
                for i in range(level):
                    ret += '    '
            else:
                ret += s
        return ret

    # main
    def gimmeThat(self, description, args, ultra):
        if self.error_flag:
            return self.error_msg
        # 预处理null, false, true情况
        for i in range(len(self.extracted_jsons)):
            self.extracted_jsons[i] = re.sub(r':[ ]*false', ': False', self.extracted_jsons[i])
            self.extracted_jsons[i] = re.sub(r':[ ]*true', ': True', self.extracted_jsons[i])
            self.extracted_jsons[i] = re.sub(r'(?i):[ ]*null', ': "NULL"', self.extracted_jsons[i])
        # 先处理只有一个JSON的情况
        if self.one_json:
            try:
                jsonified = eval(self.extracted_jsons[0].strip())
            except:
                self.error_flag = True
                self.error_msg = "输入的json格式有误，请检查一下"
                return self.error_msg
            md = JsonToMDTable(jsonified, args, ultra)
            return md.core()
        # 把拿到的JSON都变成MD table
        request_extra_value = ['nullable', 'remark']
        request_extra_args = ["False", ""]
        try:
            jsonified = eval(self.extracted_jsons[0].strip())
        except:
            self.error_flag = True
            self.error_msg = "输入的request json格式有误，请检查一下"
            return self.error_msg
        request_table = JsonToMDTable(jsonified, request_extra_args,
                                      request_extra_value)
        request_table = request_table.core()
        # same for response, except specific regular params
        filtered = ["error_code", "msg", "request"]
        response_json = {}
        try:
            jsonified = eval(self.extracted_jsons[1].strip())
        except:
            self.error_flag = True
            self.error_msg = "输入的response json格式有误，请检查一下"
            return self.error_msg
        # check if all the elements in filtered is present
        all_present = True
        for f in filtered:
            if f not in list(jsonified.keys()):
                all_present = False
        if all_present:
            # filter them
            for (key, value) in jsonified.items():
                if key not in filtered:
                    # add it
                    response_json[key] = value
        else:
            response_json = jsonified
        # if empty add empty
        if response_json == {}:
            response_table = """| args | type | remark |
|:------:|:-----:|:-----:|
"""
        else:
            response_extra_value = ["remark"]
            response_extra_args = [""]
            response_table = JsonToMDTable(response_json, response_extra_args,
                                           response_extra_value).core()
        # 根据不同的输入格式输出不同的API documentation
        finalMD = ""
        if self.api_template_flag:
            finalMD = self.api_blueprint_template.format(description,
                                                         self.autoIndent(self.original_str, 1),
                                                         self.autoIndent(request_table, 0),
                                                         self.autoIndent(response_table, 0))
        else:
            # original template
            finalMD = self.original_template.format(description,
                                                    self.autoIndent(request_table, 0),
                                                    self.autoIndent(self.extracted_jsons[0].strip(), 0),
                                                    self.autoIndent(response_table, 0),
                                                    self.autoIndent(self.extracted_jsons[1].strip(), 0))
        return finalMD
