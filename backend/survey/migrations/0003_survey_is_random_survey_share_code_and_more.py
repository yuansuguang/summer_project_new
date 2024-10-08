# Generated by Django 5.0.6 on 2024-06-04 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_question_submit_question_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='is_random',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='survey',
            name='share_code',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='max_submission',
            field=models.IntegerField(default=99999),
        ),
    ]
