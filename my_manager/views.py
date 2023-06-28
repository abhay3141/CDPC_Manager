from django.shortcuts import render,redirect
from .models import *
from .forms import *
from .filter import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from . decorators import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

# Create your views here.

@is_user_auth
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect :(')
    context = {}
    return render(request, 'my_manager/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')  


#Non Core id = 1
#Core id = 2
#SDE id =  3

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator','Managers (DPC)'])
def manager(request):
    group = request.user.groups.all()[0].name
    managers = Manager.objects.all()
    mydict = {}
    for manager in managers:
        companies = manager.company_set.all()
        mydict[manager] = companies
    context = {'managers':managers,'mydict':mydict,'group':group}
    return render(request,'my_manager/manager.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def add_manager(request):
    group = request.user.groups.all()[0].name
    form = CreateUserForm()
    form1  = CreateManagerForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form1 = CreateManagerForm(request.POST)
        pw1 = form.data.get('password1')
        pw2 = form.data.get('password2')
        email = form.data.get('username')
        try:
            validate_email(email)
        except ValidationError:
            form.add_error('username', 'Invalid Email')
        if pw1!=pw2:
            form.add_error('password1', 'Passwords Do Not Match')
            context = {'form': form, 'form1': form1, 'group': group}
            return render(request, 'my_manager/add_manager.html', context)
        try:
            validate_password(pw1)
        except ValidationError as password_error:
            form.add_error('password1', password_error)
            context = {'form': form, 'form1': form1, 'group': group}
            return render(request, 'my_manager/add_manager.html', context)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if authenticate(username=username, password=password) is None:
                group1 = Group.objects.get(name = 'Managers (DPC)')
                Manager.objects.create(
                    my_user = user,name = form1.cleaned_data.get('name'),
                    phone = form1.cleaned_data.get('phone'),
                )
                user.groups.add(group1)    
                return redirect('home')    
    context = {'form':form,'form1':form1,'group':group}
    return render(request,'my_manager/add_manager.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def manager_detail(request,pk_test3):
    group = request.user.groups.all()[0].name
    my_user1 = User.objects.get(username = pk_test3)
    manager = Manager.objects.get(my_user=my_user1)
    companies = manager.company_set.all()
    context = {'manager':manager,'companies':companies,'group':group}
    return render(request,'my_manager/manager_detail.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def manager_update(request,pk_test3):
    group = request.user.groups.all()[0].name
    my_user1 = User.objects.get(username = pk_test3)
    manager = Manager.objects.get(my_user = my_user1)
    form1 = CreateManagerForm(instance=manager)
    form = UpdateUserForm(instance = my_user1)

    if request.method == 'POST':
        form1 = CreateManagerForm(request.POST, instance=manager)
        form = UpdateUserForm(request.POST, instance=my_user1)
        email = form.data.get('username')
        try:
            validate_email(email)
        except ValidationError:
            form.add_error('username', 'Invalid Email')
        if  form1.is_valid() and form.is_valid():
            form1.save()
            form.save()
            return redirect('home')
    
    context = {'form1':form1,'group':group,'form':form}
    return render(request,'my_manager/update_manager.html',context)


@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def update_hpc(request,pk_test3):
    group = request.user.groups.all()[0].name
    my_user1 = User.objects.get(username = pk_test3)
    hpc = headplacementcoordinator.objects.get(my_user = my_user1)
    form1 = CreateHpc(instance=hpc)
    form = UpdateUserForm(instance = my_user1)

    if request.method == 'POST':
        form1 = CreateHpc(request.POST, instance=hpc)
        form = UpdateUserForm(request.POST, instance=my_user1)
        email = form.data.get('username')
        try:
            validate_email(email)
        except ValidationError:
            form.add_error('username', 'Invalid Email')
        if  form1.is_valid() and form.is_valid():
            form1.save()
            form.save()
            return redirect('home')
    
    context = {'form1':form1,'group':group,'form':form}
    return render(request,'my_manager/update_hpc.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def hpc_delete(request,pk_test3):
    group = request.user.groups.all()[0].name
    my_user1 = User.objects.get(username = pk_test3)
    hpc = headplacementcoordinator.objects.get(my_user=my_user1)
    if request.method == 'POST':
        my_user1.delete()
        return redirect('home')
    
    context = {'hpc':hpc,'group':group}
    return render(request,'my_manager/delete_hpc.html',context)


@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def manager_delete(request,pk_test4):
    group = request.user.groups.all()[0].name
    my_user1 = User.objects.get(username = pk_test4)
    manager = Manager.objects.get(my_user=my_user1)
    if request.method == 'POST':
        my_user1.delete()
        return redirect('home')
    
    context = {'manager':manager,'group':group}
    return render(request,'my_manager/delete_manager.html',context)


@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def hpc(request):
    group = request.user.groups.all()[0].name
    context = {'group':group}
    return render(request,'my_manager/hpc.html',context)

@login_required(login_url='login')
@is_user_admin
def home(request):
    group = request.user.groups.all()[0].name
    core_companies = Company.objects.filter(Role_offered = 2).count()
    non_core_companies = Company.objects.filter(Role_offered = 1).count()
    sde_companies = Company.objects.filter(Role_offered = 3).count()
    coordinators = Coordinator.objects.all()
    companies = Company.objects.all() 

    context = {'group':group,'companies':companies,'companies':companies,'core_companies' :core_companies,'non_core_companies' :non_core_companies,'sde_companies' :sde_companies,'coordinators' :coordinators}
    
    return render(request,'my_manager/dashboard.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Managers (DPC)'])
def  manager_user(request):
    group = request.user.groups.all()[0].name
    companies = request.user.manager.company_set.all()
    name = request.user.manager.name
    roles = role.objects.all()
    core_companies = 0
    non_core_companies = 0
    sde_companies = 0
    for company in companies:
            index = 0
            for role1 in roles:
                for role2 in company.Role_offered.all():
                    if(index==0 and role2==role1):
                        non_core_companies = non_core_companies+1
                    if(index==1 and role2==role1):
                        core_companies = core_companies+1
                    if(index==2 and role2==role1):
                        sde_companies = sde_companies+1
                        print('hi')
                index = index+1
 
    context = {'group':group,'companies':companies,'name':name,'core_companies':core_companies,'non_core_companies':non_core_companies,'sde_companies':sde_companies}
    return render(request,'my_manager/manager_user.html',context)


@login_required(login_url='login')
@is_user_allow(allowed_roles=['Student Coordinator'])
def user_page(request):
    group = request.user.groups.all()[0].name
    companies = request.user.coordinator.company_set.all()
    name = request.user.coordinator.name
    roles = role.objects.all()
    print(companies)
    core_companies = 0
    non_core_companies = 0
    sde_companies = 0
    for company in companies:
            index = 0
            for role1 in roles:
                for role2 in company.Role_offered.all():
                    if(index==0 and role2==role1):
                        non_core_companies = non_core_companies+1
                    if(index==1 and role2==role1):
                        core_companies = core_companies+1
                    if(index==2 and role2==role1):
                        sde_companies = sde_companies+1
                index = index+1
 
    context = {'group':group,'companies':companies,'name':name,'core_companies':core_companies,'non_core_companies':non_core_companies,'sde_companies':sde_companies}
    return render(request,'my_manager/user.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Managers (DPC)','Head Placement Coordinator'])
def coordinators(request,pk):
    group = request.user.groups.all()[0].name
    my_user1 = User.objects.get(username = pk)
    coordinator = Coordinator.objects.get(my_user=my_user1)
    companies = coordinator.company_set.all()
    tot_comp = companies.count()

    context = {'group':group,'coordinator': coordinator , 'companies':companies,'tot_comp':tot_comp}

    return render(request,'my_manager/coordinators.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator','Managers (DPC)'])
def assign_company(request,pk):
    my_user1 = User.objects.get(username = pk)
    coordinator = Coordinator.objects.get(my_user= my_user1)
    group = request.user.groups.all()[0].name
    companies = Company.objects.all()
    name = coordinator.name
    if request.method == 'POST':
        selected_companies_ids = request.POST.getlist('companies')
        for selected_company in selected_companies_ids:
            company = Company.objects.get(id = selected_company)
            company.Spoc = coordinator
            company.save()
        return redirect('home')
    context = {'companies':companies,'group':group,'name':name}
    return render(request,'my_manager/assign_companies.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def add_coordinator(request):
    group = request.user.groups.all()[0].name
    form = CreateUserForm()
    form1  = CreateCoordinatorForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form1 = CreateCoordinatorForm(request.POST)
        pw1 = form.data.get('password1')
        pw2 = form.data.get('password2')
        email = form.data.get('username')
        try:
            validate_email(email)
        except ValidationError:
            form.add_error('username', 'Invalid Email')
        if pw1!=pw2:
            form.add_error('password1', 'Passwords Do Not Match')
            context = {'form': form, 'form1': form1, 'group': group}
            return render(request, 'my_manager/add_coordinator.html', context)
        try:
            validate_password(pw1)
        except ValidationError as password_error:
            form.add_error('password1', password_error)
            context = {'form': form, 'form1': form1, 'group': group}
            return render(request, 'my_manager/add_coordinator.html', context)

        if form.is_valid() and form1.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if authenticate(username=username, password=password) is None:
                group1 = Group.objects.get(name = 'Student Coordinator')
                Coordinator.objects.create(
                    my_user = user,name = form1.cleaned_data.get('name'),
                    phone = form1.cleaned_data.get('phone'),
                )
                user.groups.add(group1)    
                return redirect('home') 
            
    context = {'form':form,'form1':form1,'group':group}
    return render(request,'my_manager/add_coordinator.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator','Managers (DPC)'])
def assign_company_manager(request,pk):
    my_user1 = User.objects.get(username = pk)
    manager = Manager.objects.get(my_user= my_user1)
    group = request.user.groups.all()[0].name
    companies = Company.objects.all()
    name = manager.name
    if request.method == 'POST':
        selected_companies_ids = request.POST.getlist('companies')
        for selected_company in selected_companies_ids:
            company = Company.objects.get(id = selected_company)
            company.Manager = manager
            company.save()
        return redirect('home')
    context = {'companies':companies,'group':group,'name':name}
    return render(request,'my_manager/assign_companies.html',context)


@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Managers (DPC)','Head Placement Coordinator'])
def companies(request):
    companies = Company.objects.all()
    group = request.user.groups.all()[0].name
    myFilter = CompanyFilter(request.GET, queryset=companies)
    companies = myFilter.qs
    context = {'companies':companies,'myFilter':myFilter,'group':group}
    return render(request,'my_manager/companies.html',context)


@login_required(login_url='login')
def company_detail(request,pk):
    group = request.user.groups.all()[0].name
    company = Company.objects.get(name = pk)
    comments = company.commentsection_set.all()
    if request.method=='POST':
        comment_text = request.POST.get('comment')
        CommentSection.objects.create(
            comment = comment_text,company = company,author = request.user
        )
        if group == 'Student Coordinator':
            return redirect('user_page')
        return redirect('companies')
    context = {'company':company,'comments':comments,'group':group}
    return render(request,'my_manager/company_detail.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def hpcs(request):
    group = request.user.groups.all()[0].name
    hpcs = headplacementcoordinator.objects.all()
    context = {'hpcs':hpcs,'group':group}
    return render(request,'my_manager/hpc.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def add_hpc(request):
    group = request.user.groups.all()[0].name
    form1 = CreateHpc()
    form = CreateUserForm()
    if request.method == 'POST':
        form1 = CreateHpc(request.POST)
        form = CreateUserForm(request.POST)
        pw1 = form.data.get('password1')
        pw2 = form.data.get('password2')
        email = form.data.get('username')
        try:
            validate_email(email)
        except ValidationError:
            form.add_error('username', 'Invalid Email')
        if pw1!=pw2:
            form.add_error('password1', 'Passwords Do Not Match')
            context = {'form': form, 'form1': form1, 'group': group}
            return render(request, 'my_manager/create_hpc.html', context)
        try:
            validate_password(pw1)
        except ValidationError as password_error:
            form.add_error('password1', password_error)
            context = {'form': form, 'form1': form1, 'group': group}
            return render(request, 'my_manager/create_hpc.html', context)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if authenticate(username=username, password=password) is None:
                group1 = Group.objects.get(name = 'Head Placement Coordinator')
                headplacementcoordinator.objects.create(
                    my_user = user,name = form1.cleaned_data.get('name'),
                    phone = form1.cleaned_data.get('phone'),
                )
                user.groups.add(group1)    
                return redirect('home')
    context = {'form1':form1,'form':form,'group':group}
    return render(request,'my_manager/create_hpc.html',context)


@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Managers (DPC)','Head Placement Coordinator'])
def add_company(request):
    group = request.user.groups.all()[0].name
    form = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    message1 = 'Add Company'
    message2 = 'Add the company!'
    context = {'form':form,'message1':message1,'message2':message2,'group':group}
    return render(request,'my_manager/add_company.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Managers (DPC)','Head Placement Coordinator'])
def update_company(request,pk_test):
    company = Company.objects.get(name = pk_test)
    form  = CompanyForm(instance=company)
    group = request.user.groups.all()[0].name
    print(group)

    if request.method == 'POST':
        form = CompanyForm(request.POST , instance = company)
        if form.is_valid():
            form.save()
            return redirect('home')

    message1 = 'Update Data of the Company'
    message2 = 'Update the information'
    context = {'form':form,'message1':message1,'message2':message2,'group':group}
    return render(request,'my_manager/add_company.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Student Coordinator'])
def update_company_user(request,pk_test2):
    group = request.user.groups.all()[0].name
    company = Company.objects.get(name = pk_test2)
    form = CompanyUserForm(instance=company)
    
    if request.method == 'POST':
        form = CompanyUserForm(request.POST , instance = company)
        if form.is_valid():
            form.save()
            return redirect('user_page')

    message1 = 'Update Data of the Company'
    message2 = 'Update the information'
    context = {'form':form,'message1':message1,'message2':message2,'group':group}
    return render(request,'my_manager/user_update_company.html',context)



@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Managers (DPC)','Head Placement Coordinator'])
def delete_company(request,pk_test1):
    group = request.user.groups.all()[0].name
    company = Company.objects.get(name = pk_test1)
    if request.method =='POST':
        company.delete()
        return redirect('home')
    context = {'item':company,'group':group}
    return render(request,'my_manager/delete.html',context)

@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def update_coordinator(request, pk_test2):
    group = request.user.groups.all()[0].name
    my_user1 = User.objects.get(username = pk_test2)
    coordinator = Coordinator.objects.get(my_user = my_user1)
    form1 = CreateCoordinatorForm(instance=coordinator)
    form = UpdateUserForm(instance = coordinator.my_user)

    if request.method == 'POST':
        form1 = CreateCoordinatorForm(request.POST, instance=coordinator)
        form = UpdateUserForm(request.POST, instance=coordinator.my_user)
        email = form.data.get('username')
        try:
            validate_email(email)
        except ValidationError:
            form.add_error('username', 'Invalid Email')
        if  form1.is_valid() and form.is_valid():
            form.save()
            form1.save()
            return redirect('home')

    context = { 'form1': form1,'group':group,'form':form}
    return render(request, 'my_manager/update_coordinator.html', context)


@login_required(login_url='login')
@is_user_allow(allowed_roles=['Super User','Head Placement Coordinator'])
def delete_coordinator(request, pk_test3):
    group = request.user.groups.all()[0].name
    my_user1 = User.objects.get(username = pk_test3)
    coordinators = Coordinator.objects.get(my_user = my_user1)
    my_user1 = coordinators.my_user
    if request.method == 'POST':
        my_user1.delete()
        return redirect('home')
    context = {'item':coordinators,'group':group}
    return render(request, 'my_manager/delete_coordinator.html',context)
