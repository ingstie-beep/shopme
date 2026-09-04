#!/usr/bin/env python3
"""
MCP server: ร้านค้าปลีก - SOP ฝ่ายจัดซื้อ & ฝ่ายขายหน้าร้าน (SOP-RETAIL-01)

เปิด SOP ให้ MCP client ใด ๆ (Claude Desktop, Claude Code ฯลฯ) เรียกใช้เป็นเครื่องมือ
(tools) ได้ เช่น ดูรายชื่อหัวข้อทั้งหมด, ดึงเนื้อหาหัวข้อใดหัวข้อหนึ่ง, ค้นหาคำในเอกสาร,
หรือดึงเอกสารฉบับเต็ม

รันแบบ stdio server: python3 server.py
"""
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

SOP_PATH = Path(__file__).parent / "sop_data" / "full-sop.md"
SOP_TEXT = SOP_PATH.read_text(encoding="utf-8")

mcp = FastMCP("retail-shop-sop")


def _parse_sections(text: str) -> dict[str, str]:
    """แบ่งเอกสาร markdown ออกเป็น {หัวข้อ: เนื้อหา} ตามหัวข้อระดับ ## และ ###"""
    pattern = re.compile(r"^(#{2,3})\s+(.*)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        heading = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[heading] = text[start:end].strip()
    return sections


SECTIONS = _parse_sections(SOP_TEXT)


@mcp.tool()
def list_sections() -> list[str]:
    """แสดงรายชื่อหัวข้อทั้งหมดใน SOP (ฝ่ายจัดซื้อและฝ่ายขายหน้าร้าน)"""
    return list(SECTIONS.keys())


@mcp.tool()
def get_section(heading: str) -> str:
    """ดึงเนื้อหาของหัวข้อใดหัวข้อหนึ่งใน SOP แบบเต็ม

    heading: ชื่อหัวข้อแบบเต็มหรือบางส่วนก็ได้ (เช่น 'การรับสินค้า', 'ปิดยอดขาย')
    ดูรายชื่อหัวข้อทั้งหมดได้จาก list_sections ก่อน
    """
    heading_lower = heading.strip().lower()
    for title, body in SECTIONS.items():
        if heading_lower in title.lower():
            return f"## {title}\n\n{body}"
    return f"ไม่พบหัวข้อที่ตรงกับ '{heading}' — ใช้ list_sections เพื่อดูหัวข้อทั้งหมด"


@mcp.tool()
def search_sop(query: str) -> str:
    """ค้นหาคำหรือวลีในเอกสาร SOP ทั้งฉบับ คืนค่าเป็นบรรทัดที่พบพร้อมบริบทรอบข้าง"""
    query_lower = query.strip().lower()
    lines = SOP_TEXT.splitlines()
    hits = []
    for i, line in enumerate(lines):
        if query_lower in line.lower():
            start, end = max(0, i - 1), min(len(lines), i + 2)
            hits.append("\n".join(lines[start:end]))
    if not hits:
        return f"ไม่พบข้อความที่ตรงกับ '{query}' ใน SOP"
    return "\n\n---\n\n".join(hits[:10])


@mcp.tool()
def get_full_sop() -> str:
    """คืนค่าเอกสาร SOP-RETAIL-01 ฉบับเต็ม (ฝ่ายจัดซื้อ + ฝ่ายขายหน้าร้าน)"""
    return SOP_TEXT


@mcp.resource("sop://retail-shop/full")
def full_sop_resource() -> str:
    """เอกสาร SOP-RETAIL-01 ฉบับเต็ม ในรูปแบบ resource ให้ client อ่านได้โดยตรง"""
    return SOP_TEXT


if __name__ == "__main__":
    mcp.run()
