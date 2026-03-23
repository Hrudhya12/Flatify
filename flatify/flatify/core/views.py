from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Profile, TaskHistory, Flat


def get_next_user(flat, task_type):
    """
    Fair assignment algorithm:
    pick the user in this flat with the fewest completions for this task_type.
    """
    profiles = Profile.objects.filter(flat=flat)
    if not profiles.exists():
        return None

    counts = []
    for p in profiles:
        count = TaskHistory.objects.filter(
            flat=flat,
            user=p.user,
            task_type=task_type
        ).count()
        counts.append((p.user, count))

    counts.sort(key=lambda x: x[1])
    return counts[0][0]  # user


def rotate_profiles(flat, task_type):
    """
    Simple rotation algorithm per flat.
    Currently same rotation for both task types,
    but separated by task_type for future customization.
    """
    profiles = list(Profile.objects.filter(flat=flat).order_by('order'))

    if len(profiles) < 2:
        return  # nothing to rotate

    # Move first to last
    first = profiles[0]
    for i in range(1, len(profiles)):
        profiles[i].order = i - 1
        profiles[i].save()

    first.order = len(profiles) - 1
    first.save()


@login_required
def dashboard(request):
    # Ensure user has a profile and flat
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        raise Http404("Profile not found")

    if not profile.flat:
        raise Http404("You are not assigned to a flat")

    flat = profile.flat

    # Fair assignment: who should do what next
    cleaning_user_obj = get_next_user(flat, 'cleaning')
    essentials_user_obj = get_next_user(flat, 'essentials')

    cleaning_user = cleaning_user_obj.username if cleaning_user_obj else "Not set yet"
    essentials_user = essentials_user_obj.username if essentials_user_obj else "Not set yet"

    # History only for this flat
    history = TaskHistory.objects.filter(flat=flat).order_by('-completed_at')[:10]

    return render(request, 'core/dashboard.html', {
        'cleaning_user': cleaning_user,
        'essentials_user': essentials_user,
        'history': history,
    })


@login_required
def complete_task(request, task_type):
    if task_type not in ['cleaning', 'essentials']:
        raise Http404("Invalid task type")

    try:
        flat = request.user.profile.flat
    except Profile.DoesNotExist:
        raise Http404("Profile not found")

    if not flat:
        raise Http404("You are not assigned to a flat")

    # Create a history entry
    TaskHistory.objects.create(
        flat=flat,
        user=request.user,
        task_type=task_type
    )

    # Rotate profiles for this flat and task type
    rotate_profiles(flat, task_type)

    return redirect('dashboard')