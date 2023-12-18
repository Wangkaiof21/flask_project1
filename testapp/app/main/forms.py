#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/12 0:56
# @Author  : v_bkaiwang
# @File    : forms.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from flask_wtf import FlaskForm
from wtforms import FileField, FieldList, SelectField, FormField, StringField, SubmitField
"""

:param FileField: 渲染文件上传字段。默认情况下，该值将是在表单数据中发送的文件名。
:param FieldList: 封装相同字段类型的多个实例的有序列表，
以列表的形式保存数据。authors = FieldList(StringField('Name'， [validators.required()]))
:param SelectField: 表示 选择表单元素
:param FormField: 将一个表单封装为另一个表单中的字段。
:param StringField: 这个字段是大多数更复杂字段的基础，并且 ' <input type="text"> ' '
:param SubmitField: <input type="submit"> ' ' <input type="submit"> ' '这允许检查是否给定 已按下提交按钮。
:return: 
"""


class UploadFrom(FlaskForm):
    feature = SelectField(label='特性', choices=[])
    file = FileField('上传测试结果')
    submit = SubmitField('确认')

    @staticmethod
    def allowed_file():
        return True


class PerfSelectFrom(FlaskForm):
    base_choices = [('All', '所有')]
    benchmark = SelectField(label='Benchmark', choices=base_choices, default='All')
    test_case_name = SelectField(label='TestCaseName', choices=base_choices, default='All')
    submit = SubmitField('查询')
    
    
class SubSelectGroup(FlaskForm):
    temp_choices = [("temp", "temp")]
    match_opr_choices = [
        ('等于', '等于'),
        ('正则', '正则'),
        ('大于', '大于'),
        ('小于', '小于'),
        ('大于等于', '大于等于'),
        ('小于等于', '小于等于')
    ]
    col_name = SelectField(label='col_name', choices=temp_choices)
    match_opr = SelectField(label='match_opr', choices=temp_choices, default='等于')
    match_value = StringField(label='match_value')


class SelectFromPro(FlaskForm):
    selector_list = FieldList(FormField(SubSelectGroup), min_entries=0)
    add = SubmitField('新增条件')
    delete = SubmitField('删除条件')
    submit = SubmitField('查询')
