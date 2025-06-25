from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import Ticket
from django.template import loader
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import pandas as pd


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
            template = loader.get_template('tickets/ticket_success.html')
            return HttpResponse(template.render({}, request))
            # return redirect('staff_dashboard')
    else:
        form = TicketForm()

    return render(request, 'users/staff_dashboard.html', {'form': form})

@login_required
def staff_ticket_list(request):
    if request.user.role != 'STAFF':
        return redirect('login')

    tickets = request.user.tickets.all()
    return render(request, 'tickets/staff_ticket_list.html', {'tickets': tickets})


@login_required
def support_ticket_list(request):
    if request.user.role != 'SUPPORT':
        return redirect('login')

    tickets = Ticket.objects.all()
    return render(request, 'tickets/support_ticket_list.html', {'tickets': tickets})

@login_required
def update_ticket_status(request, ticket_id):
    if request.user.role != 'SUPPORT':
        return redirect('login')

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['UNDER_REVIEW', 'SOLVED']:
            ticket.status = new_status
            ticket.save()
            from notifications.models import Notification
            Notification.objects.create(
                user=ticket.created_by,
                ticket=ticket,
                message=f"Your ticket '{ticket.title}' status changed to {ticket.status}."
            )
            return redirect('support_ticket_list')

    return render(request, 'tickets/update_ticket_status.html', {'ticket': ticket})

@login_required
def support_ticket_list(request):
    if request.user.role != 'SUPPORT':
        return redirect('login')

    tickets = Ticket.objects.all()

    # Filter
    status = request.GET.get('status')
    if status:
        tickets = tickets.filter(status=status)

    query = request.GET.get('q')
    if query:
        tickets = tickets.filter(title__icontains=query)

    return render(request, 'tickets/support_ticket_list.html', {'tickets': tickets})

from reportlab.pdfgen import canvas
from django.http import HttpResponse

@login_required
def export_tickets_pdf(request):
    if request.user.role not in ['ADMIN', 'SUPPORT']:
        return redirect('login')

    tickets = Ticket.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tickets.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Ticket Report")

    y = 750
    for ticket in tickets:
        p.drawString(100, y, f"{ticket.id} | {ticket.title} | {ticket.status}")
        y -= 20
        if y < 100:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response

@login_required
def export_tickets_excel(request):
    if request.user.role not in ['ADMIN', 'SUPPORT']:
        return redirect('login')

    tickets = Ticket.objects.all().values('id', 'title', 'status', 'created_at', 'created_by__username')
    df = pd.DataFrame(list(tickets))

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="tickets.xlsx"'
    df.to_excel(response, index=False)
    return response
