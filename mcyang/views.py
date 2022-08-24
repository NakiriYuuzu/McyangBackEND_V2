from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from .models import *


# TODO:Create your views here[tableName->Function].

# TODO:Create your Api Here[tableName->Function].

@csrf_exempt  # TODO: 登入驗證
def student_login(request):
    email = request.POST.get('S_email')
    password = request.POST.get('S_password')
    print(email, password)
    data = {}
    status = HTTP_200_OK

    if request.method == 'GET':
        data['message'] = 'NoT allowed get method!'
        status = HTTP_404_NOT_FOUND

    else:
        if McyangStudent.objects.filter(S_email=email, S_password=password).exists():
            data['message'] = 'success'
            data['S_id'] = McyangStudent.objects.get(S_email=email, S_password=password).S_id
            data['S_name'] = McyangStudent.objects.get(S_email=email, S_password=password).S_name

        else:
            data['message'] = '帳號或密碼錯誤！'
            status = HTTP_400_BAD_REQUEST

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)


@csrf_exempt  # TODO: 課程列表
def course_list(request):
    s_id = request.POST.get('S_id')
    data = []

    if request.method == 'GET':
        data.append({'message': 'Not allowed get method!'})
        status = HTTP_404_NOT_FOUND

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
                status = HTTP_404_NOT_FOUND
                data.append({'message': '查無資料此資料！'})

        else:
            data.append({'message': '欄位資料空白或有誤！'})
            status = HTTP_400_BAD_REQUEST

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)
