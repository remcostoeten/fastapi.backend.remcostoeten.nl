#!/usr/bin/env python3
"""
Interactive Analytics Manager
Clean and manage localhost views from production analytics data.
"""

import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from pathlib import Path

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.visitor_service import visitor_service


class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

class AnalyticsManager:
    """Interactive analytics management system"""

    def __init__(self):
        self.original_data = None
        self.backup_data = None

    def print_header(self, title: str):
        """Print a formatted header"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{title:^60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")

    def print_section(self, title: str):
        """Print a section header"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}--- {title} ---{Colors.RESET}")

    def print_success(self, message: str):
        """Print success message"""
        print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")

    def print_error(self, message: str):
        """Print error message"""
        print(f"{Colors.RED}❌ {message}{Colors.RESET}")

    def print_info(self, message: str):
        """Print info message"""
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.RESET}")

    def get_analytics_overview(self) -> Dict:
        """Get comprehensive analytics overview"""

        total_views = len(visitor_service.blog_views)
        localhost_views = [v for v in visitor_service.blog_views if v.get("is_localhost", False)]
        production_views = [v for v in visitor_service.blog_views if not v.get("is_localhost", False)]

        # Get unique visitors
        all_visitors = set(v["visitor_id"] for v in visitor_service.blog_views)
        localhost_visitors = set(v["visitor_id"] for v in localhost_views)
        production_visitors = set(v["visitor_id"] for v in production_views)

        # Group by blog slug
        blog_stats = {}
        for view in visitor_service.blog_views:
            slug = view["blog_slug"]
            if slug not in blog_stats:
                blog_stats[slug] = {
                    "total": 0,
                    "localhost": 0,
                    "production": 0,
                    "unique_visitors": set(),
                    "localhost_visitors": set()
                }

            blog_stats[slug]["total"] += 1
            blog_stats[slug]["unique_visitors"].add(view["visitor_id"])

            if view.get("is_localhost", False):
                blog_stats[slug]["localhost"] += 1
                blog_stats[slug]["localhost_visitors"].add(view["visitor_id"])
            else:
                blog_stats[slug]["production"] += 1

        # Convert sets to counts
        for slug in blog_stats:
            blog_stats[slug]["unique_visitors"] = len(blog_stats[slug]["unique_visitors"])
            blog_stats[slug]["localhost_visitors"] = len(blog_stats[slug]["localhost_visitors"])

        # Time analysis
        if visitor_service.blog_views:
            latest_view = max(v["viewed_at"] for v in visitor_service.blog_views)
            oldest_view = min(v["viewed_at"] for v in visitor_service.blog_views)
            date_range = (latest_view - oldest_view).days
        else:
            latest_view = oldest_view = None
            date_range = 0

        return {
            "total_views": total_views,
            "localhost_views": len(localhost_views),
            "production_views": len(production_views),
            "total_visitors": len(all_visitors),
            "localhost_visitors": len(localhost_visitors),
            "production_visitors": len(production_visitors),
            "blog_stats": blog_stats,
            "latest_view": latest_view,
            "oldest_view": oldest_view,
            "date_range_days": date_range,
            "localhost_percentage": round((len(localhost_views) / total_views * 100), 2) if total_views > 0 else 0
        }

    def display_overview(self, stats: Dict):
        """Display comprehensive analytics overview"""
        self.print_section("📊 Analytics Overview")

        print(f"\n{Colors.BOLD}Overall Statistics:{Colors.RESET}")
        print(f"  Total Views:           {Colors.BOLD}{stats['total_views']:,}{Colors.RESET}")
        print(f"  Production Views:     {Colors.GREEN}{stats['production_views']:,}{Colors.RESET}")
        print(f"  Localhost Views:      {Colors.YELLOW}{stats['localhost_views']:,}{Colors.RESET} ({stats['localhost_percentage']}%)")

        print(f"\n{Colors.BOLD}Visitor Statistics:{Colors.RESET}")
        print(f"  Total Visitors:       {stats['total_visitors']:,}")
        print(f"  Production Visitors:  {stats['production_visitors']:,}")
        print(f"  Localhost Visitors:   {stats['localhost_visitors']:,}")

        print(f"\n{Colors.BOLD}Time Range:{Colors.RESET}")
        if stats['latest_view']:
            print(f"  Oldest View:          {stats['oldest_view'].strftime('%Y-%m-%d %H:%M')}")
            print(f"  Latest View:          {stats['latest_view'].strftime('%Y-%m-%d %H:%M')}")
            print(f"  Data Span:            {stats['date_range_days']} days")

        if stats['localhost_views'] > 0:
            self.print_section("🏠 Localhost Views by Blog")
            print(f"{'Blog Slug':<30} {'Views':<8} {'Pct':<6} {'Unique'}")
            print(f"{'-'*60}")

            # Sort by localhost views (descending)
            sorted_blogs = sorted(stats['blog_stats'].items(),
                                key=lambda x: x[1]['localhost'], reverse=True)

            for slug, data in sorted_blogs:
                if data['localhost'] > 0:
                    percentage = round((data['localhost'] / data['total'] * 100), 1) if data['total'] > 0 else 0
                    print(f"{slug[:28]:<30} {data['localhost']:<8} {percentage:<6.1f}% {data['localhost_visitors']}")

    def display_dry_run_results(self, stats: Dict):
        """Display what would happen during cleanup"""
        self.print_section("🔍 Dry Run Results")

        if stats['localhost_views'] == 0:
            self.print_success("No localhost views found - no cleanup needed!")
            return

        print(f"\n{Colors.YELLOW}Views that would be REMOVED:{Colors.RESET}")
        print(f"  Total Localhost Views: {stats['localhost_views']:,}")
        print(f"  Localhost Visitors:   {stats['localhost_visitors']:,}")

        print(f"\n{Colors.GREEN}Views that would REMAIN:{Colors.RESET}")
        print(f"  Production Views:     {stats['production_views']:,}")
        print(f"  Production Visitors:  {stats['production_visitors']:,}")

        print(f"\n{Colors.BOLD}Impact Summary:{Colors.RESET}")
        print(f"  Views Removed:         {stats['localhost_views']:,} ({stats['localhost_percentage']}%)")
        print(f"  Final View Count:      {stats['production_views']:,}")
        print(f"  Reduction:             {stats['localhost_percentage']}%")

    def display_post_cleanup_stats(self, before_stats: Dict, after_stats: Dict):
        """Display before/after comparison"""
        self.print_section("📈 Before vs After Comparison")

        print(f"\n{Colors.BOLD}{'Metric':<20} {'Before':<12} {'After':<12} {'Change':<12}{Colors.RESET}")
        print(f"{'-'*60}")

        views_removed = before_stats['localhost_views']
        views_change = f"-{views_removed:,}" if views_removed > 0 else "0"

        print(f"{'Total Views':<20} {before_stats['total_views']:<12,} {after_stats['total_views']:<12,} {views_change:<12}")
        print(f"{'Production Views':<20} {before_stats['production_views']:<12,} {after_stats['production_views']:<12,} +{before_stats['localhost_views']:,}")
        print(f"{'Localhost Views':<20} {before_stats['localhost_views']:<12,} {after_stats['localhost_views']:<12,} -{before_stats['localhost_views']:,}")

        visitors_removed = before_stats['localhost_visitors']
        visitors_change = f"-{visitors_removed:,}" if visitors_removed > 0 else "0"

        print(f"{'Total Visitors':<20} {before_stats['total_visitors']:<12,} {after_stats['total_visitors']:<12,} {visitors_change:<12}")
        print(f"{'Production Visitors':<20} {before_stats['production_visitors']:<12,} {after_stats['production_visitors']:<12,} +{before_stats['localhost_visitors']:,}")
        print(f"{'Localhost Visitors':<20} {before_stats['localhost_visitors']:<12,} {after_stats['localhost_visitors']:<12,} -{before_stats['localhost_visitors']:,}")

    def backup_data(self, stats: Dict) -> str:
        """Create backup of current data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"analytics_backup_{timestamp}.json"

        backup_data = {
            "backup_created": datetime.now().isoformat(),
            "backup_reason": "localhost_views_cleanup",
            "statistics": stats,
            "localhost_views": [v for v in visitor_service.blog_views if v.get("is_localhost", False)],
            "total_views_before": len(visitor_service.blog_views)
        }

        with open(filename, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)

        return filename

    def cleanup_localhost_views(self, create_backup: bool = True) -> Tuple[bool, Dict, Dict]:
        """Perform actual cleanup of localhost views"""

        # Get before stats
        before_stats = self.get_analytics_overview()

        if before_stats['localhost_views'] == 0:
            return False, before_stats, before_stats

        # Create backup if requested
        backup_file = None
        if create_backup:
            backup_file = self.backup_data(before_stats)
            self.print_info(f"Backup created: {backup_file}")

        # Store original data for potential restore
        self.original_data = visitor_service.blog_views.copy()

        # Remove localhost views
        original_count = len(visitor_service.blog_views)
        visitor_service.blog_views = [v for v in visitor_service.blog_views if not v.get("is_localhost", False)]
        removed_count = original_count - len(visitor_service.blog_views)

        # Get after stats
        after_stats = self.get_analytics_overview()

        return True, before_stats, after_stats

    def restore_data(self) -> bool:
        """Restore data from backup"""
        if self.original_data is None:
            self.print_error("No backup data available to restore")
            return False

        visitor_service.blog_views = self.original_data.copy()
        self.print_success("Data restored from backup")
        return True

    def export_detailed_report(self, stats: Dict) -> str:
        """Export detailed analytics report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"analytics_report_{timestamp}.json"

        report = {
            "report_generated": datetime.now().isoformat(),
            "report_type": "analytics_overview",
            "summary": {
                "total_views": stats["total_views"],
                "production_views": stats["production_views"],
                "localhost_views": stats["localhost_views"],
                "localhost_percentage": stats["localhost_percentage"],
                "total_visitors": stats["total_visitors"],
                "production_visitors": stats["production_visitors"],
                "localhost_visitors": stats["localhost_visitors"]
            },
            "blog_statistics": stats["blog_stats"],
            "time_analysis": {
                "oldest_view": stats["oldest_view"].isoformat() if stats["oldest_view"] else None,
                "latest_view": stats["latest_view"].isoformat() if stats["latest_view"] else None,
                "date_range_days": stats["date_range_days"]
            },
            "localhost_views_detail": [
                {
                    "id": v["id"],
                    "blog_slug": v["blog_slug"],
                    "viewed_at": v["viewed_at"].isoformat(),
                    "visitor_id": v["visitor_id"]
                }
                for v in visitor_service.blog_views if v.get("is_localhost", False)
            ]
        }

        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        return filename

    def show_main_menu(self):
        """Display main interactive menu"""
        while True:
            stats = self.get_analytics_overview()

            self.print_header("🔧 Analytics Management System")

            # Quick status
            status_color = Colors.GREEN if stats['localhost_views'] == 0 else Colors.YELLOW
            print(f"\n{Colors.BOLD}Current Status:{Colors.RESET}")
            print(f"  Total Views: {stats['total_views']:,}")
            print(f"  Production: {Colors.GREEN}{stats['production_views']:,}{Colors.RESET}")
            print(f"  Localhost: {status_color}{stats['localhost_views']:,}{Colors.RESET} ({stats['localhost_percentage']}%)")

            self.print_section("📋 Menu Options")
            print("1. 📊 Show Detailed Analytics Overview")
            print("2. 🔍 Run Dry-Run Cleanup Analysis")
            print("3. 🧹 Perform Actual Cleanup (with backup)")
            print("4. 📁 Export Detailed Report")
            print("5. 💾 Create Backup Only")
            print("6. 🔄 Restore from Backup")
            print("7. ⚙️  Advanced Options")
            print("0. 🚪 Exit")

            choice = input(f"\n{Colors.CYAN}Enter your choice (0-7): {Colors.RESET}").strip()

            if choice == '1':
                self.display_overview(stats)
                input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")

            elif choice == '2':
                self.display_overview(stats)
                self.display_dry_run_results(stats)
                input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")

            elif choice == '3':
                if stats['localhost_views'] == 0:
                    self.print_success("No localhost views found - cleanup not needed!")
                    input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")
                    continue

                self.display_overview(stats)
                self.display_dry_run_results(stats)

                print(f"\n{Colors.YELLOW}⚠️  WARNING: This will permanently remove {stats['localhost_views']:,} localhost views{Colors.RESET}")
                confirm = input(f"\n{Colors.RED}Type 'DELETE' to confirm cleanup: {Colors.RESET}").strip()

                if confirm == 'DELETE':
                    success, before_stats, after_stats = self.cleanup_localhost_views()
                    if success:
                        self.display_post_cleanup_stats(before_stats, after_stats)
                        self.print_success("Cleanup completed successfully!")
                    else:
                        self.print_warning("No cleanup was performed")
                else:
                    self.print_error("Cleanup cancelled - confirmation not matched")

                input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")

            elif choice == '4':
                self.print_section("📁 Exporting Report")
                filename = self.export_detailed_report(stats)
                self.print_success(f"Report exported to: {filename}")
                input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")

            elif choice == '5':
                self.print_section("💾 Creating Backup")
                filename = self.backup_data(stats)
                self.print_success(f"Backup created: {filename}")
                input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")

            elif choice == '6':
                self.restore_data()
                input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")

            elif choice == '7':
                self.show_advanced_menu()

            elif choice == '0':
                print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.RESET}")
                break

            else:
                self.print_error("Invalid choice. Please enter 0-7.")
                input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")

    def show_advanced_menu(self):
        """Show advanced options menu"""
        while True:
            self.print_header("⚙️ Advanced Options")

            self.print_section("Advanced Menu")
            print("1. 🗑️  Clear All Data (Dangerous!)")
            print("2. 📋 Show Raw Data Structure")
            print("3. 🔍 Search Views by Pattern")
            print("4. 📊 Generate Summary Statistics")
            print("0. 🔙 Back to Main Menu")

            choice = input(f"\n{Colors.CYAN}Enter your choice (0-4): {Colors.RESET}").strip()

            if choice == '1':
                self.print_warning("This will delete ALL analytics data!")
                confirm = input(f"\n{Colors.RED}Type 'DELETE ALL' to confirm: {Colors.RESET}").strip()
                if confirm == 'DELETE ALL':
                    visitor_service.blog_views.clear()
                    self.print_success("All data cleared!")
                else:
                    self.print_error("Operation cancelled")

            elif choice == '2':
                self.print_section("📋 Raw Data Structure")
                if visitor_service.blog_views:
                    print(json.dumps(visitor_service.blog_views[:2], indent=2, default=str))
                    if len(visitor_service.blog_views) > 2:
                        print(f"\n... and {len(visitor_service.blog_views) - 2} more entries")
                else:
                    print("No data available")

            elif choice == '3':
                pattern = input("Enter search pattern (blog slug): ").strip()
                matches = [v for v in visitor_service.blog_views if pattern.lower() in v["blog_slug"].lower()]
                print(f"\nFound {len(matches)} matching views:")
                for view in matches[:5]:
                    print(f"  {view['blog_slug']} - {view['viewed_at']}")
                if len(matches) > 5:
                    print(f"  ... and {len(matches) - 5} more")

            elif choice == '4':
                stats = self.get_analytics_overview()
                self.display_overview(stats)

            elif choice == '0':
                break

            else:
                self.print_error("Invalid choice")

            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")

    def run_auto_mode(self, auto_cleanup: bool = False):
        """Run in automatic mode for Git hooks"""
        stats = self.get_analytics_overview()

        print(f"{Colors.CYAN}🔍 Analytics Auto-Mode{Colors.RESET}")
        print(f"Total Views: {stats['total_views']:,}")
        print(f"Localhost Views: {Colors.YELLOW}{stats['localhost_views']:,}{Colors.RESET} ({stats['localhost_percentage']}%)")

        if stats['localhost_views'] == 0:
            self.print_success("✨ No localhost views found - analytics are clean!")
            return True

        print(f"\n{Colors.YELLOW}⚠️ Found {stats['localhost_views']:,} localhost views to clean{Colors.RESET}")

        if auto_cleanup:
            # Create backup and clean automatically
            backup_file = self.backup_data(stats)
            self.print_info(f"Backup created: {backup_file}")

            success, before_stats, after_stats = self.cleanup_localhost_views(create_backup=False)

            if success:
                self.print_success(f"✅ Cleaned up {stats['localhost_views']:,} localhost views")
                print(f"Remaining views: {after_stats['production_views']:,}")
                return True
            else:
                self.print_error("❌ Cleanup failed")
                return False
        else:
            # Just show what needs to be cleaned
            self.display_dry_run_results(stats)
            return False


def main():
    """Main function"""
    manager = AnalyticsManager()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "auto":
            # Automatic mode for Git hooks
            auto_cleanup = "--cleanup" in sys.argv
            success = manager.run_auto_mode(auto_cleanup=auto_cleanup)
            sys.exit(0 if success else 1)

        elif command == "interactive":
            manager.show_main_menu()

        else:
            print(f"Unknown command: {command}")
            print("Available commands: interactive, auto [--cleanup]")
            sys.exit(1)
    else:
        # Default to interactive mode
        manager.show_main_menu()


if __name__ == "__main__":
    main()