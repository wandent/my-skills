#!/usr/bin/env python3
"""
Session History Search Backend

Searches through Copilot chat session folders for content, responses, and artifacts.
Supports temporal filtering (relative and absolute dates) and context extraction.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import statistics

@dataclass
class SearchMatch:
    """Represents a single search match"""
    file_path: str
    session_id: str
    file_type: str
    created_date: str
    modified_date: str
    relevance_score: float
    excerpt: str
    line_number: int
    conversation_summary: str


class SessionHistorySearcher:
    """Search chat session history for documents and artifacts"""
    
    SUPPORTED_EXTENSIONS = {'.md', '.txt', '.json'}
    SESSION_STATE_ROOT = Path.home() / ".copilot" / "session-state"
    
    def __init__(self):
        self.results: List[SearchMatch] = []
        
    def parse_temporal_filter(self, temporal_spec: str) -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Parse temporal filter specifications into date range.
        
        Examples:
        - "last 3 days" -> (now - 3 days, now)
        - "last week" -> (now - 7 days, now)
        - "last month" -> (now - 30 days, now)
        - "between May 1 and May 15" -> (May 1, May 15)
        - "after April 20" -> (April 20, now)
        - "before June 1" -> (None, June 1)
        - "March" -> (Mar 1, Mar 31)
        """
        today = datetime.now()
        
        if not temporal_spec or temporal_spec.lower() == "all":
            return None, None
        
        # Relative dates: "last X days/weeks/months"
        match = re.match(r'last\s+(\d+)\s+(day|week|month|hour)s?', temporal_spec, re.IGNORECASE)
        if match:
            amount = int(match.group(1))
            unit = match.group(2).lower()
            
            if unit == 'hour':
                delta = timedelta(hours=amount)
            elif unit == 'day':
                delta = timedelta(days=amount)
            elif unit == 'week':
                delta = timedelta(days=amount * 7)
            elif unit == 'month':
                delta = timedelta(days=amount * 30)  # Approximate
            
            start_date = today - delta
            return start_date, today
        
        # Special: "last week", "last month"
        if temporal_spec.lower() == "last week":
            return today - timedelta(days=7), today
        elif temporal_spec.lower() == "last month":
            return today - timedelta(days=30), today
        elif temporal_spec.lower() == "last 2 weeks":
            return today - timedelta(days=14), today
        elif temporal_spec.lower() == "past 2 weeks":
            return today - timedelta(days=14), today
        
        # Month name: "March", "May", etc.
        month_match = re.match(r'(\w+)', temporal_spec, re.IGNORECASE)
        if month_match:
            month_name = month_match.group(1).capitalize()
            try:
                month_num = datetime.strptime(month_name, "%B").month
                year = today.year
                # If month is in future, assume previous year
                if month_num > today.month:
                    year -= 1
                start = datetime(year, month_num, 1)
                # End of month
                if month_num == 12:
                    end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
                else:
                    end = datetime(year, month_num + 1, 1) - timedelta(seconds=1)
                return start, end
            except ValueError:
                pass
        
        # Date range: "between May 1 and May 15"
        between_match = re.search(r'between\s+(\w+\s+\d+)\s+and\s+(\w+\s+\d+)', temporal_spec, re.IGNORECASE)
        if between_match:
            try:
                start_str = between_match.group(1)
                end_str = between_match.group(2)
                year = today.year
                start = datetime.strptime(f"{start_str} {year}", "%B %d %Y")
                end = datetime.strptime(f"{end_str} {year}", "%B %d %Y")
                return start, end
            except ValueError:
                pass
        
        # "after DATE" or "since DATE"
        after_match = re.search(r'(?:after|since)\s+(\w+\s+\d+)', temporal_spec, re.IGNORECASE)
        if after_match:
            try:
                date_str = after_match.group(1)
                year = today.year
                start = datetime.strptime(f"{date_str} {year}", "%B %d %Y")
                return start, today
            except ValueError:
                pass
        
        # "before DATE" or "until DATE"
        before_match = re.search(r'(?:before|until)\s+(\w+\s+\d+)', temporal_spec, re.IGNORECASE)
        if before_match:
            try:
                date_str = before_match.group(1)
                year = today.year
                end = datetime.strptime(f"{date_str} {year}", "%B %d %Y")
                return None, end
            except ValueError:
                pass
        
        return None, None
    
    def is_within_date_range(self, file_path: Path, start_date: Optional[datetime], end_date: Optional[datetime]) -> bool:
        """Check if file modification date falls within the specified range"""
        if start_date is None and end_date is None:
            return True
        
        try:
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            if start_date and mod_time < start_date:
                return False
            if end_date and mod_time > end_date:
                return False
            return True
        except (OSError, ValueError):
            return False
    
    def calculate_relevance_score(self, match_count: int, recency_days: float) -> float:
        """
        Calculate relevance score (0-100) based on match count and recency.
        Recent files with more matches score higher.
        """
        # Match count component (0-50)
        match_score = min(match_count * 10, 50)
        
        # Recency component (0-50, newer = higher)
        # Files from today: 50, 1 month ago: 25, older: lower
        days_old = max(recency_days, 0)
        if days_old <= 1:
            recency_score = 50
        elif days_old <= 7:
            recency_score = 40
        elif days_old <= 30:
            recency_score = 25
        elif days_old <= 90:
            recency_score = 15
        else:
            recency_score = 5
        
        return match_score + recency_score
    
    def extract_excerpt(self, content: str, keywords: List[str], max_length: int = 200) -> Tuple[str, int]:
        """
        Extract a relevant excerpt containing keywords with context.
        Returns (excerpt, line_number)
        """
        lines = content.split('\n')
        
        # Find line with best keyword match
        best_line_idx = 0
        best_match_count = 0
        
        for idx, line in enumerate(lines):
            match_count = sum(1 for kw in keywords if kw.lower() in line.lower())
            if match_count > best_match_count:
                best_match_count = match_count
                best_line_idx = idx
        
        # Extract context around best match
        start_idx = max(0, best_line_idx - 1)
        end_idx = min(len(lines), best_line_idx + 3)
        excerpt_lines = lines[start_idx:end_idx]
        
        excerpt = '\n'.join(excerpt_lines)
        if len(excerpt) > max_length:
            excerpt = excerpt[:max_length] + "..."
        
        return excerpt, best_line_idx + 1
    
    def extract_conversation_context(self, session_folder: Path) -> str:
        """
        Extract conversation context from session metadata.
        Looks for checkpoint summaries or conversation metadata.
        """
        context = ""
        
        # Try to read checkpoint index
        checkpoint_index = session_folder / "checkpoints" / "index.md"
        if checkpoint_index.exists():
            try:
                with open(checkpoint_index, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Extract first few lines as context
                    lines = content.split('\n')[:3]
                    context = '\n'.join(lines).strip()
            except Exception:
                pass
        
        # Try to read plan.md for context
        if not context:
            plan_file = session_folder / "plan.md"
            if plan_file.exists():
                try:
                    with open(plan_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Extract first meaningful section
                        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
                        context = lines[0] if lines else ""
                except Exception:
                    pass
        
        return context or "Session context not available"
    
    def search_files(self, keywords: List[str], temporal_filter: Optional[str] = None, file_type_filter: Optional[str] = None) -> List[SearchMatch]:
        """
        Search session files for keywords with optional temporal and file type filtering.
        
        Args:
            keywords: List of search terms
            temporal_filter: Temporal specification (e.g., "last month", "between May 1 and May 15")
            file_type_filter: File type filter (e.g., ".md", ".json", or None for all)
        
        Returns:
            List of SearchMatch results sorted by relevance
        """
        self.results = []
        
        if not self.SESSION_STATE_ROOT.exists():
            raise FileNotFoundError(f"Session state directory not found: {self.SESSION_STATE_ROOT}")
        
        # Parse date range
        start_date, end_date = self.parse_temporal_filter(temporal_filter or "")
        
        # Normalize file type filter
        if file_type_filter and not file_type_filter.startswith('.'):
            file_type_filter = f".{file_type_filter}"
        
        # Search all session folders
        session_folders = [d for d in self.SESSION_STATE_ROOT.iterdir() if d.is_dir()]
        
        for session_folder in session_folders:
            session_id = session_folder.name
            
            # Recursively search for supported files
            for file_path in session_folder.rglob('*'):
                if not file_path.is_file():
                    continue
                
                # Check file extension
                if file_path.suffix not in self.SUPPORTED_EXTENSIONS:
                    continue
                
                # Apply file type filter
                if file_type_filter and file_path.suffix != file_type_filter:
                    continue
                
                # Check temporal filter
                if not self.is_within_date_range(file_path, start_date, end_date):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Search for keywords (case-insensitive)
                    match_count = 0
                    for keyword in keywords:
                        match_count += content.lower().count(keyword.lower())
                    
                    if match_count == 0:
                        # Also check filename
                        filename_matches = sum(1 for kw in keywords if kw.lower() in file_path.name.lower())
                        if filename_matches == 0:
                            continue
                        match_count = filename_matches
                    
                    # Extract excerpt and line number
                    excerpt, line_num = self.extract_excerpt(content, keywords)
                    
                    # Calculate recency
                    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    recency_days = (datetime.now() - mod_time).days
                    
                    # Calculate relevance score
                    score = self.calculate_relevance_score(match_count, recency_days)
                    
                    # Extract conversation context
                    context = self.extract_conversation_context(session_folder)
                    
                    # Get creation date
                    create_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                    
                    match = SearchMatch(
                        file_path=str(file_path.relative_to(self.SESSION_STATE_ROOT)),
                        session_id=session_id,
                        file_type=file_path.suffix,
                        created_date=create_time.isoformat(),
                        modified_date=mod_time.isoformat(),
                        relevance_score=score,
                        excerpt=excerpt,
                        line_number=line_num,
                        conversation_summary=context
                    )
                    self.results.append(match)
                
                except (UnicodeDecodeError, OSError, IOError):
                    # Skip files that can't be read
                    continue
        
        # Sort by relevance score (descending) then by modified date (descending)
        self.results.sort(key=lambda x: (-x.relevance_score, -datetime.fromisoformat(x.modified_date).timestamp()))
        
        return self.results
    
    def generate_summary(self, output_path: Path, keywords: List[str], temporal_filter: Optional[str] = None) -> Path:
        """
        Generate a markdown summary of search results.
        
        Args:
            output_path: Path to save the summary markdown file
            keywords: Search keywords
            temporal_filter: Temporal filter used
        
        Returns:
            Path to the generated summary file
        """
        output_path = output_path / f"session_search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Session History Search Results\n\n")
            f.write(f"**Search Date:** {datetime.now().isoformat()}\n\n")
            f.write(f"**Keywords:** {', '.join(keywords)}\n")
            if temporal_filter:
                f.write(f"**Time Filter:** {temporal_filter}\n")
            f.write(f"**Total Matches:** {len(self.results)}\n\n")
            
            if not self.results:
                f.write("No matches found.\n")
                return output_path
            
            f.write("## Results\n\n")
            f.write("| File | Type | Modified | Score | Session |\n")
            f.write("|------|------|----------|-------|----------|\n")
            
            for match in self.results:
                mod_date = datetime.fromisoformat(match.modified_date).strftime("%Y-%m-%d %H:%M")
                f.write(f"| `{match.file_path}` | {match.file_type} | {mod_date} | {match.relevance_score:.1f} | {match.session_id} |\n")
            
            f.write("\n## Details\n\n")
            
            for i, match in enumerate(self.results, 1):
                f.write(f"### Result {i}: {match.file_path}\n\n")
                f.write(f"**Session:** `{match.session_id}`\n")
                f.write(f"**Created:** {datetime.fromisoformat(match.created_date).strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Modified:** {datetime.fromisoformat(match.modified_date).strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Relevance Score:** {match.relevance_score:.1f}/100\n")
                f.write(f"**Type:** {match.file_type}\n\n")
                
                f.write(f"**Conversation Context:** {match.conversation_summary}\n\n")
                
                f.write("**Excerpt:**\n```\n")
                f.write(match.excerpt)
                f.write("\n```\n\n")
        
        return output_path


def main():
    """Example usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python query_session.py <keywords> [--time <filter>] [--type <.md|.txt|.json>]")
        sys.exit(1)
    
    keywords = sys.argv[1].split()
    temporal_filter = None
    file_type = None
    
    # Parse optional arguments
    if '--time' in sys.argv:
        idx = sys.argv.index('--time')
        if idx + 1 < len(sys.argv):
            temporal_filter = sys.argv[idx + 1]
    
    if '--type' in sys.argv:
        idx = sys.argv.index('--type')
        if idx + 1 < len(sys.argv):
            file_type = sys.argv[idx + 1]
    
    searcher = SessionHistorySearcher()
    results = searcher.search_files(keywords, temporal_filter, file_type)
    
    print(f"Found {len(results)} matches")
    for result in results[:5]:
        print(f"\n  {result.file_path}")
        print(f"    Score: {result.relevance_score:.1f}, Modified: {result.modified_date}")
    
    # Generate summary
    output_file = searcher.generate_summary(Path.cwd(), keywords, temporal_filter)
    print(f"\nSummary saved to: {output_file}")


if __name__ == "__main__":
    main()
