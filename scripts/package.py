"""Package a native build before artifact upload can dereference its symlinks."""
import hashlib
from pathlib import Path
import platform
import runpy
import shutil
import tarfile


def package(dist: Path, version: str, system: str, arch: str) -> Path:
    target = {"Darwin": "macos", "Linux": "linux", "Windows": "windows"}[system]
    arch = {"amd64": "x86_64", "aarch64": "arm64"}.get(arch.lower(), arch.lower())
    bundle = dist / ("TABOt.app" if system == "Darwin" else "TABOt")
    if not bundle.is_dir():
        raise RuntimeError(f"Missing build: {bundle}")
    links = [path for path in bundle.rglob("*") if path.is_symlink()]
    if system == "Darwin" and not links:
        raise RuntimeError("macOS bundle has no symbolic links; package the original PyInstaller build.")
    output = dist / "packages"
    output.mkdir(parents=True, exist_ok=True)
    basename = output / f"TABOt-{version}-{target}-{arch}"
    if system == "Windows":
        archive = Path(shutil.make_archive(str(basename), "zip", dist, bundle.name))
    else:
        archive = basename.with_name(basename.name + ".tar.gz")
        with tarfile.open(archive, "w:gz", dereference=False) as tar:
            tar.add(bundle, arcname=bundle.name)
        # Catch accidental dereferencing before uploading the release archive.
        with tarfile.open(archive, "r:gz") as tar:
            archived_links = {member.name: member.linkname for member in tar if member.issym()}
        expected_links = {path.relative_to(dist).as_posix(): str(path.readlink()) for path in links}
        if archived_links != expected_links:
            raise RuntimeError("Archive did not preserve the build's symbolic links.")
    with archive.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    archive.with_name(archive.name + ".sha256").write_text(
        f"{digest}  {archive.name}\n", encoding="utf-8"
    )
    print(f"Packaged {archive.name}: {archive.stat().st_size / 2**20:.1f} MiB, {len(links)} symbolic links")
    return archive


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    version = runpy.run_path(str(root / "tabota" / "__init__.py"))["__version__"]
    package(root / "dist", version, platform.system(), platform.machine())
