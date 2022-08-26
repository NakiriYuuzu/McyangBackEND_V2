import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE, \
    HTTP_500_INTERNAL_SERVER_ERROR

from .models import *


# TODO:Create your views here[tableName->Function].

# TODO:Create your Api Here[tableName->Function].

@csrf_exempt  # TODO: 登入驗證
def student_login(request):
    email = request.POST.get('S_email')
    password = request.POST.get('S_password')
    print(email, password)
    data = {}

    if request.method == 'GET':
        status = HTTP_404_NOT_FOUND

    else:
        if McyangStudent.objects.filter(S_email=email, S_password=password).exists():
            data['S_id'] = McyangStudent.objects.get(S_email=email, S_password=password).S_id
            data['S_name'] = McyangStudent.objects.get(S_email=email, S_password=password).S_name
            status = HTTP_200_OK

        else:
            status = HTTP_400_BAD_REQUEST

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt  # TODO: 課程列表
def course_list(request):
    s_id = request.POST.get('S_id')
    data = []

    if request.method == 'GET':
        status = HTTP_500_INTERNAL_SERVER_ERROR

    else:
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

        else:
            status = HTTP_404_NOT_FOUND

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
                                     'where s.Sign_id = %s', [sign_id])
        status = HTTP_200_OK
        for result in raw:
            data.append({'T_name': result.T_name, 'C_name': result.C_name, 'Sign_id': result.Sign_id})
    else:
        raw = McyangSign.objects.raw('select s.Sign_id, c.C_name, t.T_name from mc_sign s '
                                     'left join mc_course c on s.C_id_id = c.C_id '
                                     'left join mc_teacher t on c.T_id_id = t.T_id ')
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
    in_course_list = []

    if request.method == 'POST':
        if s_id and sign_id:
            in_course = McyangCourseRecord.objects.raw('select cr.* from mc_courserecord cr '
                                                       'left join mc_student s on s.S_id = cr.S_id_id '
                                                       'left join mc_course c on c.C_id = cr.C_id_id '
                                                       'left join mc_sign sign on sign.C_id_id = c.C_id '
                                                       'where cr.S_id_id = %s and sign.Sign_id = %s ', [s_id, sign_id])
            for result in in_course:
                in_course_list.append(result.C_id)
                print(result.C_id)

            if len(in_course_list) == 0:
                status = HTTP_406_NOT_ACCEPTABLE  # [406]不是此課堂的學生
            else:
                if McyangSignRecord.objects.filter(Sign_id=sign_id, S_id=s_id).exists():
                    status = HTTP_400_BAD_REQUEST  # [400]已簽到過
                else:
                    status = HTTP_200_OK  # [200]簽到成功！
                    do_insert = McyangSignRecord.objects.create(Sign_id=sign_id, S_id=s_id, crtTime=datetime.datetime.now())
                    do_insert.save()
        else:
            status = HTTP_404_NOT_FOUND  # [404]沒資料

    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR  # [500]不是POST的情況

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


# TODO: ====== 老師端 ======
@csrf_exempt  # TODO: 登入驗證
def teacher_login(request):
    email = request.POST.get('T_email')
    password = request.POST.get('T_password')
    print(email, password)
    data = {}

    if request.method == 'GET':
        status = HTTP_500_INTERNAL_SERVER_ERROR

    else:
        if McyangTeacher.objects.filter(T_email=email, T_password=password).exists():
            data['T_id'] = McyangTeacher.objects.get(T_email=email, T_password=password).T_id
            data['T_name'] = McyangTeacher.objects.get(T_email=email, T_password=password).T_name
            status = HTTP_200_OK

        else:
            status = HTTP_400_BAD_REQUEST

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt
def course_create(request):
    c_name = request.POST.get("C_name")
    t_id = request.POST.get("T_id")
    data = []

    if request.method == 'GET':
        status = HTTP_500_INTERNAL_SERVER_ERROR
    else:
        if c_name and t_id:
            status = HTTP_200_OK
        else:
            status = HTTP_404_NOT_FOUND

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)
