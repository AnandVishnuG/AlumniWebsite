from django.contrib.auth.models import Permission

# Define permission codename
CAN_ACCESS_FILE = 'can_access_file'

# Create permission
can_access_file = Permission.objects.create(
    codename=CAN_ACCESS_FILE,
    name='Can access file',
)
