from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from .utils import get_stats, paginate_projects, search_projects, valuate_projects


def projects(request):
    projects, keywords, beds, baths, min_price, max_price, valuation = search_projects(request)
    projects_per_page = 25
    custom_range, projects = paginate_projects(request, projects, projects_per_page)
    minimum_price, maximum_price, overall_avg_price, overall_price_sqf, \
        most_common_districts, most_common_nhoods, n_undervalued, n_overvalued, \
        val_options = get_stats()

    context = {'projects': projects, 'keywords': keywords, 'beds': beds, 'baths': baths,
    'min_price': min_price, 'max_price': max_price, 'val_options': val_options, 
    'custom_range': custom_range, 'overall_avg_price': overall_avg_price, 
    'overall_price_sqf': overall_price_sqf, 'most_common_districts': most_common_districts, 
    'most_common_nhoods': most_common_nhoods, 'n_undervalued': n_undervalued, 
    'n_overvalued': n_overvalued}

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    price_diff, val_price, avg_price_sqf, avg_price = valuate_projects(project)

    context = {'project': project, 'val_price': val_price, \
        'price_diff': price_diff, 'avg_price': avg_price, 'avg_price_sqf': avg_price_sqf}

    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def add_project(request):
    profile = request.user
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    project = Project.objects.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {'object': project}
    return render(request, 'projects/delete-project.html', context)