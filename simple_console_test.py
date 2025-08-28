#!/usr/bin/env python3
"""
Simple Console Test for sql-splitter v6.1.0
Print JSON output to console for manual inspection
"""

import json

def test_simple_query():
    print("🔍 Simple Console Test - sql-splitter v6.1.0")
    print("=" * 50)
    
    # Import package
    from sql_splitter import SQLParserAST
    from sql_splitter import __version__
    print(f"Version: {__version__}")
    
    # Test simple query
    sql = "SELECT customer_id, first_name, last_name FROM customers WHERE status = 'active'"
    print(f"\nSQL Query:\n{sql}")
    
    # Parse and display result  
    parser = SQLParserAST()
    result = parser.parse(sql)
    
    print(f"\nJSON Output:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_simple_query()
