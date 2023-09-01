# Generated by Django 3.2.19 on 2023-08-28 13:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('facade', '0020_alter_node_protocols'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignation',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('BOUND', 'Bound'), ('ACKNOWLEDGED', 'Acknowledged'), ('RETURNED', 'Assignation Returned (Only for Functions)'), ('DENIED', 'Denied (Assingment was rejected)'), ('ASSIGNED', 'Was able to assign to a pod'), ('PROGRESS', 'Progress (Assignment has current Progress)'), ('RECEIVED', 'Received (Assignment was received by an agent)'), ('ERROR', 'Error (Retrieable)'), ('CRITICAL', 'Critical Error (No Retries available)'), ('CANCEL', 'Assinment is beeing cancelled'), ('CANCELING', 'Cancelling (Assingment is currently being cancelled)'), ('CANCELLED', 'Assignment has been cancelled.'), ('YIELD', 'Assignment yielded a value (only for Generators)'), ('DONE', 'Assignment has finished')], default='PENDING', help_text='Current lifecycle of Assignation', max_length=300),
        ),
        migrations.AlterField(
            model_name='node',
            name='protocols',
            field=models.ManyToManyField(blank=True, help_text='The protocols this Node implements (e.g. Predicate)', related_name='nodes', to='facade.Protocol'),
        ),
    ]
