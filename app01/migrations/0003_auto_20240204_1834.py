# Generated by Django 3.0.5 on 2024-02-04 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
            ],
        ),
        migrations.AlterField(
            model_name='department',
            name='title',
            field=models.CharField(max_length=32, verbose_name='部门名称'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='account',
            field=models.DecimalField(decimal_places=2, default=8000, max_digits=10, verbose_name='月薪'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='depart',
            field=models.ForeignKey(default=49, on_delete=django.db.models.deletion.CASCADE, to='app01.Department', verbose_name='部门'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别'),
        ),
    ]
