from django.db import models
from apps.account.models import UserProfile
from datetime import datetime

# 考试分类
class Classify(models.Model):
    class_name = models.CharField(u'类型名',max_length=10)
    class_head = models.ImageField(u'类型头像',default='default_class.png')
    class_desc = models.TextField(u'类型描述')

    # meta信息，即后台栏目名
    class Meta:
        verbose_name = "考试分类"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.class_name

# 存储题库xlsx表
class BankXlsx(models.Model):
    bank_name = models.CharField(u'题库名称',max_length=20)
    bank_type = models.CharField(u'题库所属分类',max_length=10)
    bank_xlsx = models.CharField(u'上传文件名称',max_length=50)
    bank_nums = models.IntegerField(u'题库总数')
    bank_chio = models.IntegerField(u'单选题数')
    bank_chios = models.IntegerField(u'多选题数')
    bank_judge = models.IntegerField(u'判断题数')
    bank_gap = models.IntegerField(u'填空题数')
    bank_person = models.IntegerField(u'参与人数')
    bank_bs = models.IntegerField(u'已出考试')

    class Meta:
        verbose_name = "存储题库xlsx"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.bank_name

# 单选题表
class Ques_choice(models.Model):
    ques_type = models.CharField(u'题类型',default='单选题',max_length=5)
    question = models.TextField(u'单选题目')
    answer = models.TextField(u'答案')
    choiceA = models.TextField(u'选项A')
    choiceB = models.TextField(u'选项B')
    choiceC = models.TextField(u'选项C')
    choiceD = models.TextField(u'选项D')
    score = models.IntegerField(u'分值')
    choi_id = models.ForeignKey(BankXlsx,on_delete=models.CASCADE,verbose_name='关联题库表')

    class Meta:
        verbose_name = "单选题"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.question

# 多选题表
class Ques_choices(models.Model):
    ques_type = models.CharField(u'题类型',default='多选题',max_length=5)
    question = models.TextField(u'多选题目')
    answer = models.TextField(u'答案')
    choiceA = models.TextField(u'选项A')
    choiceB = models.TextField(u'选项B')
    choiceC = models.TextField(u'选项C')
    choiceD = models.TextField(u'选项D')
    score = models.IntegerField(u'分值')
    chois_id = models.ForeignKey(BankXlsx,on_delete=models.CASCADE,verbose_name='关联题库表')

    class Meta:
        verbose_name = "多选题"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.question

# 判断题
class Ques_judge(models.Model):
    ques_type = models.CharField(u'题类型',default='判断题',max_length=5)
    question = models.TextField(u'判断题目')
    answer = models.TextField(u'答案')
    score = models.IntegerField(u'分值')
    judge_id = models.ForeignKey(BankXlsx,on_delete=models.CASCADE,verbose_name='关联题库表')

    class Meta:
        verbose_name = "判断题"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.question

# 填空题
class Ques_gap(models.Model):
    ques_type = models.CharField(u'题类型',default='填空题',max_length=5)
    question = models.TextField(u'填空题目')
    answer = models.TextField(u'答案')
    score = models.IntegerField(u'分值')
    gap_id = models.ForeignKey(BankXlsx,on_delete=models.CASCADE,verbose_name='关联题库表')

    class Meta:
        verbose_name = "填空题"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.question


# 考试配置表
class Game(models.Model):
    game_name = models.CharField(u'考试名称',max_length=50)
    game_nums = models.IntegerField(u'出题数量')
    game_score = models.IntegerField(u'总分数')
    create_time = models.DateTimeField(u'开始时间',default=datetime.now)
    end_time = models.DateTimeField(u'结束时间')
    time_bar = models.IntegerField(u'答题时间限制')
    game_rule = models.TextField(u'考试规则')
    class_game = models.ForeignKey(Classify,on_delete=models.CASCADE,verbose_name='关联分类表')
    bank_game = models.ForeignKey(BankXlsx,on_delete=models.CASCADE,verbose_name='关联题库表')

    class Meta:
        verbose_name = "考试配置"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.game_name


# 考试记录表
class GameInfo(models.Model):
    total = models.IntegerField(u'得分')
    times = models.CharField(u'用时',max_length=20)
    ginfo_game = models.ForeignKey(Game,on_delete=models.CASCADE,verbose_name='关联考试配置表')
    ginfo_user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='关联用户表')

    class Meta:
        verbose_name = "考试记录"
        verbose_name_plural = verbose_name

























