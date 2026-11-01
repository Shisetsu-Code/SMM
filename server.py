import os, json, subprocess, uuid
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SMM Blender Renderer")
ROOT = Path(os.environ.get("SMM_OUTPUT", "renders")).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
BLENDER = os.environ.get("BLENDER_BIN", "blender")

@mcp.tool()
def render_scene(scene: str, resolution: int = 512, samples: int = 32) -> dict:
    """Render an existing .blend file under the configured scene directory."""
    base = Path(os.environ.get("SMM_SCENES", "scenes")).resolve()
    target = (base / scene).resolve()
    if not target.is_relative_to(base) or target.suffix != ".blend" or not target.is_file():
        return {"error": "Invalid or missing .blend scene"}
    if not 64 <= resolution <= 4096 or not 1 <= samples <= 512:
        return {"error": "Invalid render parameters"}
    job = uuid.uuid4().hex
    output = ROOT / job
    output.mkdir()
    script = Path(__file__).with_name("render.py")
    cmd = [BLENDER, "-b", str(target), "--python", str(script), "--",
           str(output / "render.png"), str(resolution), str(samples)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600,
                                env={**os.environ, "SDL_AUDIODRIVER": "dummy"})
        return {"job": job, "success": result.returncode == 0 and (output / "render.png").exists(),
                "image": str(output / "render.png"), "log": (result.stdout + result.stderr)[-4000:]}
    except subprocess.TimeoutExpired:
        return {"job": job, "error": "Render timed out"}

@mcp.tool()
def list_scenes() -> list[str]:
    """List scenes available for rendering."""
    base = Path(os.environ.get("SMM_SCENES", "scenes")).resolve()
    return [str(p.relative_to(base)) for p in base.rglob("*.blend")] if base.exists() else []

if __name__ == "__main__":
    mcp.run()
