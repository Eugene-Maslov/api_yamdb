from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_auto_20230106_1952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
