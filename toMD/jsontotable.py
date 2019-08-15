# -*- coding: utf-8 -*-
"""
    email: zhangmeng.lee@foxmail.com
"""


class JsonToMDTable:
    md_text = []

    def __init__(self, data, bonus_values=list(), bonus_titles=list()):
        """
        根据json自动生成 MarkDown格式参数列表
        :param data: 此时data为python的dict/list
        :param bonus_titles: 除['args', 'type']之外用户手动补充的表头，必须为"list"格式
        """
        assert isinstance(bonus_titles, list), "`title` Data Error"
        assert isinstance(bonus_values, list), "`list` Data Error"

        self.data = data
        self.titles = ['args', 'type'] + bonus_titles
        self._title_sp = ':--------:'  # 表头与表行的分割标志
        self._dividing = ' | '  # 列的分割标志
        self._fill = "|".join(['   ' for i in bonus_titles])
        self.bonus_values = bonus_values
        self.bonus_titles = bonus_titles

        self.md_text = []  # 整个markdown文档
        self.head = []  # 统一的表头
        self.rows = []
        self.bonus = []  # 设置的额外项
        self.tables = []  # 总共的表

    # 创建统一表头
    def built_head(self):
        titles = [title for title in self.titles]
        md_head = self._dividing.join(titles)
        md_dividing_line = '|'.join([self._title_sp for title in range(len(titles))])
        self.head = [md_head, md_dividing_line]
        # self.rows.append()

    # 新增的数据域和数据值.bonus_values与bonus_titles一一对应
    def built_bonus_values_title(self):
        bonus = self.bonus_values
        if not self.bonus_titles:  # 如果没有额外的参数域,那么就算有额外参数值,也不采用
            self.bonus = []
            return
        if len(self.bonus_values) == len(self.bonus_titles):
            pass
        else:
            if len(self.bonus_values) > len(self.bonus_titles):
                bonus = self.bonus_values[:len(self.bonus_titles)]
            else:
                bonus = bonus + (len(self.bonus_titles) - len(self.bonus_values)) * [" "]
        self.bonus = bonus

    # 完成当前表,为下一个表做准备
    def data_to_rows(self, data, secondary_title):
        rows = []  # 当前表的元素,包括表头和表行
        rows.extend(self.head)
        for idx, key in enumerate(data):
            value = data.get(key)
            args_type = type(value).__name__
            if isinstance(value, str):
                args_type = 'str'
                try:
                    int(value)
                    args_type = 'int'
                except ValueError:
                    try:
                        float(value)
                        args_type = 'float'
                    except ValueError:
                        pass
            # null situation
            if value == 'NULL':
                args_type = 'unknown'
            # 类型
            # args_type = str(type(value)).replace("<class '", '').replace("'>", "")
            # 如果值为复杂结构,只需要第一个元素
            if isinstance(value, dict):
                if value:
                    self.tables.append([key, value])
                else:
                    pass
            if isinstance(value, list):
                try:
                    if isinstance(value[0], dict):
                        args_type = 'ObjectList'  # 如果为列表嵌套字典,定义为ObjectList类型
                    self.tables.append([key, value[0]])
                except IndexError:  # 此列表为空列表
                    pass
            # 如果值是字典,或者列表,标识出来
            args = "<u style='color:red'>{}<u>".format(key.replace('\n', '')) if isinstance(value,
                                                                                            (dict, list)) else str(key)
            row = [args, args_type]
            if not self.bonus:
                pass
            else:
                row.extend(self.bonus)

            rows.append(self._dividing.join(row))

        self.md_text.append('- ' + str(secondary_title) if secondary_title else 'Overall')
        self.md_text.append(self._dividing + str(" |\n| ".join(rows)) + self._dividing)

    def core(self, data=None, secondary_title=None):
        data = data if data else self.data
        self.built_head()
        self.built_bonus_values_title()
        # 将data转换成md表行元素
        # 如果data是list,那么有多组表.否则只有一组表
        # 注意:每一组表可能有多个表,因为一个dict可能嵌套别的dict或者list
        if isinstance(data, list):
            for index, value in enumerate(data):
                self.data_to_rows(value, secondary_title)
                break
        elif isinstance(data, dict):
            self.data_to_rows(data, secondary_title)
        if self.tables:
            table = self.tables[0]
            del self.tables[0]
            return self.core(data=table[1], secondary_title=table[0])

        return "\n\n\n".join(self.md_text)

    # 原始版本
    # def core(self, data=None, secondary_title=None):
    #     data = data if data else self.data
    #     self.built_head()
    #     self.built_bonus_values_title()
    #     # 将data转换成md表行元素
    #     # 如果data是list,那么有多组表.否则只有一组表
    #     # 注意:每一组表可能有多个表,因为一个dict可能嵌套别的dict或者list
    #     if isinstance(data, list):
    #         for index, value in enumerate(data):
    #             tables = self.data_to_rows(value, secondary_title)
    #             break
    #     # elif isinstance(data, dict):
    #     #     for nest_key, nest_value in data:
    #     #         tables.append
    #     else:
    #         tables = self.data_to_rows(data, secondary_title)
    #     if tables:
    #         for table in tables:
    #             return self.core(data=table[1], secondary_title=table[0])
    #
    #     return "\n\n\n".join(self.md_text)
