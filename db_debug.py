#!/usr/bin/env python3
"""
Debug script to check where the database is being created
and to ensure all database files are cleaned up.
"""
import os
import shutil
import platform
import time

def find_database_files(root_dir):
    """Find all timetable.db files in the project directory."""
    print(f"Searching for database files in {root_dir}...")
    db_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip venv directories
        if 'venv' in dirpath or '.git' in dirpath:
            continue
        
        for filename in filenames:
            if filename == 'timetable.db':
                full_path = os.path.join(dirpath, filename)
                db_files.append(full_path)
                print(f"Found database file: {full_path}")
    
    return db_files

def remove_database_files(db_files):
    """Remove all found database files."""
    for db_file in db_files:
        try:
            os.remove(db_file)
            print(f"Removed: {db_file}")
        except Exception as e:
            print(f"Error removing {db_file}: {e}")

def create_clean_instance_directory(root_dir):
    """Create a clean instance directory within the app folder."""
    app_dir = os.path.join(root_dir, 'app')
    instance_dir = os.path.join(app_dir, 'instance')
    
    # Create instance directory if it doesn't exist
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"Created instance directory: {instance_dir}")
    
    return instance_dir

def print_system_info():
    """Print system information for debugging."""
    print("\n=== System Information ===")
    print(f"Python Version: {platform.python_version()}")
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Platform: {platform.platform()}")
    print(f"Current Working Directory: {os.getcwd()}")
    print("============================\n")

if __name__ == "__main__":
    print_system_info()
    
    # Get project root directory
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find and remove all database files
    db_files = find_database_files(root_dir)
    
    if db_files:
        print(f"\nFound {len(db_files)} database files.")
        
        # Ask user if they want to remove all database files
        response = input("Do you want to remove all found database files? (y/n): ")
        if response.lower() == 'y':
            remove_database_files(db_files)
            print("All database files removed.")
            
            # Create clean instance directory
            instance_dir = create_clean_instance_directory(root_dir)
            print(f"Set up clean instance directory at: {instance_dir}")
            
            print("\nDatabase cleanup complete!")
        else:
            print("No files were removed.")
    else:
        print("No database files found. Your project is clean.")
        
        # Create clean instance directory
        instance_dir = create_clean_instance_directory(root_dir)
        print(f"Set up clean instance directory at: {instance_dir}")