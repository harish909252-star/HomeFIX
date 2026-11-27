from django.shortcuts import render, redirect
from django.contrib import messages
import re

from .models import Booking


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(
        request,
        "home.html"
    )


# =========================================================
# BOOK SERVICE
# =========================================================

def book_service(request):

    if request.method != "POST":
        return redirect("home")

    # =====================================================
    # FORM DATA
    # =====================================================

    name = request.POST.get(
        "name",
        ""
    ).strip()
    # Capitalize the first letter of each name word on the server too.
    name = " ".join(word.capitalize() for word in name.split())

    mobile = request.POST.get(
        "mobile",
        ""
    ).strip()

    address = request.POST.get(
        "address",
        ""
    ).strip()

    pincode = request.POST.get(
        "pincode",
        ""
    ).strip()

    appliance = request.POST.get(
        "appliance",
        ""
    ).strip()

    service = request.POST.get(
        "service",
        ""
    ).strip()

    preferred_date = request.POST.get(
        "preferred_date",
        ""
    ).strip()

    preferred_time = request.POST.get(
        "preferred_time",
        ""
    ).strip()

    # =====================================================
    # VALIDATION
    # =====================================================

    if not name:
        messages.error(
            request,
            "Please enter your name."
        )
        return redirect("home")

    if not mobile:
        messages.error(
            request,
            "Please enter your mobile number."
        )
        return redirect("home")

    if not address:
        messages.error(
            request,
            "Please enter your address."
        )
        return redirect("home")

    if not pincode:
        messages.error(request, "Please enter your 6-digit PIN code.")
        return redirect("home")

    if not re.fullmatch(r"[0-9]{6}", pincode):
        messages.error(request, "Please enter a valid 6-digit PIN code.")
        return redirect("home")

    if not appliance:
        messages.error(
            request,
            "Please select an appliance."
        )
        return redirect("home")

    if not service:
        messages.error(
            request,
            "Please select a service."
        )
        return redirect("home")

    if not preferred_date:
        messages.error(
            request,
            "Please select a booking date."
        )
        return redirect("home")

    if not preferred_time:
        messages.error(
            request,
            "Please select a preferred time."
        )
        return redirect("home")

    # =====================================================
    # MOBILE
    # =====================================================

    # Accept exactly 10 digits; Indian mobile numbers start with 6, 7, 8 or 9.
    if not re.fullmatch(r"[6-9][0-9]{9}", mobile):
        messages.error(
            request,
            "Please enter a valid 10-digit Indian mobile number."
        )
        return redirect("home")

    mobile_digits = mobile

    # =====================================================
    # CREATE BOOKING
    # =====================================================

    booking = Booking.objects.create(

        name=name,

        mobile_number=mobile_digits,

        address=address,

        pincode=pincode,

        appliance=appliance,

        service=service,

        booking_date=preferred_date,

        preferred_time=preferred_time,

        status="Pending",
    )

    # =====================================================
    # SUCCESS
    # =====================================================

    messages.success(
        request,
        "Booking submitted successfully! "
        "Your booking is now Pending."
    )

    # =====================================================
    # HOME
    # =====================================================

    return redirect("home")


# =========================================================
# STAFF DASHBOARD
# =========================================================

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def dashboard(request):
    bookings_qs = Booking.objects.all()

    counts = {
        "total": bookings_qs.count(),
        "pending": bookings_qs.filter(status="Pending").count(),
        "confirmed": bookings_qs.filter(status="Confirmed").count(),
        "arrived": bookings_qs.filter(status="Arrived").count(),
        "completed": bookings_qs.filter(status="Completed").count(),
        "cancelled": bookings_qs.filter(status="Cancelled").count(),
    }

    bookings = bookings_qs.order_by("-created_at")[:50]

    return render(request, "services/dashboard.html", {
        "counts": counts,
        "bookings": bookings,
    })