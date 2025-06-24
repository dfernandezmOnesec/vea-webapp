# Generated manually to fix data migration issue

from django.db import migrations

def populate_contact_names(apps, schema_editor):
    """Populate first_name and last_name from existing name field"""
    Contact = apps.get_model('directory', 'Contact')
    
    # Get all contacts that have a name but no first_name
    contacts = Contact.objects.filter(name__isnull=False).exclude(name='')
    
    for contact in contacts:
        # Split the name into first and last name
        name_parts = contact.name.strip().split(' ', 1)
        
        if len(name_parts) >= 2:
            contact.first_name = name_parts[0]
            contact.last_name = name_parts[1]
        else:
            # If only one name, put it in first_name
            contact.first_name = name_parts[0]
            contact.last_name = ''
        
        contact.save()

def reverse_populate_contact_names(apps, schema_editor):
    """Reverse operation - combine first_name and last_name back to name"""
    Contact = apps.get_model('directory', 'Contact')
    
    contacts = Contact.objects.all()
    
    for contact in contacts:
        if contact.first_name and contact.last_name:
            contact.name = f"{contact.first_name} {contact.last_name}".strip()
        elif contact.first_name:
            contact.name = contact.first_name
        else:
            contact.name = ''
        contact.save()

class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0004_alter_contact_first_name_alter_contact_last_name'),
    ]

    operations = [
        migrations.RunPython(populate_contact_names, reverse_populate_contact_names),
    ] 