# Generated by Django 4.2.1 on 2023-08-24 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_alter_posts_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='ShouldDisLikeButtonVisibleDOM',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='posts',
            name='ShouldLikeButtonVisibleDOM',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='posts',
            name='timestamp',
            field=models.CharField(default='Thu 24 Aug 2023, 07:25PM', max_length=50),
        ),
    ]
