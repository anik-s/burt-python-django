# Generated by Django 3.0.3 on 2020-07-03 18:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0017_librarycontentperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformLibraryContent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('library_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.LibraryContent')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Platform')),
            ],
            options={
                'db_table': 'platform_library_contents',
            },
        ),
        migrations.CreateModel(
            name='PersonLibraryContent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('library_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.LibraryContent')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Person')),
            ],
            options={
                'db_table': 'person_library_contents',
            },
        ),
        migrations.CreateModel(
            name='OrganizationLibraryContent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('library_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.LibraryContent')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Organization')),
            ],
            options={
                'db_table': 'organization_library_contents',
            },
        ),
        migrations.CreateModel(
            name='FundingLibraryContent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('funding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.FundingRound')),
                ('library_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.LibraryContent')),
            ],
            options={
                'db_table': 'funding_library_contents',
            },
        ),
        migrations.CreateModel(
            name='EventLibraryContent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Event')),
                ('library_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.LibraryContent')),
            ],
            options={
                'db_table': 'event_library_contents',
            },
        ),
        migrations.CreateModel(
            name='AcquisitionLibraryContent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('acquisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Acquisition')),
                ('library_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.LibraryContent')),
            ],
            options={
                'db_table': 'acquisition_library_contents',
            },
        ),
    ]
