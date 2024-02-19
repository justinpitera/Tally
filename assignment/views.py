from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import UserProfile
from coursework.models import Course
from dashboard.models import GradeNotification
from .forms import AssignmentForm, AttachmentFormSet, FeedbackForm, GradeForm
from django.views.generic import ListView
from .models import Assignment, Attachment
from django.http import FileResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Assignment, Submission
from .forms import SubmissionForm
from .forms import GradeSubmissionForm
from .models import Submission
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

    

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
            return redirect(reverse('view_assignment', kwargs={'assignment_id': assignment.id})+ "?tab=section2")
    else:
        form = SubmissionForm()

    return render(request, 'assignment/view_assignment.html', {'assignment': assignment, 'form': form, 'is_already_submitted': is_already_submitted})
    

def get_assignment_linked_course_id(request, assignment_id):
    try:
        assignment = Assignment.objects.get(pk=assignment_id)
        course_id = assignment.linked_course.id  # Accessing via the field name
        return JsonResponse({'course_id': course_id})
    except Assignment.DoesNotExist:
        raise Http404("Assignment does not exist")

@login_required
def view_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    user_profile = UserProfile.objects.get(user=request.user)
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR

    # Initialize variables
    num_submissions = 0
    submission_grade = None 
    submission_comments = None

    if is_instructor:
        # Count the number of submissions for this assignment if the user is an instructor
        num_submissions = Submission.objects.filter(assignment=assignment).count()
    
    submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    if submission:
        # If there is a submission by the user, retrieve the grade
        submission_grade = submission.grade
        submission_comments = submission.comments
        is_already_submitted = True
    else:
        is_already_submitted = False

    if request.method == 'POST' and 'assignment_edit' in request.POST:
        # Handle the assignment edit form
        assignment_form = AssignmentForm(request.POST, instance=assignment)
        if assignment_form.is_valid():
            assignment_form.save()
            return redirect('view_assignment', assignment_id=assignment_id)
    else:
        assignment_form = AssignmentForm(instance=assignment)

    form = FeedbackForm()  # For feedbacks
    submissions = Submission.objects.filter(assignment=assignment).select_related('student')
    feedbacks = []

    if not is_instructor:
        feedbacks = submission.feedbacks.all() if submission else []
    return render(request, 'assignment/view_assignment.html', {
        'assignment': assignment,
        'is_already_submitted': is_already_submitted,
        'is_instructor': is_instructor,
        'submissions': submissions,
        'form': form,
        'feedbacks': feedbacks,
        'assignmentForm': assignment_form,
        'num_submissions': num_submissions,
        'submission_grade': submission_grade,
        'submission_comments': submission_comments,
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


@login_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    assignment = submission.assignment
    course = assignment.course
    receiver = submission.student

    if submission.comments:
        comments = submission.comments
    else:
        comments = "No comments"

    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            # Create a new GradeNotification instance
            notification = GradeNotification(course=course, assignment=assignment, receiver=receiver, comments=comments, read=False)
            notification.save()

            # Optionally, inform the user that a grade notification has been created
            messages.success(request, "The submission has been graded and the student notified.")
            url = reverse('view_assignment', args=[assignment.id]) + "?tab=section2"
            return redirect(url)
    else:
        form = GradeSubmissionForm(instance=submission)
    
    return render(request, 'assignment/grade_submission.html', {'form': form, 'submission': submission, 'assignment': assignment})


@login_required
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.role != UserProfile.INSTRUCTOR:
        return HttpResponseForbidden("You are not authorized to edit assignments.")

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        formset = AttachmentFormSet(request.POST, request.FILES, instance=assignment)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(reverse('view_assignment', kwargs={'assignment_id': assignment.id}))
    else:
        form = AssignmentForm(instance=assignment)
        formset = AttachmentFormSet(instance=assignment)

    return render(request, 'assignment/view_assignment.html', {'form': form, 'formset': formset, 'assignment': assignment})



@login_required
def add_feedback(request, submission_id):
    # Fetch the user's profile
    user_profile = UserProfile.objects.get(user=request.user)
    # Check if the user is an instructor
    is_instructor = user_profile.role == UserProfile.INSTRUCTOR
    submission = get_object_or_404(Submission, pk=submission_id)
    assignment = submission.assignment
    assignment_id = submission.assignment.id

    if is_instructor:
        if request.method == 'POST':
            form = FeedbackForm(request.POST, request.FILES)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.submission = submission
                feedback.author = request.user
                feedback.save()
                url = reverse('view_assignment', args=[assignment_id]) + "?tab=section2"
                return redirect(url)
        else:
            form = FeedbackForm()
    else:
        if request.method == 'POST':
            form = FeedbackForm(request.POST, request.FILES)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.submission = submission
                feedback.author = request.user
                feedback.save()
                url = reverse('view_assignment', args=[assignment_id]) + "?tab=section3"
                return redirect(url)
        else:
            form = FeedbackForm()

    return render(request, 'assignment/add_feedback.html', {'form': form, 'submission': submission, 'assignment': assignment, 'is_instructor':is_instructor})



@login_required
def create_assignment(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, course_id=course_id)
        formset = AttachmentFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            formset.instance = assignment
            formset.save()
            return redirect('view_assignment', assignment_id=assignment.id)
    else:
        form = AssignmentForm(course_id=course_id)
        formset = AttachmentFormSet()
    return render(request, 'assignment/create_assignment.html', {
        'form': form,
        'formset': formset,
        'course': course,
    })


@login_required
def delete_assignment(request, assignment_id):
    # Fetch the assignment to be deleted
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Fetch the user's profile to check if they have the right to delete
    user_profile = UserProfile.objects.get(user=request.user)

    # Only allow instructors (or other authorized roles) to delete assignments
    if user_profile.role != UserProfile.INSTRUCTOR:
        return HttpResponseForbidden("You are not authorized to delete this assignment.")

    course_id = assignment.course.id  # Save course id for redirect

    # Perform the deletion
    assignment.delete()

    # Optionally, display a success message
    messages.success(request, "Assignment deleted successfully.")

    # Redirect to the assignment list, or another appropriate page
    return redirect(reverse('view_course', kwargs={'course_id': course_id}) + "?tab=assignments")




