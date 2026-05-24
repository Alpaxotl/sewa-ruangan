"""
Sistem Sewa Ruangan Kelas
"""

reservations = {}  # { "nama_ruangan": { "slot": "nama_penyewa" } }

ROOMS = ["R101", "R102", "R103"]
SLOTS = ["08:00", "10:00", "12:00", "14:00", "16:00"]


def book_room(room, slot, name):
    """Pesan ruangan untuk slot tertentu."""
    if room not in ROOMS:
        raise ValueError(f"Ruangan {room} tidak tersedia")
    if slot not in SLOTS:
        raise ValueError(f"Slot {slot} tidak valid")
    if not name or not name.strip():
        raise ValueError("Nama penyewa tidak boleh kosong")

    if room not in reservations:
        reservations[room] = {}

    if slot in reservations[room]:
        raise RuntimeError(f"{room} pada slot {slot} sudah dipesan")

    reservations[room][slot] = name.strip()
    return True


def cancel_booking(room, slot):
    """Batalkan pemesanan ruangan."""
    if room not in reservations or slot not in reservations.get(room, {}):
        raise RuntimeError("Pemesanan tidak ditemukan")
    del reservations[room][slot]
    return True


def is_available(room, slot):
    """Cek apakah ruangan tersedia di slot tertentu."""
    return slot not in reservations.get(room, {})


def get_bookings(room):
    """Dapatkan semua pemesanan untuk satu ruangan."""
    return reservations.get(room, {})


def get_all_available_slots(room):
    """Dapatkan semua slot yang masih kosong untuk satu ruangan."""
    booked = reservations.get(room, {})
    return [s for s in SLOTS if s not in booked]


def reset():
    """Reset semua data (untuk keperluan testing)."""
    reservations.clear()
