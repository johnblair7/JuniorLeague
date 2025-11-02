"""
Import all historical JuniorLeague data files
"""
from data_import import import_csv_file
from app import app

if __name__ == '__main__':
    with app.app_context():
        files = [
            'data/imports/uploads/JuniorLeague2021.csv',
            'data/imports/uploads/JuniorLeague2024.csv',
            'data/imports/uploads/JuniorLeague2025.csv',
        ]
        
        for filepath in files:
            try:
                import_csv_file(filepath, confirm_matches=False)
            except Exception as e:
                print(f"\n⚠ Error importing {filepath}: {e}\n")
        
        print("\n" + "="*60)
        print("All imports complete!")
        print("="*60)

