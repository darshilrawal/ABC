from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Populate database with sample products'

    def handle(self, *args, **options):
        # Clear existing products
        Product.objects.all().delete()
        
        products_data = [
            # Kurtis
            {
                'name': 'Elegant Floral Kurti',
                'description': 'Beautiful floral printed kurti with intricate embroidery. Perfect for casual and semi-formal occasions. Made with premium cotton blend fabric for comfort.',
                'category': 'kurtis',
                'min_order_quantity': 50,
                'price_range': '₹350 - ₹450',
                'fabric': 'Cotton Blend',
                'is_featured': True,
            },
            {
                'name': 'Traditional Embroidered Kurti',
                'description': 'Classic traditional kurti with heavy embroidery work. Ideal for festive occasions and celebrations. Available in multiple vibrant colors.',
                'category': 'kurtis',
                'min_order_quantity': 50,
                'price_range': '₹450 - ₹600',
                'fabric': 'Rayon',
                'is_featured': True,
            },
            {
                'name': 'Casual Cotton Kurti',
                'description': 'Comfortable and stylish everyday wear kurti. Breathable fabric perfect for daily use. Simple yet elegant design.',
                'category': 'kurtis',
                'min_order_quantity': 100,
                'price_range': '₹250 - ₹350',
                'fabric': 'Pure Cotton',
                'is_featured': False,
            },
            {
                'name': 'Designer Palazzo Kurti Set',
                'description': 'Trendy kurti with matching palazzo pants. Modern cuts and contemporary design. Perfect for young professionals.',
                'category': 'kurtis',
                'min_order_quantity': 50,
                'price_range': '₹550 - ₹700',
                'fabric': 'Georgette',
                'is_featured': True,
            },
            {
                'name': 'Printed A-Line Kurti',
                'description': 'Stylish A-line cut kurti with beautiful prints. Flattering silhouette for all body types. Comfortable and fashionable.',
                'category': 'kurtis',
                'min_order_quantity': 75,
                'price_range': '₹300 - ₹400',
                'fabric': 'Crepe',
                'is_featured': False,
            },
            {
                'name': 'Anarkali Style Kurti',
                'description': 'Elegant Anarkali style kurti with flair bottom. Perfect for special occasions and parties. Rich fabric with intricate details.',
                'category': 'kurtis',
                'min_order_quantity': 50,
                'price_range': '₹500 - ₹650',
                'fabric': 'Silk Blend',
                'is_featured': False,
            },
            
            # Short Kurtis
            {
                'name': 'Trendy Short Kurti',
                'description': 'Modern short kurti perfect for pairing with jeans or leggings. Trendy design with beautiful prints.',
                'category': 'short_kurtis',
                'min_order_quantity': 100,
                'price_range': '₹200 - ₹300',
                'fabric': 'Cotton',
                'is_featured': True,
            },
            {
                'name': 'Casual Short Kurti Top',
                'description': 'Versatile short kurti that works as a top. Perfect for college and casual outings. Available in vibrant colors.',
                'category': 'short_kurtis',
                'min_order_quantity': 100,
                'price_range': '₹180 - ₹250',
                'fabric': 'Cotton Blend',
                'is_featured': False,
            },
            {
                'name': 'Printed Short Kurti',
                'description': 'Beautiful printed short kurti with modern patterns. Comfortable fabric for all-day wear.',
                'category': 'short_kurtis',
                'min_order_quantity': 75,
                'price_range': '₹220 - ₹320',
                'fabric': 'Rayon',
                'is_featured': False,
            },
            {
                'name': 'Embroidered Short Kurti',
                'description': 'Short kurti with delicate embroidery work. Perfect blend of traditional and modern style.',
                'category': 'short_kurtis',
                'min_order_quantity': 50,
                'price_range': '₹300 - ₹400',
                'fabric': 'Chanderi',
                'is_featured': True,
            },
            {
                'name': 'Designer Short Kurti',
                'description': 'Contemporary designer short kurti with unique cuts and patterns. Stand out with this trendy piece.',
                'category': 'short_kurtis',
                'min_order_quantity': 50,
                'price_range': '₹350 - ₹450',
                'fabric': 'Georgette',
                'is_featured': False,
            },
            
            # Tops
            {
                'name': 'Classic Western Top',
                'description': 'Elegant western top suitable for office and casual wear. Modern design with comfortable fit.',
                'category': 'tops',
                'min_order_quantity': 100,
                'price_range': '₹200 - ₹300',
                'fabric': 'Polyester',
                'is_featured': True,
            },
            {
                'name': 'Floral Print Top',
                'description': 'Beautiful floral printed top for summer. Light and breathable fabric for comfort.',
                'category': 'tops',
                'min_order_quantity': 100,
                'price_range': '₹180 - ₹280',
                'fabric': 'Crepe',
                'is_featured': False,
            },
            {
                'name': 'Solid Color Formal Top',
                'description': 'Professional solid color top for office wear. Elegant design with quality stitching.',
                'category': 'tops',
                'min_order_quantity': 75,
                'price_range': '₹250 - ₹350',
                'fabric': 'Poly Crepe',
                'is_featured': False,
            },
            {
                'name': 'Trendy Crop Top',
                'description': 'Fashionable crop top for young fashion-forward customers. Modern cuts and trendy prints.',
                'category': 'tops',
                'min_order_quantity': 100,
                'price_range': '₹150 - ₹250',
                'fabric': 'Cotton Lycra',
                'is_featured': True,
            },
            {
                'name': 'Ruffle Sleeve Top',
                'description': 'Stylish top with ruffle sleeves. Perfect for parties and evening outings.',
                'category': 'tops',
                'min_order_quantity': 75,
                'price_range': '₹280 - ₹380',
                'fabric': 'Georgette',
                'is_featured': False,
            },
            {
                'name': 'Lace Detail Top',
                'description': 'Elegant top with beautiful lace detailing. Perfect for special occasions.',
                'category': 'tops',
                'min_order_quantity': 50,
                'price_range': '₹320 - ₹420',
                'fabric': 'Net & Crepe',
                'is_featured': False,
            },
            
            # Jeans
            {
                'name': 'Classic Skinny Jeans',
                'description': 'Timeless skinny fit jeans with comfortable stretch. High-quality denim that lasts long. Perfect for everyday wear.',
                'category': 'jeans',
                'min_order_quantity': 50,
                'price_range': '₹450 - ₹600',
                'fabric': 'Denim Stretch',
                'is_featured': True,
            },
            {
                'name': 'High Waist Jeans',
                'description': 'Trendy high waist jeans for a flattering fit. Comfortable and stylish for all occasions.',
                'category': 'jeans',
                'min_order_quantity': 50,
                'price_range': '₹500 - ₹650',
                'fabric': 'Premium Denim',
                'is_featured': True,
            },
            {
                'name': 'Ripped Style Jeans',
                'description': 'Fashionable ripped jeans for trendy customers. Perfect distressed look with quality construction.',
                'category': 'jeans',
                'min_order_quantity': 50,
                'price_range': '₹480 - ₹620',
                'fabric': 'Cotton Denim',
                'is_featured': False,
            },
            {
                'name': 'Straight Fit Jeans',
                'description': 'Classic straight fit jeans for comfortable wear. Versatile style for all age groups.',
                'category': 'jeans',
                'min_order_quantity': 75,
                'price_range': '₹400 - ₹550',
                'fabric': 'Denim',
                'is_featured': False,
            },
            {
                'name': 'Bootcut Jeans',
                'description': 'Stylish bootcut jeans with perfect flare. Retro style making a comeback. Quality denim construction.',
                'category': 'jeans',
                'min_order_quantity': 50,
                'price_range': '₹520 - ₹680',
                'fabric': 'Stretch Denim',
                'is_featured': False,
            },
            {
                'name': 'Mom Fit Jeans',
                'description': 'Comfortable mom fit jeans with relaxed silhouette. Trendy vintage-inspired style.',
                'category': 'jeans',
                'min_order_quantity': 50,
                'price_range': '₹480 - ₹600',
                'fabric': 'Cotton Denim',
                'is_featured': False,
            },
        ]
        
        for product_data in products_data:
            Product.objects.create(**product_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(products_data)} sample products')
        )
