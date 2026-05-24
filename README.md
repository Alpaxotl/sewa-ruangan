# Sistem Sewa Ruangan Kelas
**IS Testing & Implementation — Week 10-11 | UNDIKSHA**

## Cara Jalankan Test

```bash
pip install pytest
python -m pytest test_sewa_ruangan.py -v
```

## Fitur yang Diuji

- Pesan ruangan (`book_room`)
- Cek ketersediaan (`is_available`, `get_all_available_slots`)
- Lihat daftar pemesanan (`get_bookings`)
- Batalkan pemesanan (`cancel_booking`)

## Teknik Pytest

| Teknik | Digunakan Untuk |
|---|---|
| `@pytest.fixture(autouse=True)` | Reset data sebelum tiap test |
| `pytest.raises` | Uji error (ruangan tidak ada, slot penuh, dll) |
| `@pytest.mark.parametrize` | Test berbagai kombinasi ruangan & slot |
| `@pytest.mark.skip` | Fitur notifikasi email belum dibuat |
