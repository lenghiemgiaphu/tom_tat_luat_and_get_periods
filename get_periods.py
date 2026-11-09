"""get_periods.py: các kỳ thời gian theo rulebook DataMate (§2).

Quy ước chung
-------------
* Mỗi kỳ là một tuple ``(start, end)`` gồm hai ``pd.Timestamp`` đã normalize
  (00:00:00), **gồm cả hai đầu**.
* Lọc dữ liệu bằng ``in_period(series, period)``. Đừng tự so ``<= end`` với cột
  có giờ: đơn lúc 15:30 của ngày ``end`` sẽ bị mất.
* ``as_of_date`` nhận ``str`` ISO, ``date``, ``datetime`` hoặc ``Timestamp``.
* ``calendar_df`` là DataFrame của ``calendar.csv`` (date, weekday, lunar_day,
  lunar_month, lunar_year, lunar_leap, holiday). ``weekday``: 1 = thứ Hai ...
  7 = Chủ nhật.

Rulebook không định nghĩa nên module KHÔNG làm: "cùng kỳ năm ngoái", "quý này",
và kỳ so sánh của "tuần này" (chỉ có ``tuan_truoc`` là cả tuần liền trước).
Gặp các câu đó thì theo chữ trong câu hỏi, hoặc abstain nếu không chắc.
"""
from __future__ import annotations

import calendar as _calendar

import pandas as pd

Period = tuple  # (pd.Timestamp, pd.Timestamp)

_ONE_DAY = pd.Timedelta(days=1)


class CalendarError(ValueError):
    """calendar.csv thiếu cột, thiếu ngày âm lịch cần tra, hoặc tra ra mơ hồ."""


# --------------------------------------------------------------------------- #
# Tiện ích nhỏ
# --------------------------------------------------------------------------- #
def _to_ts(x) -> pd.Timestamp:
    ts = pd.Timestamp(x)
    if ts.tzinfo is not None:
        ts = ts.tz_localize(None)
    return ts.normalize()


def _month_bounds(year: int, month: int) -> Period:
    if not 1 <= int(month) <= 12:
        raise ValueError(f"tháng phải từ 1 đến 12, nhận được {month!r}")
    last = _calendar.monthrange(int(year), int(month))[1]
    return pd.Timestamp(int(year), int(month), 1), pd.Timestamp(int(year), int(month), last)


def _prev_month(year: int, month: int) -> tuple:
    return (year - 1, 12) if month == 1 else (year, month - 1)


def iso(period: Period) -> tuple:
    """Kỳ -> ('YYYY-MM-DD', 'YYYY-MM-DD'), tiện in/log."""
    return period[0].strftime("%Y-%m-%d"), period[1].strftime("%Y-%m-%d")


# --------------------------------------------------------------------------- #
# Lịch âm / Tết
# --------------------------------------------------------------------------- #
def _prepare_calendar(calendar_df: pd.DataFrame) -> pd.DataFrame:
    need = {"date", "lunar_day", "lunar_month", "lunar_year", "lunar_leap"}
    missing = need - set(calendar_df.columns)
    if missing:
        raise CalendarError(f"calendar thiếu cột: {sorted(missing)}")
    cal = calendar_df.copy()
    cal["date"] = pd.to_datetime(cal["date"]).dt.normalize()
    for c in ("lunar_day", "lunar_month", "lunar_year"):
        cal[c] = pd.to_numeric(cal[c], errors="coerce")
    # lunar_leap có thể là bool thật hoặc chuỗi "true"/"false"/"1"/"0"
    cal["_leap"] = (
        cal["lunar_leap"].astype(str).str.strip().str.lower().isin({"true", "1", "1.0", "yes", "y", "t"})
    )
    return cal


def _lunar_date(cal: pd.DataFrame, lunar_year: int, lunar_month: int, lunar_day: int) -> pd.Timestamp:
    """Ngày dương của một ngày âm lịch **không nhuận**; lỗi rõ ràng nếu không có/mơ hồ."""
    hit = cal[
        (cal["lunar_year"] == lunar_year)
        & (cal["lunar_month"] == lunar_month)
        & (cal["lunar_day"] == lunar_day)
        & (~cal["_leap"])
    ]
    label = f"{lunar_day}/{lunar_month}/{lunar_year} âm lịch (không nhuận)"
    if len(hit) == 0:
        lo, hi = cal["date"].min().date(), cal["date"].max().date()
        raise CalendarError(f"calendar không có {label}; calendar phủ {lo} → {hi}")
    if len(hit) > 1:
        raise CalendarError(f"calendar có {len(hit)} dòng cho {label}, không xác định được")
    return hit["date"].iloc[0]


def tet_period(year: int, calendar_df: pd.DataFrame) -> Period:
    """Tết năm ``year``: 23 tháng Chạp (năm âm year-1) → HẾT mùng 10 tháng Giêng (năm âm year)."""
    cal = _prepare_calendar(calendar_df)
    start = _lunar_date(cal, int(year) - 1, 12, 23)
    end = _lunar_date(cal, int(year), 1, 10)
    if end < start:
        raise CalendarError(f"Tết {year}: ngày kết thúc {end.date()} trước ngày bắt đầu {start.date()}")
    return start, end


def before_tet_period(year: int, calendar_df: pd.DataFrame) -> Period:
    """'Trước Tết' = cùng số ngày với kỳ Tết, ngay trước 23 tháng Chạp."""
    start, end = tet_period(year, calendar_df)
    length = (end - start).days + 1
    return start - length * _ONE_DAY, start - _ONE_DAY


# --------------------------------------------------------------------------- #
# Tháng / quý / N ngày
# --------------------------------------------------------------------------- #
def month_period(month: int, year: int | None = None, as_of_date=None) -> Period:
    """Cả tháng M/Y. Không ghi năm: năm nay nếu tháng đó không bắt đầu sau hôm nay,
    ngược lại năm trước (tháng hiện tại tính là năm nay)."""
    if year is None:
        if as_of_date is None:
            raise ValueError("không có năm thì phải truyền as_of_date")
        today = _to_ts(as_of_date)
        first, _ = _month_bounds(today.year, month)
        year = today.year if first <= today else today.year - 1
    return _month_bounds(year, month)


def prev_month_period(month: int, year: int) -> Period:
    """Cả tháng liền trước tháng M/Y (xử lý tháng 1)."""
    y, m = _prev_month(int(year), int(month))
    return _month_bounds(y, m)


def quarter_period(quarter: int, year: int | None = None, as_of_date=None) -> Period:
    """Cả quý dương lịch (Q1 = tháng 1–3). Không ghi năm: giống ``month_period``."""
    if int(quarter) not in (1, 2, 3, 4):
        raise ValueError(f"quý phải từ 1 đến 4, nhận được {quarter!r}")
    first_month = 3 * int(quarter) - 2

    def bounds(y: int) -> Period:
        return _month_bounds(y, first_month)[0], _month_bounds(y, first_month + 2)[1]

    if year is None:
        if as_of_date is None:
            raise ValueError("không có năm thì phải truyền as_of_date")
        today = _to_ts(as_of_date)
        year = today.year if bounds(today.year)[0] <= today else today.year - 1
    return bounds(int(year))


def prev_quarter_period(quarter: int, year: int) -> Period:
    """Cả quý liền trước quý Q/Y (xử lý Q1)."""
    q, y = (4, int(year) - 1) if int(quarter) == 1 else (int(quarter) - 1, int(year))
    return quarter_period(q, y)


def last_n_days(n: int, as_of_date) -> Period:
    """N ngày gần nhất: N ngày liền nhau, ngày cuối là hôm nay."""
    n = int(n)
    if n < 1:
        raise ValueError(f"N phải ≥ 1, nhận được {n}")
    today = _to_ts(as_of_date)
    return today - (n - 1) * _ONE_DAY, today


def previous_period_same_length(period: Period) -> Period:
    """Kỳ ngay trước, cùng số ngày (dùng khi câu hỏi tự nêu 'kỳ trước' của một khoảng tuỳ ý)."""
    start, end = period
    length = (end - start).days + 1
    return start - length * _ONE_DAY, start - _ONE_DAY


# --------------------------------------------------------------------------- #
# Bộ kỳ chuẩn theo as_of_date
# --------------------------------------------------------------------------- #
def get_periods(as_of_date, calendar_df: pd.DataFrame | None = None) -> dict:
    """Trả dict tên kỳ -> (start, end). Mọi đầu mút gồm trong kỳ.

    hom_nay, hom_qua
    tuan_nay (T2 → hết hôm nay), tuan_truoc (cả T2–CN liền trước)
    thang_nay (ngày 1 → hết hôm nay)
    thang_truoc_cung_so_ngay (kỳ so của 'tháng này': 01 → ngày trùng số hôm nay,
        kẹp về cuối tháng nếu tháng trước ngắn hơn)
    thang_truoc (cả tháng liền trước)
    dau_nam (01/01 → hết hôm nay)
    tet_nam_nay, truoc_tet_nam_nay (chỉ khi calendar_df phủ được năm đó)
    """
    today = _to_ts(as_of_date)
    p: dict = {}

    p["hom_nay"] = (today, today)
    p["hom_qua"] = (today - _ONE_DAY, today - _ONE_DAY)

    monday = today - today.weekday() * _ONE_DAY  # Python: Monday = 0
    p["tuan_nay"] = (monday, today)
    p["tuan_truoc"] = (monday - 7 * _ONE_DAY, monday - _ONE_DAY)

    p["thang_nay"] = (today.replace(day=1), today)
    py, pm = _prev_month(today.year, today.month)
    pstart, pend = _month_bounds(py, pm)
    p["thang_truoc"] = (pstart, pend)
    p["thang_truoc_cung_so_ngay"] = (pstart, pstart.replace(day=min(today.day, pend.day)))

    p["dau_nam"] = (pd.Timestamp(today.year, 1, 1), today)

    if calendar_df is not None:
        try:
            p["tet_nam_nay"] = tet_period(today.year, calendar_df)
            p["truoc_tet_nam_nay"] = before_tet_period(today.year, calendar_df)
        except CalendarError:
            pass  # calendar không phủ năm này: gọi tet_period() trực tiếp sẽ thấy lỗi rõ
    return p


# --------------------------------------------------------------------------- #
# Lọc dữ liệu / đếm
# --------------------------------------------------------------------------- #
def in_period(series, period: Period) -> pd.Series:
    """Mask bool: ngày của từng phần tử nằm trong kỳ (gồm cả hai đầu, bỏ qua giờ)."""
    start, end = period
    days = pd.to_datetime(pd.Series(series)).dt.normalize()
    return (days >= start) & (days <= end)


SHIFTS = {"sang": (6, 13), "chieu": (14, 21)}  # giờ bắt đầu, giờ cuối (gồm cả phút 59)


def in_shift(series, shift: str) -> pd.Series:
    """Mask bool theo ca: sáng 06:00–13:59, chiều 14:00–21:59 (giờ tạo đơn).
    Cột chỉ có ngày (không có giờ) sẽ cho toàn False."""
    if shift not in SHIFTS:
        raise ValueError(f"ca phải là 'sang' hoặc 'chieu', nhận được {shift!r}")
    lo, hi = SHIFTS[shift]
    hours = pd.to_datetime(pd.Series(series)).dt.hour
    return (hours >= lo) & (hours <= hi)


def count_weekday(period: Period, weekday: int) -> int:
    """Số ngày thứ X trong kỳ (weekday: 1 = thứ Hai ... 7 = Chủ nhật, như calendar.csv).
    Dùng cho 'trung bình mỗi ngày thứ X': chia cho số này, kể cả ngày không có đơn."""
    if int(weekday) not in range(1, 8):
        raise ValueError(f"weekday phải từ 1 đến 7, nhận được {weekday!r}")
    days = pd.date_range(period[0], period[1], freq="D")
    return int(((days.dayofweek + 1) == int(weekday)).sum())


def clip_to_data(period: Period, data_start, data_end) -> Period | None:
    """Phần của kỳ nằm trong khoảng ngày có dữ liệu. ``None`` nghĩa là kỳ nằm HOÀN TOÀN
    ngoài dữ liệu → câu trả lời là unanswerable (không phải 0)."""
    start = max(period[0], _to_ts(data_start))
    end = min(period[1], _to_ts(data_end))
    return (start, end) if start <= end else None