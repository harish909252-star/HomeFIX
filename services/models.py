from django.db import models


class Booking(models.Model):

    # =====================================================
    # STATUS
    # =====================================================

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Arrived", "Arrived"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    # =====================================================
    # BOOKING DETAILS
    # =====================================================

    name = models.CharField(
        max_length=100
    )

    mobile_number = models.CharField(
        max_length=20
    )

    address = models.TextField()
    

    pincode = models.CharField(
        max_length=6,
        default="",
        verbose_name="PIN Code",
    )

    appliance = models.CharField(
        max_length=100
    )

    service = models.CharField(
        max_length=100
    )

    booking_date = models.DateField()

    preferred_time = models.CharField(
        max_length=50
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):
        return f"{self.name} - {self.appliance} - {self.status}"