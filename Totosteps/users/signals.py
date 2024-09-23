
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import User

@receiver(post_save, sender=User)
def assign_user_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            # Add the superuser to the admin group
            admin_group, created = Group.objects.get_or_create(name="Admin")
            instance.groups.add(admin_group)
            
            # Assign admin permissions
            admin_permissions = Permission.objects.filter(
                codename__in=['view_dashboard', 'edit_questions', 'view_users', 'view_children', 'delete_children', 'restrict_users']
            )
            instance.user_permissions.set(admin_permissions)
        
        elif instance.role == "parent":
            # Assign parent group and permissions
            parent_group, created = Group.objects.get_or_create(name="Parent")
            instance.groups.add(parent_group)
            
            parent_permissions = Permission.objects.filter(
                codename__in=[
                    'can_add_child', 'can_view_resources', 'can_view_milestones',
                    'can_view_assessment', 'can_view_results', 'can_logout',
                    'can_create_account', 'can_login'
                ]
            )
            instance.user_permissions.set(parent_permissions)
        
        else:
            # Default group for regular users
            default_group, created = Group.objects.get_or_create(name="Default User")
            instance.groups.add(default_group)
            default_permissions = Permission.objects.filter(codename="view_dashboard")
            instance.user_permissions.set(default_permissions)

        instance.save()
