# Generated by Django 4.0.3 on 2022-07-05 07:23

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_audio_alter_profile_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(default='projects/empty.png', upload_to='projects')),
                ('demo_link', models.CharField(blank=True, max_length=200, null=True)),
                ('source_code', models.CharField(blank=True, max_length=200, null=True)),
                ('vote_count', models.IntegerField(default=0)),
                ('vote_ratio', models.IntegerField(default=0)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='file',
            field=models.FileField(default='files/default.xlsx', upload_to='files', validators=[users.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_github',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_instagram',
            field=models.CharField(default='instagram', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_telegram',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_website',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_youtube',
            field=models.CharField(max_length=100),
        ),
    ]