from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import Ticket

@login_required
def create_ticket(request):
    if request.user.role != 'STAFF':
        return redirect('login')

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('staff_dashboard')
    else:
        form = TicketForm()

    return render(request, 'tickets/create_ticket.html', {'form': form})
