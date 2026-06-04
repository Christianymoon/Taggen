"""
Post-build script for PyInstaller
Copies necessary files and folders to the dist/taggen directory
"""
import shutil
import os
from pathlib import Path

def post_build():
    """Copy files and folders after PyInstaller build"""
    
    # Define source and destination paths
    script_dir = Path(__file__).parent
    dist_dir = script_dir / "dist" / "taggen"
    
    # Ensure dist directory exists
    if not dist_dir.exists():
        print(f"Error: {dist_dir} does not exist. Build may have failed.")
        return False
    
    try:
        # Copy allbarcodes.csv
        csv_source = script_dir / "allbarcodes.csv"
        csv_dest = dist_dir / "allbarcodes.csv"
        settings_source = script_dir / "settings.json"
        settings_dest = dist_dir / "settings.json"
        
        if csv_source.exists():
            shutil.copy2(csv_source, csv_dest)
            print(f"✓ Copied allbarcodes.csv to {csv_dest}")
        else:
            print(f"Warning: {csv_source} not found")
        
        # Copy assets folder
        assets_source = script_dir / "assets"
        assets_dest = dist_dir / "assets"

        # copy settings .json 
        if settings_source.exists():
            if settings_dest.exists():
                settings_dest.unlink()  # Remove existing settings.json
                print(f"Removed existing {settings_dest}")
            shutil.copy2(settings_source, settings_dest)
            print(f"✓ Copied settings.json to {settings_dest}")
        
        if assets_source.exists():
            # Remove existing assets folder if it exists
            if assets_dest.exists():
                shutil.rmtree(assets_dest)
                print(f"Removed existing {assets_dest}")
            
            shutil.copytree(assets_source, assets_dest)
            print(f"✓ Copied assets folder to {assets_dest}")
        else:
            print(f"Warning: {assets_source} not found")
        
        print("\n✓ Post-build completed successfully!")
        return True
    
        
        
    except Exception as e:
        print(f"Error during post-build: {e}")
        return False

if __name__ == "__main__":
    success = post_build()
    exit(0 if success else 1)
