from django.shortcuts import get_object_or_404, render, redirect
from coursework.models import Course
from .forms import AssignmentForm, AttachmentFormSet
from django.views.generic import ListView
from .models import Assignment, Attachment
from django.http import FileResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Assignment, Submission
from .forms import SubmissionForm
from django.urls import reverse

class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignment/assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        self.course_id = self.kwargs.get('course_id')
        if self.course_id is not None:
            course = get_object_or_404(Course, id=self.course_id)
            assignments = course.assignments.all()

            # Check if each assignment has been submitted by the current user
            for assignment in assignments:
                assignment.is_already_submitted = Submission.objects.filter(
                    assignment=assignment, student=self.request.user
                ).exists()

            return assignments
        else:
            return Assignment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_list'] = Course.objects.all()
        context['selected_course_id'] = self.course_id
        return context

# Rest of your views...

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Check if the student has already submitted the assignment
    submission = Submission.objects.filter(assignment=assignment, student=request.user).first()

    is_already_submitted = submission is not None  # True if submission exists, False otherwise

    if is_already_submitted:
        # If submission exists, assignment is already submitted for this student
        return render(request, 'assignment/view_assignment.html', {'assignment': assignment, 'is_already_submitted': is_already_submitted})

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()

            # Set the assignment's is_submitted field to True
            assignment.is_submitted = True
            assignment.save()

            # Redirect to a new URL:
            return redirect(reverse('view_course', kwargs={'course_id': assignment.course.id}))
    else:
        form = SubmissionForm()

    return render(request, 'assignment/view_assignment.html', {'assignment': assignment, 'form': form, 'is_already_submitted': is_already_submitted})

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

@login_required
def view_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Check if the student has already submitted the assignment
    submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    
    is_already_submitted = submission is not None  # True if submission exists, False otherwise
    
    return render(request, 'assignment/view_assignment.html', {'assignment': assignment, 'is_already_submitted': is_already_submitted})


def download_attachment(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)
    try:
        return FileResponse(attachment.file.open(), as_attachment=True, filename=attachment.file.name)
    except FileNotFoundError:
        raise Http404('File does not exist')
    
@login_required
def is_submitted(request, student_id, assignment_id):
    # Check if the assignment with the given ID exists
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Check if the student with the given ID has submitted the assignment
    submission = Submission.objects.filter(assignment=assignment, student_id=student_id).first()
    
    # Return a JSON response indicating whether the assignment is submitted or not
    data = {
        'is_submitted': submission is not None,
    }
    
    return JsonResponse(data)