#!/usr/bin/env python3
"""
Unified Windows Behavior Parser
Combines Timeline (ActivityCache.db) and Recall (ukg.db) parsing
Version: 2.0
"""

import argparse
from pathlib import Path
from typing import Optional
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Import our parsers
try:
    from TimelineParser import TimelineParser, ReportGenerator
    from recall_parser import WindowsRecallParser
except ImportError:
    print("⚠️  Please ensure TimelineParser.py and recall_parser.py are in the same directory")
    raise

console = Console()


class UnifiedParser:
    """Unified parser for both Timeline and Recall databases"""
    
    @staticmethod
    def detect_database_type(db_path: Path) -> str:
        """Auto-detect database type"""
        import sqlite3
        
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            # Check for Recall tables
            if 'WindowCapture' in tables or 'WindowCaptureTextIndex_content' in tables:
                return 'recall'
            
            # Check for Timeline tables
            elif 'SmartLookup' in tables or 'Activity' in tables:
                return 'timeline'
            
            else:
                # Fallback to filename
                if 'ukg' in db_path.name.lower():
                    return 'recall'
                elif 'activity' in db_path.name.lower() or 'cache' in db_path.name.lower():
                    return 'timeline'
                
                return 'unknown'
                
        except Exception as e:
            console.print(f"[red]Error detecting database type: {e}[/red]")
            return 'unknown'
    
    @staticmethod
    def parse_timeline(db_path: Path, output_dir: Path, verbose: bool = False) -> pd.DataFrame:
        """Parse Windows Timeline database"""
        console.print("[cyan]📊 Parsing Windows Timeline database...[/cyan]")
        
        with TimelineParser(db_path, verbose=verbose) as parser:
            df = parser.parse()
        
        # Generate reports
        generator = ReportGenerator(df, output_dir)
        generator.generate_all_reports()
        
        console.print(f"[green]✅ Timeline: Parsed {len(df)} records[/green]")
        return df
    
    @staticmethod
    def parse_recall(db_path: Path, output_dir: Path, verbose: bool = False, search_term: Optional[str] = None) -> pd.DataFrame:
        """Parse Windows Recall database"""
        console.print("[cyan]🔮 Parsing Windows Recall database...[/cyan]")
        
        with WindowsRecallParser(str(db_path), verbose=verbose) as parser:
            # Show database info
            version = parser.detect_version()
            schema = parser.get_schema_info()
            
            console.print(f"[cyan]Database version: {version}[/cyan]")
            console.print(f"[cyan]Tables found: {len(schema)}[/cyan]")
            
            # Parse all data
            df = parser.parse_all()
            
            # If search term provided, also search OCR data
            if search_term:
                console.print(f"[cyan]🔍 Searching for: '{search_term}'[/cyan]")
                ocr_results = list(parser.parse_ocr_data(search_term=search_term))
                console.print(f"[green]Found {len(ocr_results)} OCR matches[/green]")
        
        console.print(f"[green]✅ Recall: Parsed {len(df)} records[/green]")
        
        # Export to CSV
        output_file = output_dir / 'recall_data.csv'
        df.to_csv(output_file, index=False)
        console.print(f"[green]💾 Saved to: {output_file}[/green]")
        
        return df
    
    @staticmethod
    def display_summary(df: pd.DataFrame, db_type: str):
        """Display summary table"""
        table = Table(title=f"{db_type.upper()} Database Summary")
        
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Records", str(len(df)))
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            date_range = f"{df['timestamp'].min()} to {df['timestamp'].max()}"
            table.add_row("Date Range", date_range)
        
        if 'activity_type' in df.columns:
            unique_types = df['activity_type'].nunique()
            table.add_row("Activity Types", str(unique_types))
        
        if 'app_name' in df.columns:
            unique_apps = df['app_name'].nunique()
            table.add_row("Unique Apps", str(unique_apps))
        
        console.print(table)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='🔍 Unified Windows Behavior Parser - Timeline & Recall',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect and parse
  python unified_parser.py -f database.db -o ./output

  # Force Timeline parsing
  python unified_parser.py -f ActivityCache.db -t timeline -o ./output

  # Parse Recall with search
  python unified_parser.py -f ukg.db -t recall -o ./output --search "password"

  # Verbose mode
  python unified_parser.py -f database.db -o ./output -v
        """
    )
    
    parser.add_argument(
        '-f', '--file',
        type=Path,
        required=True,
        help='Path to database file'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path.cwd() / 'output',
        help='Output directory (default: ./output)'
    )
    parser.add_argument(
        '-t', '--type',
        choices=['timeline', 'recall', 'auto'],
        default='auto',
        help='Database type (default: auto-detect)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--search',
        type=str,
        help='Search term for Recall OCR data'
    )
    parser.add_argument(
        '--export',
        type=Path,
        help='Export combined data to CSV'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    args.output.mkdir(exist_ok=True)
    
    # Display banner
    console.print("[bold cyan]" + "="*60 + "[/bold cyan]")
    console.print("[bold cyan]🔍 Unified Windows Behavior Parser v2.0[/bold cyan]")
    console.print("[bold cyan]" + "="*60 + "[/bold cyan]\n")
    
    # Detect database type
    db_type = args.type
    if db_type == 'auto':
        db_type = UnifiedParser.detect_database_type(args.file)
        console.print(f"[yellow]🔎 Auto-detected: {db_type.upper()} database[/yellow]\n")
    
    # Parse database
    unified = UnifiedParser()
    
    try:
        if db_type == 'timeline':
            df = unified.parse_timeline(args.file, args.output, args.verbose)
        
        elif db_type == 'recall':
            df = unified.parse_recall(
                args.file,
                args.output,
                args.verbose,
                search_term=args.search
            )
        
        else:
            console.print("[red]❌ Unknown database type. Please specify with -t[/red]")
            return
        
        # Display summary
        console.print()
        unified.display_summary(df, db_type)
        
        # Export if requested
        if args.export:
            df.to_csv(args.export, index=False)
            console.print(f"\n[green]💾 Exported combined data to: {args.export}[/green]")
        
        console.print(f"\n[bold green]✅ Processing complete![/bold green]")
        console.print(f"[cyan]📁 Output directory: {args.output}[/cyan]")
        
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        if args.verbose:
            raise
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
