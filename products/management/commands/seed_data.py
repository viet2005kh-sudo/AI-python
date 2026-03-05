"""
File: products/management/commands/seed_data.py

Hướng dẫn:
1. Tạo thư mục: products/management/commands/
2. Tạo file __init__.py trong products/management/
3. Tạo file __init__.py trong products/management/commands/
4. Tạo file seed_data.py trong products/management/commands/
5. Copy TOÀN BỘ code bên dưới vào file seed_data.py
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product, ProductImage
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('🌱 Bắt đầu seed dữ liệu...'))
        
        # Create superuser
        self.create_users()
        
        # Create categories
        self.create_categories()
        
        # Create products
        self.create_products()
        
        self.stdout.write(self.style.SUCCESS('✅ Hoàn tất seed dữ liệu!'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('📋 THÔNG TIN ĐĂNG NHẬP:'))
        self.stdout.write(self.style.SUCCESS('   Admin: admin@snackshop.vn / admin123'))
        self.stdout.write(self.style.SUCCESS('   User:  user@gmail.com / user123'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('🚀 Chạy server: python manage.py runserver'))

    def create_users(self):
        """Create sample users"""
        self.stdout.write('👤 Tạo users...')
        
        # Create admin
        if not User.objects.filter(email='admin@snackshop.vn').exists():
            User.objects.create_superuser(
                email='admin@snackshop.vn',
                password='123',
                full_name='Quản Trị Viên',
                phone='0901234567',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('   ✓ Tạo admin thành công'))
        
        # Create regular user
        if not User.objects.filter(email='user@gmail.com').exists():
            User.objects.create_user(
                email='user@gmail.com',
                password='user123',
                full_name='Nguyễn Văn A',
                phone='0912345678',
                address='123 Đường ABC, Quận 1, TP.HCM'
            )
            self.stdout.write(self.style.SUCCESS('   ✓ Tạo user thành công'))

    def create_categories(self):
        """Create sample categories"""
        self.stdout.write('📁 Tạo danh mục...')
        
        categories_data = [
            {'name': 'Snack khoai tây', 'icon': '🥔', 'display_order': 1},
            {'name': 'Kẹo & Chocolate', 'icon': '🍬', 'display_order': 2},
            {'name': 'Hạt dinh dưỡng', 'icon': '🥜', 'display_order': 3},
            {'name': 'Bánh quy', 'icon': '🍪', 'display_order': 4},
            {'name': 'Đồ ăn vặt Hàn Quốc', 'icon': '🇰🇷', 'display_order': 5},
            {'name': 'Hải sản khô', 'icon': '🦑', 'display_order': 6},
        ]
        
        for cat_data in categories_data:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'display_order': cat_data['display_order'],
                    'description': f'Các loại {cat_data["name"].lower()} chất lượng cao'
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'   ✓ Tạo {len(categories_data)} danh mục'))

    def create_products(self):
        """Create sample products"""
        self.stdout.write('🛍️  Tạo sản phẩm...')
        
        # Get categories
        cat_snack = Category.objects.get(name='Snack khoai tây')
        cat_candy = Category.objects.get(name='Kẹo & Chocolate')
        cat_nut = Category.objects.get(name='Hạt dinh dưỡng')
        cat_cookie = Category.objects.get(name='Bánh quy')
        cat_korea = Category.objects.get(name='Đồ ăn vặt Hàn Quốc')
        cat_seafood = Category.objects.get(name='Hải sản khô')
        
        products_data = [
            # Snack khoai tây
            {
                'category': cat_snack,
                'name': 'Snack Khoai Tây Poca Vị Tự Nhiên 52g',
                'description': 'Snack khoai tây giòn rụm, vị mặn nhẹ, được làm từ khoai tây tươi ngon. Thích hợp làm món ăn vặt cho cả gia đình.',
                'price': Decimal('8000'),
                'discount_price': Decimal('7000'),
                'stock_quantity': 500,
                'unit': 'gói',
                'weight_grams': 52,
                'is_featured': True,
            },
            {
                'category': cat_snack,
                'name': 'Lays Stax Kem Chua Hành Tây 110g',
                'description': 'Snack khoai tây xếp lớp hương vị đậm đà. Vị kem chua hành tây béo ngậy, thơm ngon.',
                'price': Decimal('35000'),
                'discount_price': Decimal('32000'),
                'stock_quantity': 200,
                'unit': 'hộp',
                'weight_grams': 110,
                'is_featured': False,
            },
            {
                'category': cat_snack,
                'name': 'Oishi Snack Bắp Cay 42g',
                'description': 'Snack bắp giòn tan với vị cay nồng đặc trưng. Được yêu thích bởi người ưa vị cay.',
                'price': Decimal('6000'),
                'stock_quantity': 300,
                'unit': 'gói',
                'weight_grams': 42,
                'is_featured': False,
            },
            
            # Kẹo & Chocolate
            {
                'category': cat_candy,
                'name': 'Kẹo Dẻo Gấu Haribo 80g',
                'description': 'Kẹo dẻo hình gấu nhiều màu sắc, vị trái cây tự nhiên. An toàn cho trẻ em.',
                'price': Decimal('25000'),
                'stock_quantity': 300,
                'unit': 'gói',
                'weight_grams': 80,
                'is_featured': True,
            },
            {
                'category': cat_candy,
                'name': 'Chocolate Dairy Milk 38g',
                'description': 'Socola sữa Cadbury thơm ngon, béo ngậy. Nhập khẩu chính hãng từ Anh.',
                'price': Decimal('15000'),
                'discount_price': Decimal('13000'),
                'stock_quantity': 400,
                'unit': 'thanh',
                'weight_grams': 38,
                'is_featured': False,
            },
            {
                'category': cat_candy,
                'name': 'Kẹo Bạc Hà Mentos 37.5g',
                'description': 'Kẹo bạc hà mát lạnh, giúp thơm miệng. Tiện lợi mang theo.',
                'price': Decimal('12000'),
                'stock_quantity': 250,
                'unit': 'hộp',
                'weight_grams': 37,
                'is_featured': False,
            },
            
            # Hạt dinh dưỡng
            {
                'category': cat_nut,
                'name': 'Hạt Điều Rang Muối 100g',
                'description': 'Hạt điều rang giòn vị muối nhẹ. Nguồn cung cấp protein và chất béo tốt.',
                'price': Decimal('45000'),
                'discount_price': Decimal('42000'),
                'stock_quantity': 150,
                'unit': 'gói',
                'weight_grams': 100,
                'is_featured': True,
            },
            {
                'category': cat_nut,
                'name': 'Hạnh Nhân Mỹ 200g',
                'description': 'Hạnh nhân nhập khẩu Mỹ, giàu vitamin E, tốt cho sức khỏe tim mạch.',
                'price': Decimal('85000'),
                'stock_quantity': 100,
                'unit': 'hộp',
                'weight_grams': 200,
                'is_featured': False,
            },
            {
                'category': cat_nut,
                'name': 'Hạt Macca Úc 150g',
                'description': 'Hạt macca rang bơ thơm ngon, bổ dưỡng. Nhập khẩu từ Úc.',
                'price': Decimal('120000'),
                'discount_price': Decimal('110000'),
                'stock_quantity': 80,
                'unit': 'hộp',
                'weight_grams': 150,
                'is_featured': True,
            },
            
            # Bánh quy
            {
                'category': cat_cookie,
                'name': 'Bánh Quy Bơ Danisa 454g',
                'description': 'Bánh quy bơ Đan Mạch hộp thiếc sang trọng. Vị bơ thơm béo, giòn tan.',
                'price': Decimal('120000'),
                'discount_price': Decimal('110000'),
                'stock_quantity': 80,
                'unit': 'hộp',
                'weight_grams': 454,
                'is_featured': False,
            },
            {
                'category': cat_cookie,
                'name': 'Bánh Oreo Vani 137g',
                'description': 'Bánh quy Oreo sandwich với nhân kem vani ngọt ngào. Thương hiệu nổi tiếng toàn cầu.',
                'price': Decimal('25000'),
                'stock_quantity': 200,
                'unit': 'gói',
                'weight_grams': 137,
                'is_featured': False,
            },
            
            # Đồ ăn vặt Hàn Quốc
            {
                'category': cat_korea,
                'name': 'Bánh Tráng Trộn Tây Ninh 200g',
                'description': 'Bánh tráng trộn gia vị đặc biệt, vị cay ngọt đậm đà. Đặc sản Việt Nam.',
                'price': Decimal('35000'),
                'discount_price': Decimal('30000'),
                'stock_quantity': 250,
                'unit': 'gói',
                'weight_grams': 200,
                'is_featured': True,
            },
            {
                'category': cat_korea,
                'name': 'Rong Biển Vị BBQ Hàn Quốc 4g',
                'description': 'Snack rong biển vị thịt nướng BBQ, giòn tan, ít calo. Nhập khẩu Hàn Quốc.',
                'price': Decimal('18000'),
                'stock_quantity': 350,
                'unit': 'gói',
                'weight_grams': 4,
                'is_featured': False,
            },
            {
                'category': cat_korea,
                'name': 'Bánh Gạo Tokbokki 150g',
                'description': 'Bánh gạo cay Hàn Quốc, vị cay ngọt đặc trưng. Ăn liền tiện lợi.',
                'price': Decimal('28000'),
                'stock_quantity': 180,
                'unit': 'gói',
                'weight_grams': 150,
                'is_featured': False,
            },
            
            # Hải sản khô
            {
                'category': cat_seafood,
                'name': 'Mực Tẩm Gia Vị 100g',
                'description': 'Mực tẩm vị cay ngọt, dai giòn thơm ngon. Đặc sản Nha Trang.',
                'price': Decimal('55000'),
                'discount_price': Decimal('50000'),
                'stock_quantity': 120,
                'unit': 'gói',
                'weight_grams': 100,
                'is_featured': True,
            },
            {
                'category': cat_seafood,
                'name': 'Khô Cá Lóc 200g',
                'description': 'Khô cá lóc một nắng Cà Mau, thịt dai ngọt. Nguồn protein phong phú.',
                'price': Decimal('75000'),
                'stock_quantity': 90,
                'unit': 'gói',
                'weight_grams': 200,
                'is_featured': False,
            },
        ]
        
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
                # Set sold_count for demo
                product.sold_count = 50 if product.is_featured else 20
                product.save()
        
        self.stdout.write(self.style.SUCCESS(f'   ✓ Tạo {created_count} sản phẩm mới'))
        self.stdout.write(self.style.WARNING(f'   ℹ {len(products_data) - created_count} sản phẩm đã tồn tại'))