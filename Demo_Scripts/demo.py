#!/usr/bin/env python3
"""
Example: Using User Behavior Analysis Platform v2.0

This script demonstrates the key capabilities of the new platform.
"""

import asyncio
from pathlib import Path
from datetime import datetime, timedelta
import json

# Import the new modules
from backend.app.core.database.base import DatabaseFactory, ActivitySource
from backend.app.core.database.timeline_parser import TimelineParser
from backend.app.core.database.recall_parser import RecallParser


async def example_1_basic_parsing():
    """Example 1: Basic database parsing with auto-detection."""
    print("=" * 60)
    print("Example 1: Basic Database Parsing")
    print("=" * 60)
    
    # Path to your database
    db_path = Path("path/to/ActivityCache.db")
    
    # Auto-detect database type and create parser
    async with await DatabaseFactory.create_parser(db_path) as parser:
        # Get basic stats
        total_count = await parser.get_activity_count()
        print(f"✓ Database type: {parser.source.value.upper()}")
        print(f"✓ Total activities: {total_count:,}")
        
        # Parse first 10 activities
        print("\nFirst 10 activities:")
        count = 0
        async for activity in parser.parse():
            print(f"  {count + 1}. {activity.timestamp} - {activity.activity_type.value} - {activity.app_name}")
            count += 1
            if count >= 10:
                break
    
    print()


async def example_2_export_formats():
    """Example 2: Export to multiple formats."""
    print("=" * 60)
    print("Example 2: Export to Multiple Formats")
    print("=" * 60)
    
    import pandas as pd
    
    db_path = Path("path/to/ActivityCache.db")
    
    async with await DatabaseFactory.create_parser(db_path) as parser:
        # Collect all activities
        activities = []
        async for activity in parser.parse():
            activities.append(activity.to_dict())
        
        print(f"✓ Parsed {len(activities)} activities")
        
        # Export to CSV
        df = pd.DataFrame(activities)
        df.to_csv("output/activities.csv", index=False)
        print("✓ Exported to CSV: output/activities.csv")
        
        # Export to JSON
        with open("output/activities.json", "w") as f:
            json.dump(activities, f, indent=2, default=str)
        print("✓ Exported to JSON: output/activities.json")
        
        # Export to Parquet (best for large datasets)
        df.to_parquet("output/activities.parquet", index=False)
        print("✓ Exported to Parquet: output/activities.parquet")
    
    print()


async def example_3_filtering():
    """Example 3: Filter activities by criteria."""
    print("=" * 60)
    print("Example 3: Filtering Activities")
    print("=" * 60)
    
    db_path = Path("path/to/ActivityCache.db")
    
    async with await DatabaseFactory.create_parser(db_path) as parser:
        # Filter 1: Only Chrome activities
        print("Chrome activities:")
        chrome_count = 0
        async for activity in parser.parse():
            if activity.app_name and "chrome" in activity.app_name.lower():
                print(f"  • {activity.timestamp} - {activity.activity_type.value}")
                chrome_count += 1
                if chrome_count >= 5:
                    break
        
        # Filter 2: Activities in last 24 hours
        print("\nActivities in last 24 hours:")
        yesterday = datetime.now() - timedelta(days=1)
        recent_count = 0
        
        async with await DatabaseFactory.create_parser(db_path) as parser2:
            async for activity in parser2.parse():
                if activity.timestamp and activity.timestamp > yesterday:
                    print(f"  • {activity.timestamp} - {activity.app_name}")
                    recent_count += 1
                    if recent_count >= 5:
                        break
    
    print()


async def example_4_analytics():
    """Example 4: Generate analytics and insights."""
    print("=" * 60)
    print("Example 4: Analytics and Insights")
    print("=" * 60)
    
    from collections import Counter
    
    db_path = Path("path/to/ActivityCache.db")
    
    async with await DatabaseFactory.create_parser(db_path) as parser:
        activities = []
        async for activity in parser.parse():
            activities.append(activity)
        
        # Activity type distribution
        type_counts = Counter(a.activity_type.value for a in activities)
        print("Activity Type Distribution:")
        for activity_type, count in type_counts.most_common():
            percentage = (count / len(activities)) * 100
            print(f"  • {activity_type}: {count} ({percentage:.1f}%)")
        
        # Top 10 apps
        app_counts = Counter(a.app_name for a in activities if a.app_name)
        print("\nTop 10 Applications:")
        for i, (app, count) in enumerate(app_counts.most_common(10), 1):
            print(f"  {i}. {app}: {count} activities")
        
        # Active hours analysis
        hours = [a.timestamp.hour for a in activities if a.timestamp]
        hour_counts = Counter(hours)
        print("\nMost Active Hours:")
        for hour, count in hour_counts.most_common(5):
            print(f"  • {hour:02d}:00 - {count} activities")
        
        # Time range
        timestamps = [a.timestamp for a in activities if a.timestamp]
        if timestamps:
            print(f"\nTime Range:")
            print(f"  • First activity: {min(timestamps)}")
            print(f"  • Last activity: {max(timestamps)}")
            print(f"  • Duration: {max(timestamps) - min(timestamps)}")
    
    print()


async def example_5_forensics():
    """Example 5: Forensic timeline reconstruction."""
    print("=" * 60)
    print("Example 5: Forensic Timeline Reconstruction")
    print("=" * 60)
    
    db_path = Path("path/to/ActivityCache.db")
    
    # Define incident time window
    incident_start = datetime(2024, 10, 1, 14, 0, 0)
    incident_end = datetime(2024, 10, 1, 16, 0, 0)
    
    print(f"Investigating incident from {incident_start} to {incident_end}")
    print()
    
    async with await DatabaseFactory.create_parser(db_path) as parser:
        incident_activities = []
        
        async for activity in parser.parse():
            if activity.timestamp and incident_start <= activity.timestamp <= incident_end:
                incident_activities.append(activity)
        
        # Sort by timestamp
        incident_activities.sort(key=lambda x: x.timestamp)
        
        print(f"Found {len(incident_activities)} activities during incident window:")
        for activity in incident_activities[:20]:  # Show first 20
            print(f"  • {activity.timestamp} | {activity.activity_type.value:15} | {activity.app_name or 'N/A':20} | {activity.description or ''}")
        
        # Check for suspicious patterns
        print("\nSuspicious Pattern Analysis:")
        
        # 1. Clipboard usage
        clipboard_activities = [a for a in incident_activities if a.activity_type.value == "clipboard"]
        if clipboard_activities:
            print(f"  ⚠ Found {len(clipboard_activities)} clipboard operations")
        
        # 2. Unusual file access
        suspicious_files = ["password", "confidential", "secret", "private"]
        for activity in incident_activities:
            if activity.content:
                for keyword in suspicious_files:
                    if keyword in activity.content.lower():
                        print(f"  ⚠ Suspicious file access: {activity.content}")
        
        # 3. Activity during off-hours
        for activity in incident_activities:
            if activity.timestamp and (activity.timestamp.hour < 6 or activity.timestamp.hour > 22):
                print(f"  ⚠ Off-hours activity: {activity.timestamp} - {activity.app_name}")
    
    print()


async def example_6_recall_database():
    """Example 6: Working with Windows Recall database."""
    print("=" * 60)
    print("Example 6: Windows Recall Database Analysis")
    print("=" * 60)
    
    db_path = Path("path/to/ukg.db")
    
    if not db_path.exists():
        print("⚠ Windows Recall database not found (requires Windows 11 with Recall)")
        print("  Database should be at: C:\\Users\\%username%\\AppData\\Local\\CoreAIPlatform.00\\UKP\\ukg.db")
        return
    
    async with await DatabaseFactory.create_parser(db_path) as parser:
        print(f"✓ Database type: {parser.source.value.upper()}")
        
        # Parse first 5 window captures
        print("\nFirst 5 window captures:")
        count = 0
        async for activity in parser.parse():
            print(f"\n  Capture {count + 1}:")
            print(f"    • Timestamp: {activity.timestamp}")
            print(f"    • App: {activity.app_name}")
            print(f"    • Window Title: {activity.content}")
            print(f"    • Has Screenshot: {activity.screenshot_blob is not None}")
            print(f"    • Has OCR Text: {activity.ocr_text is not None}")
            
            if activity.ocr_text:
                # Show first 100 chars of OCR text
                preview = activity.ocr_text[:100] + "..." if len(activity.ocr_text) > 100 else activity.ocr_text
                print(f"    • OCR Preview: {preview}")
            
            count += 1
            if count >= 5:
                break
        
        # Search by OCR text (if RecallParser)
        if isinstance(parser, RecallParser):
            print("\nSearching for 'password' in OCR text:")
            search_count = 0
            async for activity in parser.search_by_ocr_text("password"):
                print(f"  • Found in {activity.app_name} at {activity.timestamp}")
                search_count += 1
                if search_count >= 3:
                    break
    
    print()


async def example_7_api_usage():
    """Example 7: Using the REST API programmatically."""
    print("=" * 60)
    print("Example 7: REST API Usage")
    print("=" * 60)
    
    import httpx
    
    base_url = "http://localhost:8000"
    db_path = "path/to/ActivityCache.db"
    
    print("Note: Make sure the API server is running: uba serve --port 8000")
    print()
    
    async with httpx.AsyncClient() as client:
        try:
            # 1. Health check
            response = await client.get(f"{base_url}/health")
            print(f"✓ API Status: {response.json()['status']}")
            
            # 2. Get database stats
            response = await client.get(
                f"{base_url}/api/activities/stats",
                params={"database_path": db_path}
            )
            stats = response.json()
            print(f"✓ Database: {stats['database_type']}")
            print(f"✓ Activities: {stats['total_activities']:,}")
            
            # 3. Get analytics summary
            response = await client.get(
                f"{base_url}/api/analytics/summary",
                params={"database_path": db_path}
            )
            summary = response.json()
            print(f"\nAnalytics Summary:")
            print(f"  • Unique Apps: {summary['unique_apps']}")
            print(f"  • Most Active Hours: {summary['most_active_hours']}")
            print(f"  • Top App: {summary['top_apps'][0]['app_name']}")
            
            # 4. Get forensic timeline
            response = await client.post(
                f"{base_url}/api/forensics/timeline",
                json={
                    "database_path": db_path,
                    "start_time": "2024-10-01T00:00:00Z",
                    "end_time": "2024-10-01T23:59:59Z",
                    "include_context": True
                }
            )
            timeline = response.json()
            print(f"\nForensic Timeline:")
            print(f"  • Activities Found: {timeline['total_count']}")
            
        except httpx.ConnectError:
            print("✗ Could not connect to API server")
            print("  Start server with: uba serve --port 8000")
    
    print()


async def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("User Behavior Analysis Platform v2.0 - Examples")
    print("=" * 60 + "\n")
    
    examples = [
        ("Basic Parsing", example_1_basic_parsing),
        ("Export Formats", example_2_export_formats),
        ("Filtering", example_3_filtering),
        ("Analytics", example_4_analytics),
        ("Forensics", example_5_forensics),
        ("Recall Database", example_6_recall_database),
        ("API Usage", example_7_api_usage),
    ]
    
    for name, func in examples:
        try:
            await func()
        except FileNotFoundError:
            print(f"⚠ Skipping '{name}' - Database file not found")
            print(f"  Update the db_path in the example function\n")
        except Exception as e:
            print(f"✗ Error in '{name}': {e}\n")
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
