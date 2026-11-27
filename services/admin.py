from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html
from django.middleware.csrf import get_token
from django.conf import settings

try:
    from twilio.rest import Client
except ModuleNotFoundError:  # pragma: no cover - depends on optional integration package
    Client = None

from .models import Booking


# =========================================================
# WHATSAPP FUNCTION
# =========================================================

def send_booking_whatsapp(booking, status):

    # =====================================================
    # TWILIO SETTINGS
    # =====================================================

    account_sid = getattr(
        settings,
        "TWILIO_ACCOUNT_SID",
        ""
    )

    auth_token = getattr(
        settings,
        "TWILIO_AUTH_TOKEN",
        ""
    )

    whatsapp_from = getattr(
        settings,
        "TWILIO_WHATSAPP_FROM",
        ""
    )

    # =====================================================
    # CHECK SETTINGS
    # =====================================================

    if not account_sid:
        raise ValueError(
            "TWILIO_ACCOUNT_SID is missing."
        )

    if not auth_token:
        raise ValueError(
            "TWILIO_AUTH_TOKEN is missing."
        )

    if not whatsapp_from:
        raise ValueError(
            "TWILIO_WHATSAPP_FROM is missing."
        )

    # =====================================================
    # CUSTOMER MOBILE
    # =====================================================

    customer_mobile = "".join(
        ch
        for ch in str(booking.mobile_number)
        if ch.isdigit()
    )

    # If number is stored as 91XXXXXXXXXX
    if (
        len(customer_mobile) == 12
        and customer_mobile.startswith("91")
    ):
        customer_mobile = customer_mobile[2:]

    if len(customer_mobile) != 10:
        raise ValueError(
            "Customer mobile number must contain exactly 10 digits."
        )

    customer_whatsapp = (
        "whatsapp:+91"
        + customer_mobile
    )

    # =====================================================
    # TWILIO FROM NUMBER
    # =====================================================

    if not whatsapp_from.startswith(
        "whatsapp:"
    ):
                   whatsapp_from = (
            "whatsapp:"
            + whatsapp_from
        )

    # =====================================================
    # CONFIRMED MESSAGE
    # =====================================================

    if status == "Confirmed":

        body = (
            f"Hello {booking.name},\n\n"
            f"Your HomeFix booking has been "
            f"CONFIRMED. ✅\n\n"
            f"Appliance: {booking.appliance}\n"
            f"Service: {booking.service}\n"
            f"Date: {booking.booking_date}\n"
            f"Time: {booking.preferred_time}\n\n"
            f"Thank you for choosing HomeFix."
        )

    # =====================================================
    # ARRIVED MESSAGE
    # =====================================================

    elif status == "Arrived":

        body = (
            f"Hello {booking.name},\n\n"
            f"HomeFix technician has ARRIVED. 🔧📍\n\n"
            f"Appliance: {booking.appliance}\n"
            f"Service: {booking.service}\n\n"
            f"Thank you for choosing HomeFix."
        )

    # =====================================================
    # COMPLETED MESSAGE
    # =====================================================

    elif status == "Completed":

        body = (
            f"Hello {booking.name},\n\n"
            f"Your HomeFix service has been "
            f"COMPLETED. ✅\n\n"
            f"Thank you for choosing HomeFix."
        )

    # =====================================================
    # CANCELLED MESSAGE
    # =====================================================

    elif status == "Cancelled":

        body = (
            f"Hello {booking.name},\n\n"
            f"Your HomeFix booking has been "
            f"CANCELLED. ❌\n\n"
            f"Please contact HomeFix for more information."
        )

    else:

        raise ValueError(
            "Invalid WhatsApp status."
        )

    # =====================================================
    # TWILIO CLIENT
    # =====================================================

    if Client is None:
        raise RuntimeError(
            "Twilio package is not installed. Install it with 'pip install twilio' or add it to requirements.txt."
        )

    client = Client(
        account_sid,
        auth_token
    )

    # =====================================================
    # SEND MESSAGE
    # =====================================================

    message = client.messages.create(
        from_=whatsapp_from,
        to=customer_whatsapp,
        body=body
    )

    return message.sid

# BOOKING ADMIN
# =========================================================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    # =====================================================
    # LIST DISPLAY
    # =====================================================

    list_display = (
        "name",
        "mobile_display",
        "address_display",
        "pincode",
        "appliance",
        "service",
        "booking_date",
        "preferred_time",
        "status_display",
        "booking_actions",
        "created_at",
    )

    # =====================================================
    # FILTERS
    # =====================================================
    list_filter = (
    "status",
    "appliance",
    "service",
    "booking_date",
)

    # =====================================================
    # SEARCH
    # =====================================================

    search_fields = (
        "name",
        "mobile_number",
        "address",
        "pincode",
        "appliance",
        "service",
    )

    # =====================================================
    # READ ONLY
    # =====================================================

    readonly_fields = (
        "created_at",
    )

    # =====================================================
    # ORDERING
    # =====================================================

    ordering = (
        "-created_at",
    )

    # =====================================================
    # MOBILE DISPLAY (+91)
    # =====================================================

    @admin.display(description="Phone Number")
    def mobile_display(self, obj):
        digits = "".join(ch for ch in str(obj.mobile_number) if ch.isdigit())
        if len(digits) == 10:
            return "+91 " + digits
        if len(digits) == 12 and digits.startswith("91"):
            return "+" + digits[:2] + " " + digits[2:]
        return obj.mobile_number or "-"

    # =====================================================
    # ADDRESS DISPLAY
    # =====================================================

    @admin.display(
        description="Address"
    )
    def address_display(self, obj):

        if not obj.address:
            return "-"

        return obj.address

    @admin.display(description="Status")
    def status_display(self, obj):

        colors = {
            "Pending": "#F59E0B",
            "Confirmed": "#2196F3",
            "Arrived": "#8B5CF6",
            "Completed": "#16A34A",
            "Cancelled": "#DC2626",
        }

        color = colors.get(obj.status, "#6B7280")

        return format_html(
            """
            <span style="
                display:inline-block;
                background:{};
                color:white;
                padding:6px 12px;
                border-radius:20px;
                font-weight:700;
                font-size:12px;
            ">{}</span>
            """,
            color,
            obj.status
        )

    # =====================================================
    # BOOKING ACTIONS
    # =====================================================

    @admin.display(
        description="Booking Actions"
    )
    def booking_actions(self, obj):

        url = reverse(
            "admin:services_booking_status",
            args=[obj.pk]
        )

        request = getattr(
            self,
            "_current_request",
            None
        )

        csrf_token = ""

        if request:

            csrf_token = get_token(
                request
            )

        # =================================================
        # BUTTON FUNCTION
        # =================================================

        def make_button(status, label, background):
            return format_html(
                """
                <button
                    type="button"
                    style="
                        background:{};
                        color:white;
                        border:none;
                        padding:7px 12px;
                        border-radius:6px;
                        font-weight:700;
                        font-size:12px;
                        cursor:pointer;
                        margin-right:5px;
                        margin-bottom:4px;
                    "
                    onclick="(function(btn) {{
                        btn.disabled = true;
                        fetch('{}', {{
                            method: 'POST',
                            credentials: 'same-origin',
                            headers: {{
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'X-CSRFToken': '{}'
                            }},
                            body: new URLSearchParams({{status: '{}'}})
                        }})
                        .then(function(response) {{
                            if (!response.ok) {{
                                return response.text().then(function(text) {{
                                    throw new Error('HTTP ' + response.status + ': ' + text.slice(0, 300));
                                }});
                            }}
                            window.location.reload();
                        }})
                        .catch(function(error) {{
                            alert('Booking status update failed: ' + error.message);
                            btn.disabled = false;
                        }});
                    }})(this)"
                >
                    {}
                </button>
                """,
                background,
                url,
                csrf_token,
                status,
                label,
            )

        # =================================================
        # MAIN CONTAINER
        # =================================================

        html = format_html("")

        # =================================================
        # PENDING
        # =================================================

        if obj.status == "Pending":

            html += make_button(
                "Confirmed",
                "Confirm",
                "#2196F3"
            )

            html += make_button(
                "Cancelled",
                "Cancel",
                "#DC2626"
            )

        elif obj.status == "Confirmed":

            html += make_button(
                "Arrived",
                "Mark Arrived",
                "#8B5CF6"
            )

            html += make_button(
                "Cancelled",
                "Cancel",
                "#DC2626"
            )

        elif obj.status == "Arrived":

            html += make_button(
                "Completed",
                "Complete",
                "#16A34A"
            )

            html += make_button(
                "Cancelled",
                "Cancel",
                "#DC2626"
            )

        # =================================================
        # COMPLETED
        # =================================================

        elif obj.status == "Completed":

            html += format_html("""
            <span style="
                display:inline-block;
                background:#16A34A;
                color:white;
                padding:7px 12px;
                border-radius:6px;
                font-weight:700;
                font-size:12px;
            ">
                ✓ Completed
            </span>
            """)

        # =================================================
        # CANCELLED
        # =================================================

        elif obj.status == "Cancelled":

            html += format_html("""
            <span style="
                display:inline-block;
                background:#DC2626;
                color:white;
                padding:7px 12px;
                border-radius:6px;
                font-weight:700;
                font-size:12px;
            ">
                ✗ Cancelled
            </span>
            """)
        return format_html(
            """
            <div style="
                display:flex;
                flex-wrap:wrap;
                gap:3px;
                align-items:center;
                min-width:120px;
            ">{}</div>
            """,
            html
        )
    # =====================================================
    # CUSTOM ADMIN URL
    # =====================================================

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [

            path(
                "<int:booking_id>/status/",
                self.admin_site.admin_view(
                    self.change_status
                ),
                name="services_booking_status",
            ),

        ]

        return custom_urls + urls

    # =====================================================
    # CHANGE STATUS
    # =====================================================

    def change_status(
        self,
        request,
        booking_id
    ):

        # =================================================
        # ONLY POST
        # =================================================

        if request.method != "POST":

            messages.error(
                request,
                "Invalid request."
            )

            return redirect(
                "admin:services_booking_changelist"
            )

        # =================================================
        # GET BOOKING
        # =================================================

        booking = get_object_or_404(
            Booking,
            pk=booking_id
        )

        # =================================================
        # GET NEW STATUS
        # =================================================

        new_status = request.POST.get(
            "status"
        )

        # =================================================
        # ALLOWED STATUS
        # =================================================

        allowed_statuses = [
            "Confirmed",
            "Arrived",
            "Completed",
            "Cancelled",
        ]

        if new_status not in allowed_statuses:

            messages.error(
                request,
                "Invalid booking status."
            )

            return redirect(
                "admin:services_booking_changelist"
            )

        # =================================================
        # OPTIONAL STATUS FLOW CHECK
        # =================================================

        valid_transitions = {

            "Pending": [
                "Confirmed",
                "Cancelled",
            ],

            "Confirmed": [
                "Arrived",
                "Cancelled",
            ],

            "Arrived": [
                "Completed",
                "Cancelled",
            ],

            "Completed": [],

            "Cancelled": [],
        }

        if new_status not in valid_transitions.get(
            booking.status,
            []
        ):

            messages.error(
                request,
                f"Cannot change status from "
                f"{booking.status} to "
                f"{new_status}."
            )

            return redirect(
                "admin:services_booking_changelist"
            )

        # =================================================
        # SAVE DATABASE STATUS FIRST
        # =================================================

        old_status = booking.status

        booking.status = new_status

        booking.save(
            update_fields=[
                "status"
            ]
        )


        # =================================================
        # SEND WHATSAPP
        # =================================================

        try:

            send_booking_whatsapp(
                booking,
                new_status
            )

            messages.success(
                request,
                f"{booking.name}: "
                f"{old_status} → {new_status}. "
                f"WhatsApp sent successfully."
            )

        except Exception as e:

            # =============================================
            # STATUS IS ALREADY SAVED
            # =============================================

            messages.warning(
                request,
                f"{booking.name}: "
                f"status changed from "
                f"{old_status} to "
                f"{new_status}. "
                f"WhatsApp was not sent. "
                f"Reason: {str(e)}"
            )

        # =================================================
        # RETURN ADMIN LIST
        # =================================================

        return redirect(
            "admin:services_booking_changelist"
        )

    # =====================================================
    # CURRENT REQUEST
    # =====================================================

    def changelist_view(
        self,
        request,
        extra_context=None
    ):

        self._current_request = request

        return super().changelist_view(
            request,
            extra_context=extra_context
        )
