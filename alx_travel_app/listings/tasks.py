from alx_travel_app.celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking


@shared_task(name='send_booking_confirmation_email')
def send_booking_confirmation_email(booking_id):
    """
    Send booking confirmation email asynchronously.
    """
    try:
        booking = Booking.objects.select_related('listing', 'user').get(booking_id=booking_id)

        subject = f'Booking Confirmation - {booking.listing.title}'

        message = f"""
Dear {booking.user.get_full_name() or booking.user.username},

Your booking has been confirmed!

Booking Details:
- Property: {booking.listing.title}
- Check-in: {booking.check_in_date}
- Check-out: {booking.check_out_date}
- Total Price: ${booking.total_price}
- Booking Reference: {booking.booking_id}

Thank you for choosing our service!

Best regards,
ALX Travel App Team
        """

        recipient_list = [booking.user.email]

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        return f"Email sent successfully to {booking.user.email}"

    except Booking.DoesNotExist:
        return f"Booking with ID {booking_id} not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"
