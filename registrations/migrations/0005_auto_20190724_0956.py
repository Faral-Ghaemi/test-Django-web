# Generated by Django 2.2.3 on 2019-07-24 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0004_auto_20190723_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membertype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='price',
            field=models.DecimalField(decimal_places=0, default=100, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Price',
        ),
        migrations.AddField(
            model_name='membertype',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrations.Category'),
        ),
    ]
