# Generated by Django 4.0.2 on 2022-12-18 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post111',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('cover', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]