import xadmin

from .models import *


class ClassifyAdmin(object):
    list_display = ['class_name', 'class_head', 'class_desc']
    search_fields = ['class_name']
    list_filter = ['class_name']


class BankXlsxAdmin(object):
    list_display = ['bank_name', 'bank_type', 'bank_xlsx', 'bank_nums', 'bank_chio', 'bank_chios', 'bank_judge',
                    'bank_gap', 'bank_person', 'bank_bs']
    search_fields = ['bank_name', 'bank_type', 'bank_xlsx', 'bank_nums', 'bank_chio', 'bank_chios', 'bank_judge',
                     'bank_gap', 'bank_person', 'bank_bs']
    list_filter = ['bank_name', 'bank_type', 'bank_xlsx', 'bank_nums', 'bank_chio', 'bank_chios', 'bank_judge',
                   'bank_gap', 'bank_person', 'bank_bs']


class Ques_choiceAdmin(object):
    list_display = ['question', 'answer', 'choiceA', 'choiceB', 'choiceC', 'choiceD', 'score', 'choi_id']
    search_fields = ['question']
    list_filter = ['question', 'score']


class Ques_choicesAdmin(object):
    list_display = ['question', 'answer', 'choiceA', 'choiceB', 'choiceC', 'choiceD', 'score', 'chois_id']
    search_fields = ['question']
    list_filter = ['question', 'score']


class Ques_judgeAdmin(object):
    list_display = ['question', 'answer', 'score', 'judge_id']
    search_fields = ['question']
    list_filter = ['question', 'score']


class Ques_gapAdmin(object):
    list_display = ['question', 'answer', 'score', 'gap_id']
    search_fields = ['question']
    list_filter = ['question', 'score']


class GameAdmin(object):
    list_display = ['game_name', 'game_nums', 'game_score', 'create_time', 'end_time', 'time_bar', 'game_rule',
                    'class_game', 'bank_game']
    search_fields = ['game_name']
    list_filter = ['game_name', 'game_nums', 'game_score', 'time_bar', 'game_rule']


class GameInfoAdmin(object):
    list_display = ['total', 'times', 'ginfo_game', 'ginfo_user']
    search_fields = ['total']
    list_filter = ['total', 'times']


xadmin.site.register(Classify, ClassifyAdmin)
xadmin.site.register(BankXlsx, BankXlsxAdmin)
xadmin.site.register(Ques_choice, Ques_choiceAdmin)
xadmin.site.register(Ques_choices, Ques_choicesAdmin)
xadmin.site.register(Ques_judge, Ques_judgeAdmin)
xadmin.site.register(Ques_gap, Ques_gapAdmin)
xadmin.site.register(Game, GameAdmin)
xadmin.site.register(GameInfo, GameInfoAdmin)
