#!/usr/bin/env python3
"""
Emergency Fix Diagnostic - SQLParserAST v6.0

🚨 Quick diagnosis of why all output arrays are empty
🎯 Find and fix the exact integration point causing data loss

Author: AI Assistant
Date: 2025-08-28
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql_splitter'))

from sql_splitter.core.sql_parser_ast_v6_0 import SQLParserAST
from sql_splitter.core.content_extractor import ContentExtractor

def emergency_diagnostic():
    """🚨 Emergency diagnostic to find root cause"""
    print("🚨 EMERGENCY DIAGNOSTIC - SQLParserAST v6.0")
    print("=" * 60)
    
    # Simple test SQL
    test_sql = "SELECT mt_item.DetailsID, mt_item.iType FROM mt_item WHERE mt_item.iDeleted < 1"
    
    print("🔧 Step 1: Test ContentExtractor directly")
    extractor = ContentExtractor()
    
    # Test direct extraction
    fields = extractor.extract_fields(test_sql)
    where_conditions = extractor.extract_where_conditions(test_sql)
    
    print(f"   📊 Direct fields: {len(fields)}")
    print(f"   📊 Direct WHERE: {len(where_conditions)}")
    
    if fields:
        print(f"      📝 Field sample: {fields[0]}")
    if where_conditions:
        print(f"      📝 WHERE sample: {where_conditions[0]}")
    
    print("\n🔧 Step 2: Test main parser")
    parser = SQLParserAST()
    result = parser.parse(test_sql)
    
    print(f"   📊 Parser success: {result.get('success', False)}")
    print(f"   📊 Parser fields: {len(result.get('fields', []))}")
    print(f"   📊 Parser tables: {len(result.get('tables', []))}")
    print(f"   📊 Parser joins: {len(result.get('joins', []))}")
    print(f"   📊 Parser WHERE: {len(result.get('whereConditions', []))}")
    
    print("\n🔧 Step 3: Step through parser manually")
    parser._reset_state()
    parser.original_sql = test_sql
    normalized_sql = parser._normalize_sql(test_sql)
    
    # Build AST
    ast_tree = parser._build_ast_tree(normalized_sql)
    
    # Set context
    parser.content_extractor.set_context(
        parser.table_aliases, 
        parser.database_name, 
        parser.detected_databases
    )
    
    # Test content extraction step by step
    group_by_fields = parser.content_extractor.extract_group_by_fields(normalized_sql)
    manual_fields = parser.content_extractor.extract_fields(normalized_sql, group_by_fields)
    manual_where = parser.content_extractor.extract_where_conditions(normalized_sql)
    
    print(f"   📊 Manual fields: {len(manual_fields)}")
    print(f"   📊 Manual WHERE: {len(manual_where)}")
    
    # Test final aggregation
    tables = parser._extract_tables_from_ast(ast_tree)
    joins = parser._extract_joins_from_ast(ast_tree)
    
    print(f"   📊 AST tables: {len(tables)} -> {tables}")
    print(f"   📊 AST joins: {len(joins)}")
    
    # Test direct aggregation call
    final_result = parser.content_extractor.create_expect_md_output(
        tables, joins, manual_fields, manual_where
    )
    
    print(f"\n📊 Final aggregation result:")
    print(f"   📊 Final fields: {len(final_result.get('fields', []))}")
    print(f"   📊 Final tables: {len(final_result.get('tables', []))}")
    print(f"   📊 Final joins: {len(final_result.get('joins', []))}")
    print(f"   📊 Final WHERE: {len(final_result.get('whereConditions', []))}")
    
    # Show the issue
    if len(manual_fields) > 0 and len(final_result.get('fields', [])) == 0:
        print("\n🚨 ROOT CAUSE FOUND: Manual extraction works but final aggregation fails!")
    elif len(manual_fields) == 0:
        print("\n🚨 ROOT CAUSE FOUND: ContentExtractor.extract_fields() fails!")
    else:
        print("\n✅ Cannot reproduce the issue - something else is wrong")

if __name__ == "__main__":
    emergency_diagnostic()
