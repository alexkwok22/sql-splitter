#!/usr/bin/env python3
"""
Regression Diagnostic Script

🚨 Diagnose why parser suddenly stopped extracting fields, joins, and WHERE conditions
🔍 Compare working vs failing scenarios to identify root cause

Author: AI Assistant
Date: 2025-08-28
"""

import os
import sys
import json
import traceback

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql_splitter'))

from sql_splitter.core.sql_parser_ast_v6_0 import SQLParserAST
from sql_splitter.core.content_extractor import ContentExtractor

def diagnose_regression():
    """🚨 Diagnose the regression in parser functionality"""
    print("🚨 Parser Regression Diagnostic")
    print("=" * 50)
    
    # Test SQL that should work
    test_sql = """
    select date_format(`mt_item`.`iCreateT`,'%Y-%m') AS `i_month`,`mt_item`.`DetailsID` AS `DetailsID`,`mt_item`.`Details_OrderID` AS `Details_OrderID`,`mt_item`.`iType` AS `iType`,`mt_item`.`iDesc` AS `iDesc`,`mt_item`.`iLink` AS `iLink`,`mt_item`.`iQty` AS `iQty`,`mt_item`.`iPrice` AS `iPrice`,`mt_item`.`iStatus` AS `iStatus`,`mt_item`.`iUpdateT` AS `iUpdateT`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,`mv_item_status_desc`.`Remarks` AS `Remarks`,`mv_order`.`Customer` AS `Customer`,`mv_order`.`Order_Status_Name` AS `Order_status_name`,`mv_order`.`Order_Status` AS `Order_Status`,`mt_item`.`iPic` AS `iPic`,`mt_item`.`igroup` AS `iGroup`,`mt_item`.`iTrack` AS `iTrack`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from (((`mt_item` join `mv_order` on(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`)) left join `mv_item_status_desc` on(`mt_item`.`iType` = `mv_item_status_desc`.`Item_Type`)) left join `mv_item_type_desc` on(`mt_item`.`iType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_item`.`iDeleted` < 1
    """
    
    print("🔧 Step 1: Test main parser directly")
    parser = SQLParserAST()
    result = parser.parse(test_sql)
    
    print(f"   📊 Success: {result.get('success', False)}")
    print(f"   📊 Tables: {len(result.get('tables', []))} -> {result.get('tables', [])}")
    print(f"   📊 JOINs: {len(result.get('joins', []))}")
    print(f"   📊 Fields: {len(result.get('fields', []))}")
    print(f"   📊 WHERE: {len(result.get('whereConditions', []))}")
    
    print("\n🔧 Step 2: Test ContentExtractor directly")
    extractor = ContentExtractor()
    
    # Test field extraction
    fields = extractor.extract_fields(test_sql)
    where_conditions = extractor.extract_where_conditions(test_sql)
    
    print(f"   📊 Direct field extraction: {len(fields)} fields")
    print(f"   📊 Direct WHERE extraction: {len(where_conditions)} conditions")
    
    if len(fields) > 0:
        print(f"      📝 Sample field: {fields[0]}")
    if len(where_conditions) > 0:
        print(f"      📝 WHERE: {where_conditions[0]}")
    
    print("\n🔧 Step 3: Test component integration path")
    
    # Step through parser phases manually
    parser._reset_state()
    parser.original_sql = test_sql
    normalized_sql = parser._normalize_sql(test_sql)
    
    print(f"   📊 Normalized SQL length: {len(normalized_sql)}")
    print(f"   📊 Parser state reset: OK")
    
    # Build AST tree
    ast_tree = parser._build_ast_tree(normalized_sql)
    print(f"   📊 AST tree built: OK")
    print(f"   📊 Table aliases after AST: {len(parser.table_aliases)} -> {parser.table_aliases}")
    
    # Test content extraction phase
    parser.content_extractor.set_context(
        parser.table_aliases, 
        parser.database_name, 
        parser.detected_databases
    )
    
    # Test each extraction step
    group_by_fields = parser.content_extractor.extract_group_by_fields(normalized_sql)
    fields = parser.content_extractor.extract_fields(normalized_sql, group_by_fields)
    where_conditions = parser.content_extractor.extract_where_conditions(normalized_sql)
    
    print(f"   📊 Group BY fields: {len(group_by_fields)}")
    print(f"   📊 Content extractor fields: {len(fields)}")
    print(f"   📊 Content extractor WHERE: {len(where_conditions)}")
    
    # Test AST extraction methods
    tables = parser._extract_tables_from_ast(ast_tree)
    joins = parser._extract_joins_from_ast(ast_tree)
    
    print(f"   📊 AST extracted tables: {len(tables)} -> {tables}")
    print(f"   📊 AST extracted JOINs: {len(joins)}")
    
    print("\n🔧 Step 4: Compare with working test data")
    
    # Load previous working results
    if os.path.exists('test_original_sql_results.json'):
        with open('test_original_sql_results.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        
        if 'detailed_results' in old_data:
            momo_mv_item = None
            for result in old_data['detailed_results']:
                if result.get('query_name') == 'momo_mv_item':
                    momo_mv_item = result
                    break
            
            if momo_mv_item:
                old_output = momo_mv_item.get('parser_output', {})
                print(f"   📊 Previous fields: {len(old_output.get('fields', []))}")
                print(f"   📊 Previous tables: {len(old_output.get('tables', []))}")
                print(f"   📊 Previous JOINs: {len(old_output.get('joins', []))}")
                print(f"   📊 Previous WHERE: {len(old_output.get('whereConditions', []))}")
                
                if len(old_output.get('fields', [])) > 0:
                    print(f"      📝 Previous field sample: {old_output['fields'][0]}")
    
    print("\n🎯 Root Cause Analysis")
    print("=" * 30)
    
    # Analyze the differences
    issues = []
    
    if len(fields) == 0:
        issues.append("❌ ContentExtractor.extract_fields() returns empty array")
    else:
        issues.append("✅ ContentExtractor.extract_fields() works correctly")
    
    if len(where_conditions) == 0:
        issues.append("❌ ContentExtractor.extract_where_conditions() returns empty array")
    else:
        issues.append("✅ ContentExtractor.extract_where_conditions() works correctly")
    
    if len(tables) <= 1:
        issues.append("❌ AST table extraction returns insufficient tables")
    else:
        issues.append("✅ AST table extraction works correctly")
    
    if len(joins) == 0:
        issues.append("❌ AST JOIN extraction returns empty array")
    else:
        issues.append("✅ AST JOIN extraction works correctly")
    
    for issue in issues:
        print(f"   {issue}")
    
    print(f"\n🔧 Next Steps:")
    if len(fields) == 0:
        print("   1. Debug ContentExtractor.extract_fields() method")
        print("   2. Check field extraction regex patterns")
    if len(where_conditions) == 0:
        print("   3. Debug WHERE condition extraction logic")
    if len(joins) == 0:
        print("   4. Debug AST JOIN extraction and extracted_joins storage")
    if len(tables) <= 1:
        print("   5. Debug table extraction and extracted_tables storage")

if __name__ == "__main__":
    try:
        diagnose_regression()
    except Exception as e:
        print(f"\n❌ Diagnostic failed: {str(e)}")
        traceback.print_exc()
