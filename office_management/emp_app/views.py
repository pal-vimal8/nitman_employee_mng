from django.shortcuts import redirect, render,HttpResponse,get_object_or_404
from .models import *
from datetime import datetime
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps':emps
    }
    print(context)
    return render(request, 'all_emp.html', context)


def add_emp(request):
    if request.method == 'POST':
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        phone = request.POST.get('phone')
        dept_id = int(request.POST.get('department'))
        role_id = int(request.POST.get('role'))
        dept = get_object_or_404(Department, pk=dept_id)
        role = get_object_or_404(Role, pk=role_id)

        try: 
            new_emp = Employee(first_name=first_name,last_name=last_name, salary=salary,bonus=bonus,phone=phone,dept=dept,role=role,hire_date=datetime.now())
            new_emp.save()
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}')
        # return render(request, 'all_emp.html')
        # return HttpResponse('employee added successfully')
        return redirect('all_emp')
    
    elif request.method == 'GET':
        departs = Department.objects.all()
        roles = Role.objects.all()
        context = {
            'departs':departs,
        'roles':roles
        }
        return render(request, 'add_emp.html',context)
    else:
        return HttpResponse('An error exception')


def remove_emp(request,emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            # return HttpResponse('employee removed successfully')
            return redirect('all_emp')
        except:
            return HttpResponse('Please Enter a valid emp id')
    emps = Employee.objects.all()
    context = {
        'emps':emps
    }
    # return HttpResponse(request, context)
    return render(request, 'remove_emp.html',context)


def filter_emp(request):
    print(request.method)
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('first_name')
        dept = request.POST.get('department')
        role = request.POST.get('role')

        if name:
            emps = Employee.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = Employee.objects.filter(dept__name__icontains=dept)
        if role:
            emps = Employee.objects.filter(role__name__icontains=role)

        context = {
            'emps':emps
        }
        return render(request, 'all_emp.html',context)
    
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An exception occured')

def edit_emp(request, emp_id):
    emp = get_object_or_404(Employee, pk=emp_id)
    departs = Department.objects.all()
    roles = Role.objects.all()
    print(roles)
    if request.method == 'POST':
        emp.first_name = request.POST.get('first_name')
        emp.last_name = request.POST.get('last_name')
        emp.salary = request.POST.get('salary')
        emp.bonus = request.POST.get('bonus')
        emp.phone = request.POST.get('phone')
        emp.dept_id = int(request.POST.get('department'))
        emp.role_id = int(request.POST.get('role'))
        # emp.role_id = int(request.POST.get('role'))
        # emp.dept = get_object_or_404(Department, pk=dept_id)
        # emp.dept = get_object_or_404(Department)
       
        # emp.role = get_object_or_404(Role, pk=role_id)
        emp.save()

        return redirect('all_emp')

    elif request.method == 'GET':
        return render(request, 'edit_emp.html', {'emp': emp,'departs':departs,'roles':roles})

    else:
        return HttpResponse('An error occurred while editing the data')
