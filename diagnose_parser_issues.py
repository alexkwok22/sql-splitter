#!/usr/bin/env python3
"""
Diagnose Parser Issues - JOIN, WHERE, Field-Table Association

🔍 Analyze why these features are not working correctly
📊 Test individual components to find root causes

Author: AI Assistant
Date: 2025-08-28
"""

import sys
import os
import re
import json

# Add local package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql_splitter'))

def diagnose_parser_issues():
    print("🔍 Parser Issues Diagnostic")
    print("=" * 50)
    
    # Import components
    from sql_splitter.core.sql_parser_ast_v6_0 import SQLParserAST
    from sql_splitter.core.join_handler import JoinHandler, parse_joins_from_sql
    from sql_splitter.core.content_extractor import ContentExtractor
    
    # Test SQL
    test_sql = "SELECT o.order_id, c.customer_name FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.status = 'active'"
    
    print(f"Test SQL: {test_sql}")
    print()
    
    # 1. Test JOIN detection directly
    print("🔧 1. Testing JOIN Handler directly:")
    join_handler = JoinHandler()
    joins = parse_joins_from_sql(test_sql)
    print(f"   Direct JOIN detection: {len(joins)} joins found")
    for i, join in enumerate(joins):
        print(f"   JOIN {i+1}: {join}")
    
    # 2. Test WHERE detection directly  
    print("\n🔧 2. Testing WHERE extraction directly:")
    content_extractor = ContentExtractor()
    where_conditions = content_extractor.extract_where_conditions(test_sql)
    print(f"   Direct WHERE detection: {len(where_conditions)} conditions found")
    for condition in where_conditions:
        print(f"   WHERE: {condition}")
    
    # 3. Test field extraction directly
    print("\n🔧 3. Testing Field extraction directly:")
    fields = content_extractor.extract_fields(test_sql)
    print(f"   Direct field detection: {len(fields)} fields found")
    for field in fields:
        print(f"   Field: {field}")
    
    # 4. Test main parser integration
    print("\n🔧 4. Testing Main Parser integration:")
    parser = SQLParserAST()
    result = parser.parse(test_sql)
    
    parser_fields = result.get('fields', [])
    parser_joins = result.get('joins', [])  
    parser_where = result.get('whereConditions', [])
    
    print(f"   Parser fields: {len(parser_fields)}")
    print(f"   Parser joins: {len(parser_joins)}")
    print(f"   Parser WHERE: {len(parser_where)}")
    
    # 5. Identify integration issues
    print("\n🚨 Issues Found:")
    if len(joins) > 0 and len(parser_joins) == 0:
        print("   ❌ JOIN Handler works but Parser integration fails")
    elif len(joins) == 0:
        print("   ❌ JOIN Handler itself is broken")
    
    if len(where_conditions) > 0 and len(parser_where) == 0:
        print("   ❌ WHERE extraction works but Parser integration fails")  
    elif len(where_conditions) == 0:
        print("   ❌ WHERE extraction itself is broken")
        
    if len(fields) > 0 and len(parser_fields) == 0:
        print("   ❌ Field extraction works but Parser integration fails")
    elif len(fields) == 0:
        print("   ❌ Field extraction itself is broken")
        
    # Check field-table association
    for field in parser_fields:
        if not field.get('table', ''):
            print(f"   ❌ Field '{field.get('field', 'unknown')}' missing table association")
    
    print("\n✅ Diagnostic completed")

if __name__ == "__main__":
    diagnose_parser_issues()
