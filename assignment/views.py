from django.shortcuts import render, redirect
from .forms import AssignmentForm, AttachmentFormSet
from django.views.generic import ListView
from .models import Assignment




class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignment/assignment_list.html'  # Define your template path
    context_object_name = 'assignments'

def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save()
            formset = AttachmentFormSet(request.POST, request.FILES, instance=assignment)
            if formset.is_valid():
                formset.save()
                return redirect('dashboard')
    else:
        form = AssignmentForm()
        formset = AttachmentFormSet()
    return render(request, 'assignment/create.html', {'form': form, 'formset': formset})
