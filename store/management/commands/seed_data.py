"""
Management command to populate Glowify with sample data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from store.models import Category, Product, Ingredient


class Command(BaseCommand):
    help = 'Seeds the database with sample Glowify product data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed Glowify data...'))

        # Clear existing data
        Product.objects.all().delete()
        Category.objects.all().delete()
        Ingredient.objects.all().delete()
        self.stdout.write('Cleared existing data.')

        # Create Categories
        categories_data = [
            {
                'name': 'Lipstick',
                'description': 'Bold, hydrating lipsticks for every occasion.',
            },
            {
                'name': 'Serum',
                'description': 'Targeted treatments for radiant, healthy skin.',
            },
            {
                'name': 'Foundation',
                'description': 'Buildable coverage for a flawless complexion.',
            },
            {
                'name': 'Blush',
                'description': 'Natural-looking flush for a youthful glow.',
            },
            {
                'name': 'Lip Gloss',
                'description': 'Glossy, hydrating lip colors for a luscious pout.',
            },
            {
                'name': 'Mist',
                'description': 'Refreshing facial mists for instant hydration.',
            },
        ]

        categories = {}
        for cat_data in categories_data:
            cat = Category.objects.create(**cat_data)
            categories[cat.name] = cat
            self.stdout.write(f'  Created category: {cat.name}')

        # Create Ingredients
        ingredients_data = [
            {
                'name': 'Hyaluronic Acid',
                'description': 'A powerful humectant that draws moisture from the environment into your skin, keeping it plump, dewy, and supple all day long.',
                'benefit': 'Provides hydration without heaviness',
                'image_hint': 'hyaluronic-acid',
            },
            {
                'name': 'Niacinamide',
                'description': 'A versatile form of Vitamin B3 that works to minimize the appearance of pores, even skin tone, and regulate sebum production.',
                'benefit': 'Refines pores and regulates excess oil production',
                'image_hint': 'niacinamide',
            },
            {
                'name': 'Retinol',
                'description': 'A gold-standard anti-aging ingredient that promotes cell turnover, reduces fine lines, and improves skin texture over time.',
                'benefit': 'Reduces fine lines and improves texture',
                'image_hint': 'retinol',
            },
            {
                'name': 'Vitamin C',
                'description': 'A potent antioxidant that brightens the complexion, fades dark spots, and protects skin from environmental damage.',
                'benefit': 'Brightens and evens skin tone',
                'image_hint': 'vitamin-c',
            },
        ]

        for ing_data in ingredients_data:
            ing_data.pop('image_hint', None)
            ing = Ingredient.objects.create(**ing_data)
            self.stdout.write(f'  Created ingredient: {ing.name}')

        # Create Products with placeholder image URLs
        products_data = [
            {
                'name': 'Glow Matte Lipstick – Rose Bliss',
                'category': categories['Lipstick'],
                'description': 'A velvety matte lipstick infused with moisturizing agents for long-lasting wear. The Rose Bliss shade is a perfect everyday pink that flatters all skin tones. Enriched with Vitamin E and jojoba oil to keep your lips soft and nourished throughout the day.',
                'price': 799,
                'badge': 'Best Seller',
                'rating': 4.9,
                'review_count': 97,
                'is_featured': True,
                'stock': 150,
                'image_url': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=400&fit=crop&crop=center',
            },
            {
                'name': 'Radiant Glow Serum',
                'category': categories['Serum'],
                'description': 'A lightweight, fast-absorbing serum packed with hyaluronic acid and niacinamide. This powerhouse formula delivers intense hydration while minimizing the appearance of pores and fine lines. Suitable for all skin types, including sensitive skin.',
                'price': 1299,
                'badge': 'New',
                'rating': 4.7,
                'review_count': 166,
                'is_featured': True,
                'stock': 200,
                'image_url': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&h=400&fit=crop&crop=center',
            },
            {
                'name': 'Velvet Touch Foundation',
                'category': categories['Foundation'],
                'description': 'A buildable, medium-to-full coverage foundation with a natural velvet finish. Infused with skin-caring ingredients that blur imperfections and give skin a healthy, radiant appearance. Available in 40 shades to match every skin tone.',
                'price': 1099,
                'badge': 'Trending',
                'rating': 4.6,
                'review_count': 214,
                'is_featured': True,
                'stock': 175,
                'image_url': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop&crop=center',
            },
            {
                'name': 'Blush & Bloom Cheek Tint',
                'category': categories['Blush'],
                'description': 'A buildable, blendable cheek tint that gives a natural, flushed look lasting up to 12 hours. The lightweight, water-based formula melts into skin for a fresh, dewy finish. Perfect for creating that coveted "your skin but better" glow.',
                'price': 699,
                'badge': '',
                'rating': 4.9,
                'review_count': 97,
                'is_featured': True,
                'stock': 120,
                'image_url': 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop&crop=center',
            },
            {
                'name': 'Luxe Shine Lip Gloss – Crystal Pink',
                'category': categories['Lip Gloss'],
                'description': 'A high-shine, non-sticky lip gloss in a beautiful crystal pink shade. Infused with vitamin E and castor oil for a nourishing, plumping effect. The doe-foot applicator ensures precise application for a perfectly glossy pout every time.',
                'price': 749,
                'badge': 'Hot Pick',
                'rating': 4.7,
                'review_count': 186,
                'is_featured': True,
                'stock': 130,
                'image_url': 'https://images.unsplash.com/photo-1599733594230-6b823276b5b0?w=400&h=400&fit=crop&crop=center',
            },
            {
                'name': 'Hydrating Glow Face Mist',
                'category': categories['Mist'],
                'description': 'An ultra-fine, refreshing facial mist that instantly hydrates and revives tired skin. Formulated with hyaluronic acid, rose water, and green tea extract to deliver a burst of moisture and antioxidant protection throughout the day.',
                'price': 599,
                'badge': 'Skin Savvy',
                'rating': 4.8,
                'review_count': 132,
                'is_featured': True,
                'stock': 160,
                'image_url': 'https://images.unsplash.com/photo-1598662957563-ee4965d4d72c?w=400&h=400&fit=crop&crop=center',
            },
            # Additional non-featured products for the shop page
            {
                'name': 'Rose Petal Eye Shadow Palette',
                'category': categories['Blush'],
                'description': 'A stunning 12-shade palette featuring warm pinks, roses, and neutrals perfect for creating everything from everyday glam to dramatic evening looks.',
                'price': 1499,
                'badge': 'New',
                'rating': 4.8,
                'review_count': 78,
                'is_featured': False,
                'stock': 90,
                'image_url': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=400&fit=crop&crop=top',
            },
            {
                'name': 'Dewy Skin Tinted Moisturizer',
                'category': categories['Foundation'],
                'description': 'A lightweight tinted moisturizer with SPF 30 that evens out skin tone while providing all-day hydration. Perfect for a no-makeup makeup look.',
                'price': 899,
                'badge': 'Skin Savvy',
                'rating': 4.5,
                'review_count': 143,
                'is_featured': False,
                'stock': 110,
                'image_url': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop&crop=center',
            },
            {
                'name': 'Plum Berry Matte Lip Color',
                'category': categories['Lipstick'],
                'description': 'A rich, pigmented matte lip color in a sophisticated plum berry shade. Long-wearing formula with a comfortable, non-drying finish.',
                'price': 849,
                'badge': 'Trending',
                'rating': 4.6,
                'review_count': 112,
                'is_featured': False,
                'stock': 140,
                'image_url': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&h=400&fit=crop&crop=center',
            },
            {
                'name': 'Brightening Vitamin C Serum',
                'category': categories['Serum'],
                'description': 'A potent 15% Vitamin C serum that fades dark spots, brightens complexion, and protects against free radical damage. Formulated with ferulic acid for enhanced stability.',
                'price': 1599,
                'badge': 'Best Seller',
                'rating': 4.9,
                'review_count': 289,
                'is_featured': False,
                'stock': 85,
                'image_url': 'https://images.unsplash.com/photo-1556228720-da92f67f2e1e?w=400&h=400&fit=crop&crop=center',
            },
        ]

        for prod_data in products_data:
            prod = Product.objects.create(**prod_data)
            self.stdout.write(f'  Created product: {prod.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nSeeding complete!'
            f'\n  Categories: {Category.objects.count()}'
            f'\n  Products: {Product.objects.count()}'
            f'\n  Ingredients: {Ingredient.objects.count()}'
        ))
