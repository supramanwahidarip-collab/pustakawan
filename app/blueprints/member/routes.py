from datetime import datetime
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.blueprints.member import member_bp
from app.utils.decorators import member_required
from app.models.book import Book, Category
from app.models.loan import Loan


@member_bp.route('/catalog')
@login_required
@member_required
def catalog():
    # Fitur pencarian dan filter kategori
    search_query = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)

    books_query = Book.query

    if search_query:
        books_query = books_query.filter(
            (Book.title.ilike(f'%{search_query}%')) |
            (Book.author.ilike(f'%{search_query}%'))
        )

    if category_id:
        books_query = books_query.filter_by(category_id=category_id)

    books = books_query.order_by(Book.title).all()
    categories = Category.query.all()

    return render_template('member/catalog.html',
                           books=books,
                           categories=categories,
                           search_query=search_query,
                           selected_category=category_id)


@member_bp.route('/books/<int:book_id>/borrow', methods=['POST'])
@login_required
@member_required
def request_borrow(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        flash('Buku tidak ditemukan.', 'danger')
        return redirect(url_for('member.catalog'))

    if book.stock_available <= 0:
        flash(f'Maaf, stok buku "{book.title}" sedang habis.', 'warning')
        return redirect(url_for('member.catalog'))

    # Cek apakah anggota sudah mencapai batas maksimal pinjam (maks 3 buku aktif)
    active_loans_count = current_user.loans.filter(Loan.status.in_(['PENDING', 'BORROWED', 'OVERDUE'])).count()
    if active_loans_count >= 3:
        flash('Anda telah mencapai batas maksimal peminjaman aktif (3 buku).', 'warning')
        return redirect(url_for('member.catalog'))

    # Buat kode transaksi unik
    import random
    loan_code = f"TRX-{datetime.utcnow().strftime('%Y%m%d')}-{random.randint(100, 999)}"

    new_loan = Loan(
        loan_code=loan_code,
        user_id=current_user.id,
        book_id=book.id,
        status='PENDING',
    )

    db.session.add(new_loan)
    db.session.commit()

    flash(f'Pengajuan pinjam untuk buku "{book.title}" berhasil dikirim! Menunggu validasi pustakawan.', 'success')
    return redirect(url_for('member.my_loans'))


@member_bp.route('/my-loans')
@login_required
@member_required
def my_loans():
    loans = current_user.loans.order_by(Loan.request_date.desc()).all()
    return render_template('member/my_loans.html', loans=loans)