# Generated by Django 3.1.5 on 2021-01-20 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_temprecipe_snippet'),
    ]

    operations = [
        migrations.CreateModel(
            name='FullRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=200)),
                ('steps', models.CharField(max_length=500)),
                ('meta', models.CharField(max_length=300)),
                ('nutrition', models.CharField(max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='temprecipe',
            name='snippet',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.CharField(max_length=100)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.fullrecipe')),
            ],
        ),
    ]