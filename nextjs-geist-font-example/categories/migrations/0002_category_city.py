# Generated migration to add city foreign key to Category with default city assignment

from django.db import migrations, models
import django.db.models.deletion

def set_default_city(apps, schema_editor):
    City = apps.get_model('cities', 'City')
    Category = apps.get_model('categories', 'Category')
    default_city = City.objects.first()
    for category in Category.objects.all():
        category.city = default_city
        category.save()

class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('cities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='cities.city', verbose_name='Город'),
        ),
        migrations.RunPython(set_default_city),
        migrations.AlterField(
            model_name='category',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='cities.city', verbose_name='Город'),
        ),
    ]
