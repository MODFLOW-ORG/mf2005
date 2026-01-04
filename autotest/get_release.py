"""Download official MODFLOW-2005 release executable for regression testing."""
import platform
from pathlib import Path
from modflow_devtools.download import get_release, download_and_unzip
from modflow_devtools.ostags import get_ostag
import config


def get_release_executable():
    """
    Download the official MODFLOW-2005 release executable from MODFLOW-ORG/executables.
    Places it in temp/release/ for use as regression test baseline.
    """
    release_dir = Path(config.releasedir)
    release_dir.mkdir(parents=True, exist_ok=True)

    exe_name = f"mf2005{config.exe_ext}"
    exe_path = release_dir / exe_name

    # Skip if executable already exists
    if exe_path.exists():
        print(f"Release executable already exists: {exe_path}")
        return

    # Get the latest release from MODFLOW-ORG/executables
    print("Fetching latest release info from MODFLOW-ORG/executables...")
    try:
        release = get_release("MODFLOW-ORG/executables", tag="latest", verbose=True)
    except Exception as e:
        print(f"Failed to get release info: {e}")
        print("Regression testing will be skipped.")
        return

    # Get the appropriate asset for this platform
    ostag = get_ostag()
    assets = release["assets"]

    # Find the asset for this platform
    # Asset names are typically like: "linux.zip", "mac.zip", "win64.zip"
    asset_url = None
    for asset in assets:
        asset_name = asset["name"]
        if ostag in asset_name or (ostag == "win64" and "win" in asset_name):
            asset_url = asset["browser_download_url"]
            print(f"Found asset: {asset_name}")
            break

    if not asset_url:
        print(f"No asset found for platform: {ostag}")
        print("Regression testing will be skipped.")
        return

    # Download and extract the archive
    print(f"Downloading and extracting {asset_url}...")
    try:
        extract_path = download_and_unzip(
            asset_url,
            path=release_dir,
            delete_zip=True,
            verbose=True
        )

        # The executable should be somewhere in the extracted files
        # Look for mf2005 or mf2005.exe in the extracted directory
        extracted_files = list(release_dir.rglob("mf2005*"))

        # Find the actual executable
        mf2005_exe = None
        for f in extracted_files:
            if f.is_file() and f.name.lower() in ["mf2005", "mf2005.exe"]:
                mf2005_exe = f
                break

        if mf2005_exe and mf2005_exe != exe_path:
            # Move to expected location
            mf2005_exe.rename(exe_path)
            print(f"Moved executable to: {exe_path}")
        elif mf2005_exe:
            print(f"Release executable ready: {exe_path}")
        else:
            print("Warning: Could not find mf2005 executable in extracted files")
            print("Regression testing will be skipped.")
            return

        # Make executable on Unix
        if platform.system() in ["Linux", "Darwin"]:
            import os
            os.chmod(exe_path, 0o755)

        # Clean up any other extracted files/directories
        for item in release_dir.iterdir():
            if item != exe_path and item.is_dir():
                import shutil
                shutil.rmtree(item)
            elif item != exe_path and item.is_file() and item.name != exe_name:
                item.unlink()

        print(f"Release executable ready: {exe_path}")

    except Exception as e:
        print(f"Error downloading or extracting release: {e}")
        print("Regression testing will be skipped.")
        return


if __name__ == "__main__":
    get_release_executable()
