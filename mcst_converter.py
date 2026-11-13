"""문체부 기사 목록 시트를 조간 언론보도 TXT 형식으로 변환."""
from datetime import date
from io import BytesIO
from openpyxl import load_workbook
import re


def _val(v):
    return str(v).strip() if v is not None else ""


def convert_mcst_excel(source, report_date=None):
    """source: Streamlit UploadedFile, bytes 또는 경로. 결과: (텍스트, 통계)."""
    if hasattr(source, "getvalue"):
        source = BytesIO(source.getvalue())
    elif isinstance(source, bytes):
        source = BytesIO(source)
    wb = load_workbook(source, read_only=True, data_only=True)
    try:
        if "기사 목록" not in wb.sheetnames:
            raise ValueError("'기사 목록' 시트를 찾지 못했습니다. 해당 시트가 있는 엑셀을 업로드하세요.")
        ws = wb["기사 목록"]
        rows = ws.iter_rows(values_only=True)
        header = next(rows, ())
        names = [_val(v).replace(" ", "") for v in header]
        def col(*opts):
            for option in opts:
                if option in names:
                    return names.index(option)
            return None
        i_title = col("기사제목", "제목")
        i_press = col("매체명", "매체")
        i_page = col("지면", "면")
        i_original = col("원문URL", "원문링크")
        i_naver = col("네이버URL", "네이버링크")
        if i_title is None or i_press is None:
            raise ValueError("기사 목록 시트에 '기사제목', '매체명' 열이 필요합니다.")
        def get(row, idx):
            return _val(row[idx]) if idx is not None and idx < len(row) else ""
        entries = []
        group = None
        article_count = 0
        duplicates = 0
        for row in rows:
            title = get(row, i_title)
            press = get(row, i_press)
            if not title:
                continue
            if not press and (title.startswith("<") or title.startswith("*")):
                entries.append({"kind": "heading", "text": title})
                group = None
                continue
            if not press:
                continue
            page = get(row, i_page)
            original = get(row, i_original)
            naver = get(row, i_naver)
            url = naver or original
            # 동일 링크가 연속된 행은 같은 기사로 간주하고 지면만 합칩니다.
            # 섹션 경계를 넘거나 링크가 없는 기사는 병합하지 않습니다.
            key = (press, naver or original) if (naver or original) else None
            if key and group and group["key"] == key:
                if page and page not in group["pages"]:
                    group["pages"].append(page)
                duplicates += 1
                continue
            group = {"kind": "article", "title": title, "press": press, "pages": [page] if page else [], "url": url, "key": key}
            entries.append(group)
            article_count += 1
        if not article_count:
            raise ValueError("기사 목록에서 변환할 기사를 찾지 못했습니다.")
        d = report_date or date.today()
        if isinstance(d, str):
            d = date.fromisoformat(d)
        weekdays = ["월", "화", "수", "목", "금", "토", "일"]
        lines = [f"{d:%m.%d.}({weekdays[d.weekday()]}) 조간 언론보도 요약입니다", ""]
        for item in entries:
            if item["kind"] == "heading":
                lines.extend([item["text"], ""])
            else:
                suffix = ", ".join([item["press"]] + item["pages"])
                lines.append(f"■ {item['title']} ({suffix})")
                if item["url"]:
                    lines.append(item["url"])
                lines.append("")
        return "\n".join(lines).rstrip() + "\n", {"articles": article_count, "merged_rows": duplicates, "sections": sum(x["kind"] == "heading" for x in entries)}
    finally:
        wb.close()
