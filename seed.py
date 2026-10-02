import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from registry.models import Category, Gift, SiteSettings

# Create Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin user created (admin / admin123)")

# Create Settings
SiteSettings.get_settings()

# Create Categories
categories = [
    "Quarto", "Cozinha", "Sala", "Banheiro", "Limpeza", "Casa", "Outros"
]

for idx, cat_name in enumerate(categories):
    Category.objects.get_or_create(name=cat_name, defaults={'order': idx})

# Add some mock gifts
if not Gift.objects.exists():
    cozinha = Category.objects.get(name="Cozinha")
    quarto = Category.objects.get(name="Quarto")

    Gift.objects.create(
        category=cozinha,
        name="Jogo de Panelas [DEMO]",
        description="Lindo jogo de panelas antiaderente.",
        total_quantity=2,
    )
    Gift.objects.create(
        category=quarto,
        name="Jogo de Cama King [DEMO]",
        description="Jogo de cama 400 fios, 100% algodão.",
        total_quantity=3,
    )
    print("Mock gifts created")

print("Seed done")
