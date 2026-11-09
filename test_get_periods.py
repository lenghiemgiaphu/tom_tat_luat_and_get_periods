"""Kiểm thử get_periods. Chạy: python -m unittest test_get_periods -v

Cần calendar.csv: đặt cạnh file này, hoặc trỏ bằng biến môi trường DATAMATE_CALENDAR.
Các ví dụ lấy từ rulebook §2 (15/10 → 01–15/09; 31/03 → cả tháng 2; tuần T2–CN; Tết).
Ngày Tết kiểm chéo độc lập với lịch âm thực tế (mùng 1 Tết: 10/02/2024, 29/01/2025,
17/02/2026, 06/02/2027).
"""
import os
import unittest
from datetime import date, datetime

import pandas as pd

import get_periods as gp


def D(s):
    return pd.Timestamp(s)


def P(a, b):
    return (D(a), D(b))


def _find_calendar():
    for p in (
        os.environ.get("DATAMATE_CALENDAR"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendar.csv"),
        "/mnt/user-data/uploads/calendar.csv",
    ):
        if p and os.path.exists(p):
            return pd.read_csv(p)
    return None


CAL = _find_calendar()


class TestBasicPeriods(unittest.TestCase):
    def test_hom_nay_hom_qua(self):
        p = gp.get_periods("2026-03-01")
        self.assertEqual(p["hom_nay"], P("2026-03-01", "2026-03-01"))
        self.assertEqual(p["hom_qua"], P("2026-02-28", "2026-02-28"))  # qua ranh giới tháng
        p = gp.get_periods("2026-01-01")
        self.assertEqual(p["hom_qua"], P("2025-12-31", "2025-12-31"))  # qua ranh giới năm

    def test_as_of_nhieu_kieu(self):
        want = gp.get_periods("2026-03-04")
        for x in (date(2026, 3, 4), datetime(2026, 3, 4, 23, 59), pd.Timestamp("2026-03-04 15:30")):
            self.assertEqual(gp.get_periods(x), want)

    def test_tuan_giua_tuan(self):  # 2026-03-04 là thứ Tư
        p = gp.get_periods("2026-03-04")
        self.assertEqual(p["tuan_nay"], P("2026-03-02", "2026-03-04"))
        self.assertEqual(p["tuan_truoc"], P("2026-02-23", "2026-03-01"))

    def test_tuan_thu_hai(self):  # 2026-11-09 là thứ Hai
        p = gp.get_periods("2026-11-09")
        self.assertEqual(p["tuan_nay"], P("2026-11-09", "2026-11-09"))
        self.assertEqual(p["tuan_truoc"], P("2026-11-02", "2026-11-08"))

    def test_tuan_chu_nhat(self):  # 2026-11-08 là Chủ nhật: vẫn thuộc tuần bắt đầu 11-02
        p = gp.get_periods("2026-11-08")
        self.assertEqual(p["tuan_nay"], P("2026-11-02", "2026-11-08"))
        self.assertEqual(p["tuan_truoc"], P("2026-10-26", "2026-11-01"))

    def test_thang_nay_so_voi_thang_truoc_cung_so_ngay(self):
        p = gp.get_periods("2026-10-15")  # ví dụ rulebook
        self.assertEqual(p["thang_nay"], P("2026-10-01", "2026-10-15"))
        self.assertEqual(p["thang_truoc_cung_so_ngay"], P("2026-09-01", "2026-09-15"))
        self.assertEqual(p["thang_truoc"], P("2026-09-01", "2026-09-30"))

    def test_31_03_so_voi_ca_thang_2(self):  # ví dụ rulebook
        p = gp.get_periods("2026-03-31")
        self.assertEqual(p["thang_truoc_cung_so_ngay"], P("2026-02-01", "2026-02-28"))
        p = gp.get_periods("2028-03-31")  # năm nhuận
        self.assertEqual(p["thang_truoc_cung_so_ngay"], P("2028-02-01", "2028-02-29"))

    def test_30_04_dung_chu_rulebook(self):
        # "ngày trùng số với hôm nay": 30/04 → 01–30/03 (không phải cả tháng 3)
        p = gp.get_periods("2026-04-30")
        self.assertEqual(p["thang_truoc_cung_so_ngay"], P("2026-03-01", "2026-03-30"))

    def test_dau_thang_dau_nam(self):
        p = gp.get_periods("2026-01-01")
        self.assertEqual(p["thang_nay"], P("2026-01-01", "2026-01-01"))
        self.assertEqual(p["thang_truoc"], P("2025-12-01", "2025-12-31"))
        self.assertEqual(p["thang_truoc_cung_so_ngay"], P("2025-12-01", "2025-12-01"))
        self.assertEqual(p["dau_nam"], P("2026-01-01", "2026-01-01"))
        p = gp.get_periods("2026-11-09")
        self.assertEqual(p["dau_nam"], P("2026-01-01", "2026-11-09"))

    def test_last_n_days(self):
        self.assertEqual(gp.last_n_days(7, "2026-11-09"), P("2026-11-03", "2026-11-09"))
        self.assertEqual(gp.last_n_days(1, "2026-11-09"), P("2026-11-09", "2026-11-09"))
        self.assertEqual(gp.last_n_days(30, "2026-03-04"), P("2026-02-03", "2026-03-04"))
        with self.assertRaises(ValueError):
            gp.last_n_days(0, "2026-11-09")

    def test_previous_period_same_length(self):
        self.assertEqual(
            gp.previous_period_same_length(P("2026-03-02", "2026-03-04")), P("2026-02-27", "2026-03-01")
        )


class TestMonthQuarter(unittest.TestCase):
    def test_thang_co_nam(self):
        self.assertEqual(gp.month_period(6, 2025), P("2025-06-01", "2025-06-30"))
        self.assertEqual(gp.month_period(2, 2024), P("2024-02-01", "2024-02-29"))
        self.assertEqual(gp.month_period(2, 2025), P("2025-02-01", "2025-02-28"))
        with self.assertRaises(ValueError):
            gp.month_period(13, 2025)

    def test_thang_khong_ghi_nam(self):
        t = "2026-11-09"
        self.assertEqual(gp.month_period(10, as_of_date=t), P("2026-10-01", "2026-10-31"))
        self.assertEqual(gp.month_period(11, as_of_date=t), P("2026-11-01", "2026-11-30"))  # tháng hiện tại
        self.assertEqual(gp.month_period(12, as_of_date=t), P("2025-12-01", "2025-12-31"))  # sau hôm nay → năm trước
        self.assertEqual(gp.month_period(1, as_of_date="2026-01-15"), P("2026-01-01", "2026-01-31"))
        self.assertEqual(gp.month_period(2, as_of_date="2026-01-15"), P("2025-02-01", "2025-02-28"))
        with self.assertRaises(ValueError):
            gp.month_period(6)

    def test_prev_month(self):
        self.assertEqual(gp.prev_month_period(1, 2026), P("2025-12-01", "2025-12-31"))
        self.assertEqual(gp.prev_month_period(3, 2024), P("2024-02-01", "2024-02-29"))

    def test_quy(self):
        self.assertEqual(gp.quarter_period(1, 2025), P("2025-01-01", "2025-03-31"))
        self.assertEqual(gp.quarter_period(2, 2025), P("2025-04-01", "2025-06-30"))
        self.assertEqual(gp.quarter_period(3, 2025), P("2025-07-01", "2025-09-30"))
        self.assertEqual(gp.quarter_period(4, 2025), P("2025-10-01", "2025-12-31"))
        with self.assertRaises(ValueError):
            gp.quarter_period(5, 2025)

    def test_quy_khong_ghi_nam(self):
        self.assertEqual(gp.quarter_period(1, as_of_date="2026-02-10"), P("2026-01-01", "2026-03-31"))
        self.assertEqual(gp.quarter_period(2, as_of_date="2026-02-10"), P("2025-04-01", "2025-06-30"))
        self.assertEqual(gp.quarter_period(4, as_of_date="2026-11-09"), P("2026-10-01", "2026-12-31"))
        self.assertEqual(gp.quarter_period(3, as_of_date="2026-11-09"), P("2026-07-01", "2026-09-30"))

    def test_prev_quarter(self):
        self.assertEqual(gp.prev_quarter_period(1, 2026), P("2025-10-01", "2025-12-31"))
        self.assertEqual(gp.prev_quarter_period(3, 2025), P("2025-04-01", "2025-06-30"))


@unittest.skipIf(CAL is None, "không tìm thấy calendar.csv (đặt DATAMATE_CALENDAR)")
class TestTet(unittest.TestCase):
    def test_calendar_weekday_convention(self):
        # 1 = thứ Hai ... 7 = Chủ nhật, khớp isoweekday cho cả file
        iso_wd = pd.to_datetime(CAL["date"]).dt.dayofweek + 1
        self.assertTrue((iso_wd == CAL["weekday"]).all())

    def test_tet_theo_lich_am(self):
        self.assertEqual(gp.tet_period(2024, CAL), P("2024-02-02", "2024-02-19"))
        self.assertEqual(gp.tet_period(2025, CAL), P("2025-01-22", "2025-02-07"))
        self.assertEqual(gp.tet_period(2026, CAL), P("2026-02-10", "2026-02-26"))
        self.assertEqual(gp.tet_period(2027, CAL), P("2027-01-30", "2027-02-15"))

    def test_truoc_tet_cung_so_ngay(self):
        # Tết 2024 dài 18 ngày, Tết 2025 dài 17 ngày
        self.assertEqual(gp.before_tet_period(2024, CAL), P("2024-01-15", "2024-02-01"))
        self.assertEqual(gp.before_tet_period(2025, CAL), P("2025-01-05", "2025-01-21"))
        for y in (2024, 2025, 2026, 2027):
            s, e = gp.tet_period(y, CAL)
            bs, be = gp.before_tet_period(y, CAL)
            self.assertEqual((be - bs).days, (e - s).days)
            self.assertEqual(be, s - pd.Timedelta(days=1))

    def test_tet_ngoai_pham_vi_bao_loi_ro(self):
        for y in (2023, 2030):
            with self.assertRaises(gp.CalendarError) as cm:
                gp.tet_period(y, CAL)
            self.assertIn("calendar", str(cm.exception))

    def test_get_periods_co_tet(self):
        p = gp.get_periods("2026-11-09", CAL)
        self.assertEqual(p["tet_nam_nay"], P("2026-02-10", "2026-02-26"))
        self.assertEqual(p["truoc_tet_nam_nay"], P("2026-01-24", "2026-02-09"))

    def test_get_periods_khong_vo_khi_calendar_thieu_nam(self):
        p = gp.get_periods("2030-05-05", CAL)
        self.assertNotIn("tet_nam_nay", p)
        self.assertIn("thang_nay", p)


class TestTetSynthetic(unittest.TestCase):
    """Calendar giả: tháng Chạp nhuận + lunar_leap dạng chuỗi."""

    def _cal(self, leap_as_text):
        rows = [
            # 23/12 nhuận (phải bị bỏ qua) và 23/12 thường
            ("2024-01-10", 23, 12, 2023, True),
            ("2024-02-02", 23, 12, 2023, False),
            ("2024-02-19", 10, 1, 2024, False),
            ("2024-03-19", 10, 1, 2024, True),  # mùng 10 tháng Giêng nhuận giả
        ]
        df = pd.DataFrame(rows, columns=["date", "lunar_day", "lunar_month", "lunar_year", "lunar_leap"])
        if leap_as_text:
            df["lunar_leap"] = df["lunar_leap"].map({True: "true", False: "false"})
        return df

    def test_bo_qua_thang_nhuan(self):
        for text in (False, True):
            self.assertEqual(gp.tet_period(2024, self._cal(text)), P("2024-02-02", "2024-02-19"))

    def test_thieu_cot(self):
        with self.assertRaises(gp.CalendarError):
            gp.tet_period(2024, self._cal(False).drop(columns=["lunar_leap"]))

    def test_trung_lap_bao_loi(self):
        df = pd.concat([self._cal(False), self._cal(False).iloc[[1]]], ignore_index=True)
        with self.assertRaises(gp.CalendarError):
            gp.tet_period(2024, df)


class TestFilters(unittest.TestCase):
    def test_in_period_gom_ca_ngay_cuoi(self):
        s = pd.Series(
            ["2026-03-03 23:59:59", "2026-03-04 00:00:00", "2026-03-04 15:30:00", "2026-03-04 23:59:59", "2026-03-05 00:00:00"]
        )
        m = gp.in_period(s, P("2026-03-04", "2026-03-04"))
        self.assertEqual(m.tolist(), [False, True, True, True, False])

    def test_in_period_cot_chi_co_ngay(self):
        m = gp.in_period(pd.Series(["2026-03-01", "2026-03-31", "2026-04-01"]), P("2026-03-01", "2026-03-31"))
        self.assertEqual(m.tolist(), [True, True, False])

    def test_in_shift_bien(self):
        s = pd.Series(
            ["2026-03-04 05:59", "2026-03-04 06:00", "2026-03-04 13:59", "2026-03-04 14:00", "2026-03-04 21:59", "2026-03-04 22:00"]
        )
        self.assertEqual(gp.in_shift(s, "sang").tolist(), [False, True, True, False, False, False])
        self.assertEqual(gp.in_shift(s, "chieu").tolist(), [False, False, False, True, True, False])
        with self.assertRaises(ValueError):
            gp.in_shift(s, "toi")

    def test_count_weekday(self):
        nov = P("2026-11-01", "2026-11-30")  # 01/11/2026 là Chủ nhật
        self.assertEqual(gp.count_weekday(nov, 7), 5)  # CN: 1, 8, 15, 22, 29
        self.assertEqual(gp.count_weekday(nov, 1), 5)  # T2: 2, 9, 16, 23, 30
        self.assertEqual(gp.count_weekday(nov, 2), 4)  # T3: 3, 10, 17, 24
        self.assertEqual(sum(gp.count_weekday(nov, w) for w in range(1, 8)), 30)
        with self.assertRaises(ValueError):
            gp.count_weekday(nov, 0)

    def test_clip_to_data(self):
        k = P("2026-03-01", "2026-03-31")
        self.assertEqual(gp.clip_to_data(k, "2026-03-10", "2026-12-31"), P("2026-03-10", "2026-03-31"))
        self.assertEqual(gp.clip_to_data(k, "2025-01-01", "2026-03-15"), P("2026-03-01", "2026-03-15"))
        self.assertEqual(gp.clip_to_data(k, "2025-01-01", "2026-12-31"), k)
        self.assertIsNone(gp.clip_to_data(k, "2026-04-01", "2026-12-31"))  # hoàn toàn ngoài → unanswerable
        self.assertIsNone(gp.clip_to_data(k, "2025-01-01", "2026-02-28"))

    def test_iso(self):
        self.assertEqual(gp.iso(P("2026-03-01", "2026-03-31")), ("2026-03-01", "2026-03-31"))


if __name__ == "__main__":
    unittest.main(verbosity=2)