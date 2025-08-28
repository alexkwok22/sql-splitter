#!/usr/bin/env python3
"""
Local Package Test - sql-splitter
Compare local package vs PyPI package output
"""

import json
import sys
import os

def test_local_package():
    print("🔍 Local Package Test - sql-splitter")
    print("=" * 50)
    
    # Add local package to path (import from local directory, not PyPI)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql_splitter'))
    
    # Import from LOCAL package
    from sql_splitter.core.sql_parser_ast_v6_0 import SQLParserAST
    
    print("✅ Imported from LOCAL package")
    print(f"Local package path: {os.path.dirname(__file__)}/sql_splitter")
    
    # Test same queries as PyPI version
    test_queries = [
        {
            "name": "Simple SELECT",
            "sql": "SELECT customer_id, first_name, last_name FROM customers WHERE status = 'active'"
        },
        {
            "name": "Complex Momo Query (shortened)",
            "sql": """select `mt_item`.`DetailsID` AS `DetailsID`, `mt_item`.`iType` AS `iType`, `mv_order`.`Customer` AS `Customer` from `mt_item` join `mv_order` on(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`) where `mt_item`.`iDeleted` < 1"""
        }
    ]
    
    parser = SQLParserAST()
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"📋 Test {i}: {test['name']}")
        print(f"{'=' * 60}")
        print(f"📝 SQL Query:")
        print(test['sql'])
        
        try:
            # Parse the query
            result = parser.parse(test['sql'])
            
            print(f"\n🔍 LOCAL Package JSON Output:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"❌ Error parsing query: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'=' * 60}")
    print("🔍 Local package test completed")
    print("👀 Compare outputs with PyPI version")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    test_local_package()
