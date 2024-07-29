import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.text import slugify

def generate_unique_slugs(apps, schema_editor):
    Product = apps.get_model('app', 'Product')
    for product in Product.objects.all():
        if not product.slug:
            product.slug = slugify(product.title)  # Use 'title' instead of 'name'
        unique_slug = product.slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{product.slug}-{num}'
            num += 1
        product.slug = unique_slug
        product.save()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_customer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=100),  # Added field without unique constraint
        ),
        migrations.RunPython(generate_unique_slugs),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),  # Added unique constraint afterward
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
