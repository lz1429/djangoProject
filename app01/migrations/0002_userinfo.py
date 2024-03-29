# Generated by Django 3.0.5 on 2024-01-30 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='姓名')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('create_date', models.DateField(verbose_name='入职时间')),
                ('account', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='月薪')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号码')),
                ('birth_date', models.DateField(verbose_name='出生日期')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Department', verbose_name='部门')),
            ],
        ),
    ]
