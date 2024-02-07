from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import UserProfile
from coursework.models import Course
from .forms import AssignmentForm, AttachmentFormSet, FeedbackForm, GradeForm
from django.views.generic import ListView
from .models import Assignment, Attachment
from django.http import FileResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Assignment, Submission
from .forms import SubmissionForm
from .forms import GradeSubmissionForm
from .models import Submission
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
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


@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Check if the student has already submitted the assignment
    submission = Submission.objects.filter(assignment=assignment, student=request.user).first()

    is_already_submitted = submission is not None

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
            return redirect(reverse('assignment_view', kwargs={'assignment_id': assignment.id}))
    else:
        form = SubmissionForm()

    return render(request, 'assignment/view_assignment.html', {'assignment': assignment, 'form': form, 'is_already_submitted': is_already_submitted})

def create_assignment(request, course_id):
    # Fetch the course instance using the course_id
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, initial={'course': course_id})
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course  # Directly assign the course instance
            assignment.save()

            formset = AttachmentFormSet(request.POST, request.FILES, instance=assignment)
            if formset.is_valid():
                formset.save()
                return redirect(f'{reverse("view_course", args=[course.id])}?tab=assignments')
    else:
        form = AssignmentForm(initial={'course': course_id})
        formset = AttachmentFormSet(instance=Assignment())

    # Include the course name in the context
    return render(request, 'assignment/create.html', {'form': form, 'formset': formset, 'course_name': course.title,'course_id':course_id})

def get_assignment_linked_course_id(request, assignment_id):
    try:
        assignment = Assignment.objects.get(pk=assignment_id)
        course_id = assignment.linked_course.id  # Accessing via the field name
        return JsonResponse({'course_id': course_id})
    except Assignment.DoesNotExist:
        raise Http404("Assignment does not exist")
    
@login_required
def view_assignment(request, assignment_id):
    form = FeedbackForm()
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Fetch the user's profile
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check if the user is an instructor
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR

    # Fetch submissions for the specified assignment
    submissions = Submission.objects.filter(assignment=assignment).select_related('student')

    # Check if the student has already submitted the assignment
    if not is_instructor:
        submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
        feedbacks = submission.feedbacks.all() if submission else []
        is_already_submitted = submission is not None
        
    else:
        feedbacks = []
        is_already_submitted = False

    return render(request, 'assignment/view_assignment.html', {
        'assignment': assignment,
        'is_already_submitted': is_already_submitted,
        'is_instructor': is_instructor,
        'submissions': submissions,
        'form': form,
        'feedbacks': feedbacks,  # Pass feedbacks to the template
    })



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


class CourseGradesView(LoginRequiredMixin, ListView):
    model = Submission 
    template_name = 'assignment/course_grades.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        # Get the course_id from the URL parameters
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        # Filter submissions/grades by the course
        return Submission.objects.filter(assignment__course=course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return context



def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    assignment = submission.assignment

    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            url = reverse('assignment_view', args=[submission.assignment.id]) + "?tab=section2"
            return redirect(url)
    else:
        form = GradeSubmissionForm(instance=submission)
    
    return render(request, 'assignment/grade_submission.html', {'form': form, 'submission': submission, 'assignment': assignment})
    
@login_required
def add_feedback(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    assignment = submission.assignment
    assignment_id = submission.assignment.id
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.submission = submission
            feedback.author = request.user
            feedback.save()
            url = reverse('assignment_view', args=[assignment_id]) + "?tab=section2"
            return redirect(url)
    else:
        form = FeedbackForm()
    return render(request, 'assignment/add_feedback.html', {'form': form, 'submission': submission, 'assignment': assignment})