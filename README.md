# SMM — Blender MCP
Local MCP server for rendering editable Blender scenes. Python 3.12+ and Blender required.

Install: `python -m pip install -r requirements.txt`.
Run: `python server.py` (stdio MCP transport).
Configure your MCP client with command `python`, args `["/absolute/path/to/SMM/server.py"]`, and environment `BLENDER_BIN`, `SMM_SCENES`, `SMM_OUTPUT` as needed.
Generate demo: `blender -b --python demo.py`. Then use MCP tools `list_scenes` and `render_scene`.
Only render trusted .blend files: Blender scene files may execute Python. No remote code or arbitrary Python tool is exposed.
CI renders on CPU; Windows AMD HIP setup will follow after CI validation.
