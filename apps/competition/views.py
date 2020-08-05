import json
import os
import random
import xlrd

from django.http import StreamingHttpResponse, Http404
from django.shortcuts import render, redirect

from Exam.settings import BACKUP_ROOT
from .models import *


# 首页
def index(request):
    class_datas = Classify.objects.all()
    return render(request, 'web/index.html', {'class_datas': class_datas})


# 考试分类详情
def class_detail(request, str):
    if request.user.is_authenticated:
        type = Classify.objects.get(class_name=str)
        game_datas = Game.objects.filter(class_game_id=type.id)

        return render(request, 'competition/games.html', {'game_datas': game_datas})
    else:
        return render(request, 'login.html')


# 录入、配置题库首页
def set_index(request):
    if request.user.is_authenticated:
        return render(request, 'setgames/index.html')
    else:
        return render(request, 'login.html')


# 录制题库
def set_bank(request):
    back_class = Classify.objects.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            bank_name = request.POST.get('bank_name', '')
            bank_type = request.POST.get('bank_type')
            bank_template = request.FILES.get('template', None)
            if bank_name and bank_type and bank_template:
                if not bank_template:
                    return render(request, 'err.html')
                if bank_template.name.split('.')[-1] not in ['xls', 'xlsx']:
                    return render(request, 'err.html')
                bank = BankXlsx.objects.filter(bank_name=bank_name)
                xlsx = BankXlsx.objects.filter(bank_xlsx=bank_template)
                if not bank and not xlsx:
                    # 上传题库到backup文件夹
                    bank_repo = open(os.path.join(BACKUP_ROOT, bank_template.name), 'wb+')
                    for chunk in bank_template.chunks():
                        bank_repo.write(chunk)
                    bank_repo.close()

                    # 取出xlsx格式 题库里面的题
                    data = xlrd.open_workbook('backup/{}'.format(bank_template))
                    table = data.sheets()[0]
                    num1 = 0
                    num2 = 0
                    num3 = 0
                    num4 = 0
                    for i in range(1, table.nrows):
                        ti_type = table.row_values(i)[0]
                        if ti_type == '单选题':
                            num1 += 1
                        elif ti_type == '多选题':
                            num2 += 1
                        elif ti_type == '判断题':
                            num3 += 1
                        elif ti_type == '填空题':
                            num4 += 1
                        else:
                            pass

                    # 添加到题库录入表
                    bank_data = BankXlsx(bank_name=bank_name, bank_type=bank_type, bank_xlsx=bank_template,
                                         bank_nums=table.nrows - 1, bank_chio=num1, bank_chios=num2, bank_judge=num3,
                                         bank_gap=num4, bank_person=0, bank_bs=0)
                    bank_data.save()

                    # 添加到各个类型的题表
                    bank1 = BankXlsx.objects.get(bank_name=bank_name)
                    for i in range(1, table.nrows):
                        ti_type = table.row_values(i)[0]
                        if ti_type == '单选题':
                            question = table.row_values(i)[1]
                            answer = table.row_values(i)[2]
                            A = table.row_values(i)[3]
                            B = table.row_values(i)[4]
                            C = table.row_values(i)[5]
                            D = table.row_values(i)[6]
                            if question and answer and A and B and C and D:
                                cun1 = Ques_choice(question=question, answer=answer, choiceA=A, choiceB=B, choiceC=C,
                                                   choiceD=D, score=5, choi_id_id=bank1.id)
                                cun1.save()
                            else:
                                pass
                        elif ti_type == '多选题':
                            question = table.row_values(i)[1]
                            answer = table.row_values(i)[2]
                            A = table.row_values(i)[3]
                            B = table.row_values(i)[4]
                            C = table.row_values(i)[5]
                            D = table.row_values(i)[6]
                            if question and answer and A and B and C and D:
                                cun2 = Ques_choices(question=question, answer=answer, choiceA=A, choiceB=B, choiceC=C,
                                                    choiceD=D, score=5, chois_id_id=bank1.id)
                                cun2.save()
                            else:
                                pass
                        elif ti_type == '判断题':
                            question = table.row_values(i)[1]
                            answer = table.row_values(i)[2]
                            if question and answer:
                                cun3 = Ques_judge(question=question, answer=answer, score=5, judge_id_id=bank1.id)
                                cun3.save()
                            else:
                                pass
                        elif ti_type == '填空题':
                            question = table.row_values(i)[1]
                            answer = table.row_values(i)[2]
                            if question and answer:
                                cun4 = Ques_gap(question=question, answer=answer, score=5, gap_id_id=bank1.id)
                                cun4.save()
                            else:
                                pass
                        else:
                            pass

                else:
                    return render(request, 'setgames/bank.html', {'class_datas': back_class, 'err': '题库名/题库文件已存在'})
            else:
                return render(request, 'setgames/bank.html', {'class_datas': back_class, 'err': '数据不完整'})
        return render(request, 'setgames/bank.html', {'class_datas': back_class})
    else:
        return render(request, 'login.html')


# 题库模板下载
def template_download(request):
    file_name = 'web/static/template/template.xlsx'
    try:
        # StreamingHttpResponse 下载大文件
        response = StreamingHttpResponse(open(file_name, 'rb'))
        # 防止输出文件乱码
        response['content_type'] = "application/octet-stream"  # 指示传输内容的类型
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_name)  # 以附件的形式下载保存
        return response
    except Exception:
        raise Http404


# 配置考试
def set_test(request):
    con = ''
    type = request.GET.get('type', '')
    bank = request.GET.get('bank')
    class_datas = Classify.objects.all()
    bank_datas = BankXlsx.objects.all()
    if request.user.is_authenticated:
        if type:
            bank_datas = BankXlsx.objects.filter(bank_type=type)
        if bank:
            bank_info = BankXlsx.objects.get(id=bank)
        else:
            bank_info = []
        if request.method == 'POST':
            name = request.POST.get('name')
            num = request.POST.get('num')
            score = request.POST.get('score')
            starttime = request.POST.get('starttime')
            endtime = request.POST.get('endtime')
            times = request.POST.get('times')
            ruleText = request.POST.get('ruleText', '')
            name_exists = Game.objects.filter(game_name=name)
            if type and bank:
                if name and num and score and starttime and endtime and times:
                    if not name_exists:
                        if int(num) <= bank_info.bank_nums:
                            g = Game(game_name=name, game_nums=num, game_score=score, create_time=starttime, end_time=endtime,
                                     time_bar=times, game_rule=ruleText, class_game_id=Classify.objects.get(class_name=type).id,
                                     bank_game_id=bank_info.id)
                            g.save()
                            bank_info.bank_bs += 1
                            bank_info.save()
                            return redirect('/detail/{}'.format(type))
                        else:
                            con = '数量超出所属题库的题数!'
                    else:
                        con = '该考试名已存在!'
                else:
                    con = '配置信息输入有误!'
            else:
                con = '请选择题库!'
        return render(request, 'setgames/game.html',
                      {'class_datas': class_datas, 'bank_datas': bank_datas, 'type_date': type, 'bank': bank,
                       'bank_info': bank_info, 'con': con})
    else:
        return render(request, 'login.html')


# 考试信息
def test_info(request, id):
    if request.user.is_authenticated:
        game_info = Game.objects.get(id=id)
        exists = GameInfo.objects.filter(ginfo_user_id=request.user.id,ginfo_game_id=game_info.id)
        return render(request, 'competition/index.html', {'game_info': game_info,'exists':exists})
    else:
        return render(request, 'login.html')


starttime1 = []
suiji_list = []
# 开始考试
def test_start(request, id):
    import datetime
    starttime2 = datetime.datetime.now()
    starttime1.append(starttime2)

    num = 0
    data_list = []
    test_data = Game.objects.get(id=id)
    times = test_data.time_bar - 1
    bank_data = test_data.bank_game
    choi_data = Ques_choice.objects.filter(choi_id=bank_data.id).all()
    chois_data = Ques_choices.objects.filter(chois_id=bank_data.id)
    judge_data = Ques_judge.objects.filter(judge_id=bank_data.id)
    gap_data = Ques_gap.objects.filter(gap_id=bank_data.id)
    for data1 in choi_data:
        num += 1
        data_list.append(data1)
    for data2 in chois_data:
        num += 1
        data_list.append(data2)
    for data3 in judge_data:
        num += 1
        data_list.append(data3)
    for data4 in gap_data:
        num += 1
        data_list.append(data4)

    data_list = random.sample(data_list, test_data.game_nums)
    suiji_list.append(data_list)
    if request.user.is_authenticated:
        if request.method == 'POST':
            my_score = 0
            endtime = datetime.datetime.now()
            my_time = endtime - starttime1[0]
            starttime1.clear()
            yes = 0
            for i, data in zip(range(num), suiji_list[0]):
                j = i + 1
                name = request.POST.getlist('{}'.format(j),[])
                if not name:
                    name = ['空']
                print(name)
                if data.ques_type == '多选题':
                    if name == list(data.answer):
                        yes += 1
                        my_score += data.score
                else:
                    if name[0] == data.answer:
                        yes += 1
                        my_score += data.score
            print(my_score)
            suiji_list.clear()

            # 做记录
            user = UserProfile.objects.get(id=request.user.id)
            no = test_data.game_nums - yes
            jilu = GameInfo(total=my_score, times=my_time, yes=yes, no=int(no), ginfo_game_id=test_data.id,
                            ginfo_user_id=user.id)
            jilu.save()
            # 参与考试人数
            person_nums = BankXlsx.objects.get(id=int(test_data.bank_game_id))
            person_nums.bank_person += 1
            person_nums.save()
            return redirect('set:result', user.id, test_data.id)

        return render(request, 'competition/game.html', {
            'test_data': test_data, 'bank_data': suiji_list[0],
            'times': json.dumps(times), 'leng': json.dumps(len(suiji_list[0]))
        })
    else:
        return render(request, 'login.html')


# 考试结果
def result(request, uid, gid):
    count = 0
    user = UserProfile.objects.get(id=uid)
    userinfo = GameInfo.objects.filter(ginfo_user_id=uid, ginfo_game_id=gid)[0]
    rank = GameInfo.objects.order_by('-total')
    rank = GameInfo.objects.filter(ginfo_game_id=gid).order_by('-total')
    for i in rank:
        count += 1
        if request.user.is_authenticated:
            if i.id == userinfo.id:
                print(count)

                return render(request, 'competition/result.html', {'user': user, 'userinfo': userinfo, 'count': count})
        else:
            return render(request, 'login.html')


# 成绩排行
def rank(request):
    game = request.GET.get('test')
    if request.user.is_authenticated:
        if not game:
            order = GameInfo.objects.order_by('-total')
        else:
            game_deatil = Game.objects.get(game_name=game)
            order = GameInfo.objects.filter(ginfo_game_id=game_deatil.id).order_by('-total')
        good = GameInfo.objects.filter(ginfo_user_id=request.user.id).order_by('-total')
        return render(request, 'competition/rank.html', {'game': game, 'order': order, 'good': good})
    else:
        return render(request, 'login.html')
