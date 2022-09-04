import datetime

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_417_EXPECTATION_FAILED

from .models import *


# TODO:Create your views here[tableName->Function].

# TODO:Create your Api Here[tableName->Function].

@csrf_exempt  # TODO: 登入驗證
def login(request):
    s_email = request.POST.get('S_email')
    s_password = request.POST.get('S_password')
    t_email = request.POST.get('T_email')
    t_password = request.POST.get('T_password')
    print(s_email, s_password, t_email, t_password)
    data = {}

    if request.method == 'POST':
        if s_email and s_password:
            status = HTTP_200_OK
            if McyangStudent.objects.filter(S_email=s_email, S_password=s_password).exists():
                data['S_id'] = McyangStudent.objects.get(S_email=s_email, S_password=s_password).S_id
                data['S_name'] = McyangStudent.objects.get(S_email=s_email, S_password=s_password).S_name

            else:
                status = HTTP_400_BAD_REQUEST

        elif t_email and t_password:
            status = HTTP_200_OK
            if McyangTeacher.objects.filter(T_email=t_email, T_password=t_password).exists():
                data['T_id'] = McyangTeacher.objects.get(T_email=t_email, T_password=t_password).T_id
                data['T_name'] = McyangTeacher.objects.get(T_email=t_email, T_password=t_password).T_name

            else:
                status = HTTP_400_BAD_REQUEST
        else:
            status = HTTP_404_NOT_FOUND

    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt  # TODO: 課程列表
def course_list(request):
    s_id = request.POST.get('S_id')
    t_id = request.POST.get('T_id')
    print(s_id, t_id)
    data = []

    if request.method == 'POST':
        if s_id:
            raw = McyangCourse.objects.raw('select DISTINCT c.*, t.T_name from mc_course c '
                                           'left join mc_courserecord cr on cr.C_id_id = c.C_id '
                                           'left join mc_teacher t on c.T_id_id = t.T_id '
                                           'where cr.S_id_id = %s', [s_id])
            if len(raw) > 0:
                status = HTTP_200_OK
                for result in raw:
                    data.append({'C_id': result.C_id, 'C_name': result.C_name, 'T_name': result.T_name})
            else:
                status = HTTP_400_BAD_REQUEST

        elif t_id:
            raw = McyangCourse.objects.raw('select DISTINCT c.*, t.T_name from mc_course c '
                                           'left join mc_courserecord cr on cr.C_id_id = c.C_id '
                                           'left join mc_teacher t on c.T_id_id = t.T_id '
                                           'where c.T_id_id = %s', [t_id])
            if len(raw) > 0:
                status = HTTP_200_OK
                for result in raw:
                    data.append({'C_id': result.C_id, 'C_name': result.C_name, 'T_name': result.T_name})

            else:
                status = HTTP_400_BAD_REQUEST

        else:
            status = HTTP_404_NOT_FOUND

    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt
def course_sign_list(request):
    sign_id = request.GET.get('id', '')
    print(sign_id)
    data = []

    if sign_id:
        raw = McyangSign.objects.raw('select s.Sign_id, c.C_name, t.T_name from mc_sign s '
                                     'left join mc_course c on s.C_id_id = c.C_id '
                                     'left join mc_teacher t on c.T_id_id = t.T_id '
                                     'where s.Sign_id = %s order by s.Sign_id ', [sign_id])
        status = HTTP_200_OK
        for result in raw:
            data.append({'T_name': result.T_name, 'C_name': result.C_name, 'Sign_id': result.Sign_id})
    else:
        raw = McyangSign.objects.raw('select s.Sign_id, c.C_name, t.T_name from mc_sign s '
                                     'left join mc_course c on s.C_id_id = c.C_id '
                                     'left join mc_teacher t on c.T_id_id = t.T_id '
                                     'order by s.Sign_id ')
        status = HTTP_200_OK
        for result in raw:
            data.append({'T_name': result.T_name, 'C_name': result.C_name, 'Sign_id': result.Sign_id})

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt
def course_signup(request):
    s_id = request.POST.get('S_id')
    sign_id = request.POST.get('Sign_id')
    print(s_id, sign_id)

    data = {}

    if request.method == 'POST':
        if s_id and sign_id:
            in_course = McyangCourseRecord.objects.raw('select cr.* from mc_courserecord cr '
                                                       'left join mc_student s on s.S_id = cr.S_id_id '
                                                       'left join mc_course c on c.C_id = cr.C_id_id '
                                                       'left join mc_sign sign on sign.C_id_id = c.C_id '
                                                       'where cr.S_id_id = %s and sign.Sign_id = %s ', [s_id, sign_id])
            if len(in_course) == 0:
                status = HTTP_406_NOT_ACCEPTABLE  # [406]不是此課堂的學生
            else:
                if McyangSignRecord.objects.filter(Sign_id=sign_id, S_id=s_id).exists():
                    status = HTTP_400_BAD_REQUEST  # [400]已簽到過
                else:
                    status = HTTP_200_OK  # [200]簽到成功！
                    seq_no = McyangSignRecord.objects.filter().count() + 1
                    McyangSignRecord.objects.create(SR_id=seq_no, Sign_id_id=sign_id, S_id_id=s_id,
                                                    crtTime=datetime.datetime.now())

        else:
            status = HTTP_404_NOT_FOUND  # [404]沒資料

    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR  # [500]不是POST的情況

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt
def course_create(request):
    c_name = request.POST.get("C_name")
    t_id = request.POST.get("T_id")
    print(c_name, t_id)
    data = {}

    if request.method == 'POST':
        if c_name and t_id:
            status = HTTP_200_OK
            try:
                with transaction.atomic():
                    McyangCourse.objects.create(C_id=McyangCourse.objects.count() + 1, C_name=c_name, T_id_id=t_id,
                                                C_image="", crtTime=datetime.datetime.now())
            except:
                status = HTTP_417_EXPECTATION_FAILED
        else:
            status = HTTP_404_NOT_FOUND

    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt
def sign_create(request):
    c_name = request.POST.get("C_name")
    t_id = request.POST.get("T_id")
    print(c_name, t_id)
    data = {}
    datas = []

    if request.method == 'POST':
        if c_name and t_id:
            c_id = McyangCourse.objects.get(T_id_id=t_id, C_name=c_name).C_id
            print(c_id)
            if c_id:
                status = HTTP_200_OK
                try:
                    with transaction.atomic():
                        seq_no = McyangSign.objects.filter().count() + 1
                        test = McyangSign.objects.create(Sign_id=seq_no, C_id_id=c_id, crtTime=datetime.datetime.now())
                        raw = McyangStudent.objects.raw(
                            'select s.* from mc_student s left join mc_courserecord cr on cr.S_id_id = s.S_id where cr.C_id_id = %s',
                            [c_id])

                        sign_id = test.Sign_id
                        for result in raw:
                            datas.append({'S_id': result.S_id, 'StudentID': result.S_email, 'S_name': result.S_name})
                        data['Sign_id'] = sign_id
                        data['C_id'] = test.C_id_id
                        data['StudentList'] = datas
                except:
                    status = HTTP_417_EXPECTATION_FAILED

            else:
                status = HTTP_400_BAD_REQUEST
        else:
            status = HTTP_404_NOT_FOUND
    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt
def sign_record_list(request):
    sign_id = request.GET.get('Sign_id', '')
    data = []

    if request.method == 'GET':
        if sign_id:
            status = HTTP_200_OK
            raw = McyangStudent.objects.raw('select distinct s.* from mc_student s '
                                            'left join mc_signrecord sr on sr.S_id_id = s.S_id '
                                            'where sr.Sign_id_id = %s', [sign_id])
            for result in raw:
                data.append({'S_id': result.S_id, 'StudentID': result.S_email, 'S_name': result.S_name})

        else:
            status = HTTP_200_OK
            raw = McyangStudent.objects.raw('select distinct s.* from mc_student s '
                                            'left join mc_signrecord sr on sr.S_id_id = s.S_id')
            for result in raw:
                data.append({'S_id': result.S_id, 'StudentID': result.S_email, 'S_name': result.S_name})

    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt
def race_create(request):
    c_id = request.POST.get("C_id")
    race_doc = request.POST.get("Race_doc")
    race_id = request.POST.get("Race_id")
    stat = request.POST.get("Status")
    print(c_id, race_doc, race_id, stat)
    data = {}

    if request.method == 'POST':
        if c_id and race_doc and not race_id and not stat:
            try:
                with transaction.atomic():
                    status = HTTP_200_OK
                    # status = 0 表示開始中 1表示結束
                    seq_no = McyangRaceAnswer.objects.filter().count() + 1
                    race = McyangRaceAnswer.objects.create(R_id=seq_no, R_doc=race_doc, Status=0,
                                                           crtTime=datetime.datetime.now(), C_id_id=c_id)
                    data['Race_id'] = race.R_id
                    data['Race_doc'] = race.R_doc
                    data['Status'] = race.Status
                    data['CrtTime'] = race.crtTime
                    data['C_id'] = c_id

            except Exception as e:
                status = HTTP_417_EXPECTATION_FAILED
                print(e)
        elif stat and race_id and not c_id and not race_doc:
            try:
                with transaction.atomic():
                    status = HTTP_200_OK
                    McyangRaceAnswer.objects.filter(R_id=race_id).update(Status=stat)

            except Exception as e:
                status = HTTP_417_EXPECTATION_FAILED
                print(e)

        else:
            status = HTTP_400_BAD_REQUEST
    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt
def race_list_create(request):
    s_name = request.POST.get("S_name")
    r_id = request.POST.get("Race_id")
    answer = request.POST.get("Answer")
    print(s_name, r_id, answer)
    data = {}

    if request.method == 'POST':
        if s_name and r_id and not answer:
            current = McyangRaceAnswer.objects.get(R_id=r_id)
            if current.Status == 0:
                try:
                    with transaction.atomic():
                        status = HTTP_200_OK
                        s_id = McyangStudent.objects.get(S_name=s_name).S_id
                        seq_no = McyangRaceList.objects.filter().count() + 1
                        create = McyangRaceList.objects.create(RL_id=seq_no, R_id_id=r_id, S_id_id=s_id,
                                                               crtTime=datetime.datetime.now(), Answer="0")
                        data['RL_id'] = create.RL_id
                except Exception as e:
                    status = HTTP_417_EXPECTATION_FAILED
                    print(e)
            else:
                status = HTTP_406_NOT_ACCEPTABLE
        elif s_name and r_id and answer:
            try:
                with transaction.atomic():
                    status = HTTP_200_OK
                    s_id = McyangStudent.objects.get(S_name=s_name).S_id
                    McyangRaceList.objects.filter(R_id_id=r_id, S_id_id=s_id).update(Answer=answer)
            except Exception as e:
                status = HTTP_417_EXPECTATION_FAILED
                print(e)
        else:
            status = HTTP_400_BAD_REQUEST
    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt
def race_list_list(request):
    race_id = request.GET.get('Race_id', '')
    data = []

    if request.method == 'GET':
        if race_id:
            status = HTTP_200_OK
            raw = McyangRaceList.objects.raw('select rl.*, s.S_name, s.S_email from mc_racelist rl '
                                             'left join mc_student s on s.S_id = rl.S_id_id '
                                             'where rl.R_id_id = %s order by rl.RL_id desc ', [race_id])
            for result in raw:
                data.append({'RL_id': result.RL_id, 'Answer': result.Answer, 'S_name': result.S_name,
                             'StudentID': result.S_email})
        else:
            status = HTTP_400_BAD_REQUEST
    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)
