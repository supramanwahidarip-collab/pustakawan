from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Category, Book, Loan

app = create_app()


def seed_database():
    with app.app_context():
        print("Mereset dan membangun skema database...")
        db.drop_all()
        db.create_all()

        # 1. Buat Akun Pustakawan & Peminjam
        librarian = User(
            username='admin_pustaka',
            email='pustakawan@toscalib.id',
            full_name='Budi Santoso, S.IIP.',
            member_id_code='LIB-2026-01',
            role='librarian',
            phone='081234567890'
        )
        librarian.set_password('Admin123!')

        member1 = User(
            username='arip_dev',
            email='arip@student.id',
            full_name='Arip Supraman',
            member_id_code='MBR-2026-001',
            role='member',
            phone='081298765432'
        )
        member1.set_password('Member123!')

        member2 = User(
            username='nadia_putri',
            email='nadia@student.id',
            full_name='Nadia Putri Maharani',
            member_id_code='MBR-2026-002',
            role='member',
            phone='081355556666'
        )
        member2.set_password('Member123!')

        db.session.add_all([librarian, member1, member2])
        db.session.commit()

        # 2. Buat Kategori Buku
        cat_se = Category(name='Rekayasa Perangkat Lunak', slug='rekayasa-perangkat-lunak',
                          description='Arsitektur sistem, pemrograman, dan algoritma.')
        cat_ai = Category(name='Sains Data & AI', slug='sains-data-ai',
                          description='Machine learning, statistik, dan pengolahan data.')
        cat_biz = Category(name='Manajemen & Bisnis Digital', slug='manajemen-bisnis',
                           description='Strategi produk, startup, dan rekayasa industri.')
        cat_des = Category(name='Desain UI/UX & Produk', slug='desain-ui-ux',
                           description='Interaksi manusia-komputer dan sistem desain.')

        db.session.add_all([cat_se, cat_ai, cat_biz, cat_des])
        db.session.commit()

        # 3. Buat Katalog Buku
        books_data = [
            Book(
                isbn='978-0132350884',
                title='Clean Architecture: A Craftsman Guide to Software Structure',
                author='Robert C. Martin',
                publisher='Prentice Hall',
                publish_year=2017,
                category_id=cat_se.id,
                shelf_location='RAK-A1',
                stock_total=5,
                stock_available=4,
                synopsis='Panduan mendalam merancang arsitektur perangkat lunak yang tangguh, modular, dan mudah dipelihara jangka panjang.'
            ),
            Book(
                isbn='978-1492052203',
                title='Architecture Patterns with Python',
                author='Harry Percival & Bob Gregory',
                publisher='O’Reilly Media',
                publish_year=2020,
                category_id=cat_se.id,
                shelf_location='RAK-A2',
                stock_total=4,
                stock_available=3,
                synopsis='Penerapan Domain-Driven Design, Event-Driven Architecture, dan Service Layer menggunakan ekosistem Python modern.'
            ),
            Book(
                isbn='978-1449373320',
                title='Designing Data-Intensive Applications',
                author='Martin Kleppmann',
                publisher='O’Reilly Media',
                publish_year=2017,
                category_id=cat_ai.id,
                shelf_location='RAK-B1',
                stock_total=3,
                stock_available=3,
                synopsis='Membahas konsep fundamental database relasional, NoSQL, skalabilitas, konsistensi, dan keandalan sistem terdistribusi.'
            ),
            Book(
                isbn='978-0465050659',
                title='The Design of Everyday Things',
                author='Don Norman',
                publisher='Basic Books',
                publish_year=2013,
                category_id=cat_des.id,
                shelf_location='RAK-C1',
                stock_total=6,
                stock_available=6,
                synopsis='Buku klasik wajib tentang psikologi desain antarmuka agar produk intuitif dan ramah pengguna.'
            ),
            Book(
                isbn='978-0307887894',
                title='The Lean Startup: How Constant Innovation Creates Radically Successful Businesses',
                author='Eric Ries',
                publisher='Crown Business',
                publish_year=2011,
                category_id=cat_biz.id,
                shelf_location='RAK-D2',
                stock_total=4,
                stock_available=4,
                synopsis='Pendekatan ilmiah dalam membangun produk digital dan mengukur validasi pasar secara efisien.'
            )
        ]
        db.session.add_all(books_data)
        db.session.commit()

        # 4. Buat Sampel Transaksi Peminjaman (Aktif, Terlambat, dan Menunggu Persetujuan)
        now = datetime.utcnow()

        # Peminjaman 1: Sedang dipinjam normal
        loan1 = Loan(
            loan_code='TRX-202611-001',
            user_id=member1.id,
            book_id=books_data[0].id,
            request_date=now - timedelta(days=3),
            borrow_date=now - timedelta(days=3),
            due_date=now + timedelta(days=4),
            status='BORROWED',
            notes='Buku diambil dalam kondisi sampul baru.'
        )

        # Peminjaman 2: Terlambat 3 hari (untuk menguji fitur denda otomatis)
        loan2 = Loan(
            loan_code='TRX-202610-089',
            user_id=member2.id,
            book_id=books_data[1].id,
            request_date=now - timedelta(days=10),
            borrow_date=now - timedelta(days=10),
            due_date=now - timedelta(days=3),
            status='BORROWED',
            notes='Peminjaman untuk referensi tugas akhir.'
        )

        # Peminjaman 3: Baru diajukan (PENDING)
        loan3 = Loan(
            loan_code='TRX-202611-002',
            user_id=member1.id,
            book_id=books_data[2].id,
            request_date=now - timedelta(hours=2),
            status='PENDING',
            notes='Mohon disiapkan untuk pengambilan sore ini.'
        )

        db.session.add_all([loan1, loan2, loan3])
        db.session.commit()

        print("=====================================================")
        print("✅ Seeding Database Selesai!")
        print("Akun Pustakawan : admin_pustaka / Admin123!")
        print("Akun Peminjam 1 : arip_dev      / Member123!")
        print("Akun Peminjam 2 : nadia_putri   / Member123!")
        print("=====================================================")


if __name__ == '__main__':
    seed_database()