from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
import random

from alx_travel_app.alx_travel_app import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seed the database with sample listing data'

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')

        # Clear existing data to prevent duplicates on re-run
        self.stdout.write('Clearing old data...')
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create sample users
        self.create_users()

        # Create sample listings
        self.create_listings()

        # Create sample bookings
        self.create_bookings()

        # Create sample reviews
        self.create_reviews()

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded the database!')
        )

    def create_users(self):
        users_data = [
            {'username': 'john_host', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_guest', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'bob_traveler', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Johnson'},
            {'username': 'alice_host', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Brown'},
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')

    def create_listings(self):
        hosts = User.objects.filter(username__in=['john_host', 'alice_host'])

        listings_data = [
            {
                'title': 'Cozy Beach House',
                'description': 'Beautiful beach house with ocean view',
                'price_per_night': Decimal('150.00'),
                'location': 'Miami, FL',
                'amenities': 'WiFi, Pool, Beach Access, Parking'
            },
            {
                'title': 'Mountain Cabin Retreat',
                'description': 'Peaceful cabin in the mountains',
                'price_per_night': Decimal('120.00'),
                'location': 'Aspen, CO',
                'amenities': 'WiFi, Fireplace, Hiking Trails, Parking'
            },
            {
                'title': 'Downtown Apartment',
                'description': 'Modern apartment in city center',
                'price_per_night': Decimal('200.00'),
                'location': 'New York, NY',
                'amenities': 'WiFi, Gym, Concierge, Public Transport'
            },
            {
                'title': 'Lakeside Villa',
                'description': 'Luxurious villa by the lake',
                'price_per_night': Decimal('300.00'),
                'location': 'Lake Tahoe, CA',
                'amenities': 'WiFi, Private Dock, Hot Tub, Parking'
            }
        ]

        for i, listing_data in enumerate(listings_data):
            listing, created = Listing.objects.get_or_create(
                title=listing_data['title'],
                defaults={
                    **listing_data,
                    'host': hosts[i % len(hosts)]
                }
            )
            if created:
                self.stdout.write(f'Created listing: {listing.title}')

    def create_bookings(self):
        listings = Listing.objects.all()
        guests = User.objects.filter(username__in=['jane_guest', 'bob_traveler'])

        for listing in listings:
            for guest in guests:
                check_in = date.today() + timedelta(days=random.randint(1, 30))
                check_out = check_in + timedelta(days=random.randint(2, 7))
                nights = (check_out - check_in).days
                total_price = listing.price_per_night * nights

                booking, created = Booking.objects.get_or_create(
                    listing=listing,
                    guest=guest,
                    check_in_date=check_in,
                    defaults={
                        'check_out_date': check_out,
                        'total_price': total_price,
                        'status': random.choice(['pending', 'confirmed', 'completed'])
                    }
                )
                if created:
                    self.stdout.write(f'Created booking for {listing.title}')

    def create_reviews(self):
        # Create reviews for completed bookings
        completed_bookings = Booking.objects.filter(status='completed')

        review_comments = [
            "Great place to stay! Highly recommended.",
            "Beautiful location and excellent amenities.",
            "Host was very responsive and helpful.",
            "Clean and comfortable accommodation.",
            "Amazing views and peaceful environment."
        ]

        for booking in completed_bookings:
            review, created = Review.objects.get_or_create(
                listing=booking.listing,
                reviewer=booking.guest,
                defaults={
                    'rating': random.randint(3, 5),
                    'comment': random.choice(review_comments)
                }
            )
            if created:
                self.stdout.write(f'Created review for {booking.listing.title}')
