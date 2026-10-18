from django.core.management.base import BaseCommand
from django.contrib.auth.models import (
    Group,
    Permission,
)


class Command(BaseCommand):
    help = "Create roles and assign permissions"

    def handle(self, *args, **kwargs):

        roles = [
            "Admin",
            "Manager",
            "Cashier",
            "Stock Keeper",
        ]

        groups = {}

        for role in roles:
            group, created = Group.objects.get_or_create(
                name=role
            )
            groups[role] = group

        # Admin can manage users.
        user_permissions = Permission.objects.filter(
            content_type__app_label="auth",
            content_type__model="user",
        )

        groups["Admin"].permissions.add(
            *user_permissions
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Roles and permissions configured!"
            )
        )