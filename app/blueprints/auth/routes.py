from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.blueprints.auth import auth_bp


@auth_bp.route('/')
def index():
    """Gerbang utama: Mengarahkan user sesuai status login dan role-nya."""
    if current_user.is_authenticated:
        if current_user.is_librarian:
            return redirect(url_for('librarian.dashboard'))
        return redirect(url_for('member.catalog'))  # Diarahkan ke katalog anggota
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')
        remember = True if request.form.get('remember') else False

        # Bisa login menggunakan Username atau Email
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()

        if not user or not user.check_password(password):
            flash('Username/Email atau kata sandi yang Anda masukkan salah.', 'danger')
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash('Akun Anda sedang dinonaktifkan. Hubungi Pustakawan.', 'warning')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        flash(f'Selamat datang kembali, {user.full_name}!', 'success')

        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        return redirect(url_for('auth.index'))

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validasi dasar
        if password != confirm_password:
            flash('Konfirmasi kata sandi tidak cocok.', 'danger')
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash('Kata sandi minimal harus 6 karakter.', 'warning')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan, silakan pilih yang lain.', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Alamat email sudah terdaftar.', 'danger')
            return redirect(url_for('auth.register'))

        # Generate Kode Anggota Otomatis (Contoh: MBR-2026-003)
        member_count = User.query.filter_by(role='member').count() + 1
        member_code = f"MBR-{datetime.utcnow().year}-{member_count:03d}"

        new_member = User(
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            member_id_code=member_code,
            role='member'
        )
        new_member.set_password(password)

        db.session.add(new_member)
        db.session.commit()

        flash(f'Registrasi berhasil dengan ID {member_code}! Silakan masuk.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Anda telah berhasil keluar dari sistem.', 'info')
    return redirect(url_for('auth.login'))


# --- RUTE LANDING SEMENTARA UNTUK VERIFIKASI FASE 2 ---
# (Akan digantikan oleh Dashboard penuh di Fase 3 dan Fase 4)

@auth_bp.route('/librarian-portal')
@login_required
def librarian_preview():
    if not current_user.is_librarian:
        return redirect(url_for('auth.member_preview'))
    return render_template('auth/role_landing.html', portal_title="Portal Pustakawan (Librarian)")


@auth_bp.route('/member-portal')
@login_required
def member_preview():
    if current_user.is_librarian:
        return redirect(url_for('auth.librarian_preview'))
    return render_template('auth/role_landing.html', portal_title="Portal Anggota (Member)")