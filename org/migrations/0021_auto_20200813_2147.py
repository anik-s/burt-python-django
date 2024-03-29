# Generated by Django 3.0.3 on 2020-08-13 15:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0020_platformbusinesssubmodeltype'),
    ]

    operations = [
        migrations.AddField(
            model_name='personjob',
            name='end_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='personjob',
            name='start_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.CreateModel(
            name='OrganizationHasBusinessModelType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Organization')),
                ('pbm_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.PlatformBusinessSubModelType')),
            ],
            options={
                'db_table': 'organization_has_business_model_types',
            },
        ),
    ]
