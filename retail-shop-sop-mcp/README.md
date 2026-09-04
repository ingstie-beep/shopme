# retail-shop-sop MCP server

MCP server ที่เปิด SOP-RETAIL-01 (ฝ่ายจัดซื้อ + ฝ่ายขายหน้าร้าน) ให้เรียกใช้เป็นเครื่องมือ (tools) ได้ ผ่าน [Model Context Protocol](https://modelcontextprotocol.io)

**สำคัญ:** นี่คือ MCP server แบบรันในเครื่อง (local stdio server) — ไม่ใช่บริการออนไลน์ ต้องติดตั้งและรันบนคอมพิวเตอร์ที่จะใช้งาน แล้วชี้ MCP client (เช่น Claude Desktop, Claude Code) ให้มาเรียกใช้ ไฟล์นี้ไม่ได้เชื่อมกับแชทนี้โดยอัตโนมัติ

## เครื่องมือ (tools) ที่มีให้

| เครื่องมือ | ใช้ทำอะไร |
|---|---|
| `list_sections` | แสดงหัวข้อทั้งหมดใน SOP |
| `get_section(heading)` | ดึงเนื้อหาของหัวข้อใดหัวข้อหนึ่ง (พิมพ์ชื่อหัวข้อบางส่วนได้) |
| `search_sop(query)` | ค้นหาคำ/วลีในเอกสารทั้งฉบับ |
| `get_full_sop` | ดึงเอกสาร SOP ฉบับเต็มทั้งหมด |

เนื้อหา SOP อยู่ที่ `sop_data/full-sop.md` — แก้ไขไฟล์นี้ได้โดยตรงเมื่อ SOP มีการอัปเดต ไม่ต้องแก้โค้ด

## วิธีติดตั้ง

ต้องมี Python 3.10 ขึ้นไป

```bash
cd retail-shop-sop-mcp
pip install -r requirements.txt
```

ทดสอบว่ารันได้ (จะค้างรอ input เพราะเป็น stdio server — กด Ctrl+C เพื่อออก):

```bash
python3 server.py
```

## วิธีเชื่อมกับ Claude Desktop

แก้ไฟล์ config ของ Claude Desktop:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

เพิ่มรายการนี้ (แก้ path ให้ตรงกับที่วางไฟล์จริง):

```json
{
  "mcpServers": {
    "retail-shop-sop": {
      "command": "python3",
      "args": ["/absolute/path/to/retail-shop-sop-mcp/server.py"]
    }
  }
}
```

จากนั้นปิด-เปิด Claude Desktop ใหม่ จะเห็นเครื่องมือ `list_sections`, `get_section`, `search_sop`, `get_full_sop` ในเมนู tools

## วิธีเชื่อมกับ Claude Code

```bash
claude mcp add retail-shop-sop -- python3 /absolute/path/to/retail-shop-sop-mcp/server.py
```

## หมายเหตุ

- Skill (`SKILL.md`) กับ MCP server นี้ **ทำงานคนละแบบ**: Skill คือคำแนะนำให้ Claude อ่านแล้วทำตาม/ร่างเอกสารให้ ส่วน MCP server นี้คือเครื่องมือที่ Claude (หรือ MCP client อื่น) เรียก "ดึงข้อมูล" จากไฟล์ SOP จริงแบบเป๊ะๆ ไม่ได้สรุปหรือตีความ — เหมาะเป็นแหล่งอ้างอิงที่แน่นอนเวลาต้องการข้อความต้นฉบับ
- ถ้าแก้ไข `sop_data/full-sop.md` ต้อง restart server (หรือ restart Claude Desktop/Claude Code) เพื่อให้โหลดเนื้อหาใหม่
