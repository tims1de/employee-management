from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Employee
from .permissions import CanAccessEmployeeAPI
from .serializer import EmployeeSerializer


@api_view(['GET'])
@permission_classes([CanAccessEmployeeAPI])
def get_all_employees_info(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([CanAccessEmployeeAPI])
def get_employees_by_similar_level(request):
    level = request.GET.get('level')

    employees = Employee.objects.filter(Q(level=int(level)))
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)