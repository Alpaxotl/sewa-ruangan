"""
Unit Test & Feature Test — Sistem Sewa Ruangan Kelas
Week 10-11 | IS Testing & Implementation | UNDIKSHA
"""

import pytest
from sewa_ruangan import book_room, cancel_booking, is_available, get_bookings, get_all_available_slots, reset


# Reset data sebelum setiap test agar tidak saling mempengaruhi
@pytest.fixture(autouse=True)
def bersihkan_data():
    reset()


# ─────────────────────────────────────────────────────────────
# UNIT TEST — Fungsi book_room
# ─────────────────────────────────────────────────────────────

def test_pesan_ruangan_berhasil():
    assert book_room("R101", "08:00", "Budi") == True

def test_pesan_ruangan_tidak_valid():
    with pytest.raises(ValueError, match="tidak tersedia"):
        book_room("R999", "08:00", "Budi")

def test_pesan_slot_tidak_valid():
    with pytest.raises(ValueError, match="tidak valid"):
        book_room("R101", "07:00", "Budi")

def test_pesan_nama_kosong():
    with pytest.raises(ValueError, match="kosong"):
        book_room("R101", "08:00", "")

def test_pesan_slot_sudah_diisi():
    book_room("R101", "08:00", "Budi")
    with pytest.raises(RuntimeError, match="sudah dipesan"):
        book_room("R101", "08:00", "Sari")


# ─────────────────────────────────────────────────────────────
# UNIT TEST — Cek ketersediaan & daftar slot
# ─────────────────────────────────────────────────────────────

def test_slot_tersedia_sebelum_dipesan():
    assert is_available("R101", "10:00") == True

def test_slot_tidak_tersedia_setelah_dipesan():
    book_room("R101", "10:00", "Komang")
    assert is_available("R101", "10:00") == False

def test_semua_slot_kosong_awalnya():
    slots = get_all_available_slots("R101")
    assert len(slots) == 5

def test_slot_berkurang_setelah_dipesan():
    book_room("R101", "08:00", "Budi")
    book_room("R101", "10:00", "Sari")
    slots = get_all_available_slots("R101")
    assert len(slots) == 3
    assert "08:00" not in slots


# ─────────────────────────────────────────────────────────────
# UNIT TEST — Pembatalan
# ─────────────────────────────────────────────────────────────

def test_batal_pemesanan_berhasil():
    book_room("R102", "12:00", "Wayan")
    assert cancel_booking("R102", "12:00") == True

def test_slot_kembali_tersedia_setelah_dibatalkan():
    book_room("R102", "12:00", "Wayan")
    cancel_booking("R102", "12:00")
    assert is_available("R102", "12:00") == True

def test_batal_pemesanan_tidak_ada():
    with pytest.raises(RuntimeError, match="tidak ditemukan"):
        cancel_booking("R101", "08:00")


# ─────────────────────────────────────────────────────────────
# UNIT TEST — Parametrize: berbagai ruangan & slot
# ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("room,slot,name", [
    ("R101", "08:00", "Budi"),
    ("R102", "10:00", "Sari"),
    ("R103", "14:00", "Komang"),
    ("R101", "16:00", "Wayan"),
])
def test_pesan_berbagai_ruangan_dan_slot(room, slot, name):
    assert book_room(room, slot, name) == True
    assert is_available(room, slot) == False


# ─────────────────────────────────────────────────────────────
# FEATURE TEST — Alur lengkap: pesan → cek → batal → pesan lagi
# ─────────────────────────────────────────────────────────────

def test_alur_pesan_dan_lihat_daftar():
    book_room("R101", "08:00", "Budi")
    book_room("R101", "10:00", "Sari")
    daftar = get_bookings("R101")
    assert daftar["08:00"] == "Budi"
    assert daftar["10:00"] == "Sari"

def test_alur_batal_dan_pesan_ulang():
    book_room("R103", "14:00", "Komang")
    cancel_booking("R103", "14:00")
    # Slot yang dibatalkan bisa dipesan orang lain
    assert book_room("R103", "14:00", "Gede") == True

def test_dua_ruangan_slot_sama_tidak_konflik():
    # R101 dan R102 bisa dipesan di slot yang sama oleh orang berbeda
    book_room("R101", "08:00", "Budi")
    book_room("R102", "08:00", "Sari")
    assert is_available("R101", "08:00") == False
    assert is_available("R102", "08:00") == False

def test_ruangan_berbeda_tidak_saling_mempengaruhi():
    book_room("R101", "08:00", "Budi")
    # R102 di slot yang sama tetap kosong
    assert is_available("R102", "08:00") == True

@pytest.mark.skip(reason="Fitur notifikasi email belum diimplementasikan")
def test_notifikasi_email_setelah_pesan():
    pass
