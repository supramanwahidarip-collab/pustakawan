from datetime import datetime, timedelta
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.blueprints.librarian import librarian_bp
from app.utils.decorators import librarian_required
from app.models.loan import Loan
from flask_login import current_user

@librarian_bp.route('/dashboard')
@login_required
@librarian_required
def dashboard():
    # Halaman utama dashboard pustakawan (mengarahkan langsung ke manajemen sirkulasi/buku)
    return redirect(url_for('librarian.manage_loans'))

@librarian_bp.route('/loans')
@login_required
@librarian_required
def manage_loans():
    status_filter = request.args.get('status', 'ALL')
    loans_query = Loan.query

    if status_filter != 'ALL':
        loans_query = loans_query.filter_by(status=status_filter)

    loans = loans_query.order_by(Loan.request_date.desc()).all()
    return render_template('librarian/loans.html', loans=loans, active_status=status_filter)

@librarian_bp.route('/loans/<int:loan_id>/approve', methods=['POST'])
@login_required
@librarian_required
def approve_loan(loan_id):
    loan = db.session.get(Loan, loan_id)
    if not loan:
        flash('Data peminjaman tidak ditemukan.', 'danger')
        return redirect(url_for('librarian.manage_loans'))

    if loan.status != 'PENDING':
        flash('Peminjaman ini sudah diproses sebelumnya.', 'warning')
        return redirect(url_for('librarian.manage_loans'))

    book = loan.book
    if book.stock_available <= 0:
        flash(f'Stok buku "{book.title}" habis, persetujuan dibatalkan.', 'danger')
        return redirect(url_for('librarian.manage_loans'))

    # Kurangi stok tersedia & ubah status jadi BORROWED
    book.stock_available -= 1
    loan.status = 'BORROWED'
    loan.borrow_date = datetime.utcnow()
    # Tenggat waktu pengembalian otomatis 7 hari dari sekarang
    loan.due_date = datetime.utcnow() + timedelta(days=7)
    loan.librarian_id = current_user.id

    db.session.commit()
    flash(f'Peminjaman untuk "{book.title}" berhasil disetujui.', 'success')
    return redirect(url_for('librarian.manage_loans'))

@librarian_bp.route('/loans/<int:loan_id>/return', methods=['POST'])
@login_required
@librarian_required
def return_book(loan_id):
    loan = db.session.get(Loan, loan_id)
    if not loan:
        flash('Data peminjaman tidak ditemukan.', 'danger')
        return redirect(url_for('librarian.manage_loans'))

    if loan.status != 'BORROWED':
        flash('Buku ini tidak dalam status sedang dipinjam.', 'warning')
        return redirect(url_for('librarian.manage_loans'))

    book = loan.book
    # Kembalikan stok buku & ubah status jadi RETURNED
    book.stock_available += 1
    loan.status = 'RETURNED'
    loan.return_date = datetime.utcnow()

    db.session.commit()
    flash(f'Buku "{book.title}" telah dikembalikan dan stok diperbarui.', 'success')
    return redirect(url_for('librarian.manage_loans'))