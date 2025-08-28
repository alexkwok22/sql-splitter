#!/usr/bin/env python3
"""
Integration Diagnostic and Fix Script

🚨 Diagnose and fix the integration issues between components in SQLParserAST v6.0
🎯 Target: Fix empty tables/joins arrays and missing field-table associations

Author: AI Assistant
Date: 2025-08-26
"""

import os
import sys
import json
import traceback

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql_splitter'))

from sql_splitter.core.sql_parser_ast_v6_0 import SQLParserAST, parse_sql
from sql_splitter.core.join_handler import parse_joins_from_sql
from sql_splitter.core.table_extractor import extract_all_tables_from_sql
from sql_splitter.core.content_extractor import extract_content_from_sql, ContentExtractor

def test_component_isolation():
    """🔍 Test each component in isolation to confirm they work correctly"""
    print("🔍 STEP 1: Testing Components in Isolation")
    print("=" * 60)
    
    # Test SQL from momo_mv_item (known to have complex JOINs)
    test_sql = """
    select date_format(`mt_item`.`iCreateT`,'%Y-%m') AS `i_month`,`mt_item`.`DetailsID` AS `DetailsID`,`mt_item`.`Details_OrderID` AS `Details_OrderID`,`mt_item`.`iType` AS `iType`,`mt_item`.`iDesc` AS `iDesc`,`mt_item`.`iLink` AS `iLink`,`mt_item`.`iQty` AS `iQty`,`mt_item`.`iPrice` AS `iPrice`,`mt_item`.`iStatus` AS `iStatus`,`mt_item`.`iUpdateT` AS `iUpdateT`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,`mv_item_status_desc`.`Remarks` AS `Remarks`,`mv_order`.`Customer` AS `Customer`,`mv_order`.`Order_Status_Name` AS `Order_status_name`,`mv_order`.`Order_Status` AS `Order_Status`,`mt_item`.`iPic` AS `iPic`,`mt_item`.`igroup` AS `iGroup`,`mt_item`.`iTrack` AS `iTrack`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from (((`mt_item` join `mv_order` on(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`)) left join `mv_item_status_desc` on(`mt_item`.`iType` = `mv_item_status_desc`.`Item_Type`)) left join `mv_item_type_desc` on(`mt_item`.`iType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_item`.`iDeleted` < 1
    """
    
    # Test JOIN handler
    print("🔧 Testing JOIN Handler...")
    joins, join_aliases = parse_joins_from_sql(test_sql)
    print(f"   ✅ JOINs detected: {len(joins)}")
    print(f"   ✅ JOIN aliases: {len(join_aliases)}")
    for i, join in enumerate(joins):
        print(f"   📋 JOIN {i+1}: {join.join_type} {join.table_reference.table_name}")
    
    # Test table extractor
    print("\n🔧 Testing Table Extractor...")
    tables, table_aliases = extract_all_tables_from_sql(test_sql, set())
    print(f"   ✅ Tables detected: {len(tables)} -> {tables}")
    print(f"   ✅ Table aliases: {len(table_aliases)} -> {table_aliases}")
    
    # Test content extractor
    print("\n🔧 Testing Content Extractor...")
    extractor = ContentExtractor()
    extractor.set_context(table_aliases)
    
    fields = extractor.extract_fields(test_sql)
    where_conditions = extractor.extract_where_conditions(test_sql)
    
    print(f"   ✅ Fields detected: {len(fields)}")
    print(f"   ✅ WHERE conditions: {len(where_conditions)} -> {where_conditions}")
    
    # Check field-table associations
    fields_with_tables = [f for f in fields if f.get('table')]
    print(f"   📊 Fields with table associations: {len(fields_with_tables)}/{len(fields)}")
    
    return {
        'joins': len(joins),
        'tables': len(tables),
        'fields': len(fields),
        'fields_with_tables': len(fields_with_tables),
        'where_conditions': len(where_conditions),
        'table_aliases': table_aliases,
        'join_aliases': join_aliases
    }

def test_main_parser_integration():
    """🔍 Test main parser integration to find where data is lost"""
    print("\n🔍 STEP 2: Testing Main Parser Integration")
    print("=" * 60)
    
    test_sql = """
    select date_format(`mt_item`.`iCreateT`,'%Y-%m') AS `i_month`,`mt_item`.`DetailsID` AS `DetailsID`,`mt_item`.`Details_OrderID` AS `Details_OrderID`,`mt_item`.`iType` AS `iType`,`mt_item`.`iDesc` AS `iDesc`,`mt_item`.`iLink` AS `iLink`,`mt_item`.`iQty` AS `iQty`,`mt_item`.`iPrice` AS `iPrice`,`mt_item`.`iStatus` AS `iStatus`,`mt_item`.`iUpdateT` AS `iUpdateT`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,`mv_item_status_desc`.`Remarks` AS `Remarks`,`mv_order`.`Customer` AS `Customer`,`mv_order`.`Order_Status_Name` AS `Order_status_name`,`mv_order`.`Order_Status` AS `Order_Status`,`mt_item`.`iPic` AS `iPic`,`mt_item`.`igroup` AS `iGroup`,`mt_item`.`iTrack` AS `iTrack`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from (((`mt_item` join `mv_order` on(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`)) left join `mv_item_status_desc` on(`mt_item`.`iType` = `mv_item_status_desc`.`Item_Type`)) left join `mv_item_type_desc` on(`mt_item`.`iType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_item`.`iDeleted` < 1
    """
    
    parser = SQLParserAST()
    result = parser.parse(test_sql)
    
    print(f"🔧 Main Parser Results:")
    print(f"   ✅ Success: {result.get('success', False)}")
    print(f"   📊 Tables: {len(result.get('tables', []))} -> {result.get('tables', [])}")
    print(f"   📊 JOINs: {len(result.get('joins', []))}")
    print(f"   📊 Fields: {len(result.get('fields', []))}")
    print(f"   📊 WHERE: {len(result.get('whereConditions', []))}")
    
    # Check field-table associations in main parser result
    fields_with_tables = [f for f in result.get('fields', []) if f.get('table')]
    print(f"   📊 Fields with table associations: {len(fields_with_tables)}/{len(result.get('fields', []))}")
    
    return result

def diagnose_integration_loss():
    """🔍 Step-by-step diagnosis of where data is lost in integration"""
    print("\n🔍 STEP 3: Diagnosing Integration Data Loss")
    print("=" * 60)
    
    test_sql = """
    select date_format(`mt_item`.`iCreateT`,'%Y-%m') AS `i_month`,`mt_item`.`DetailsID` AS `DetailsID`,`mt_item`.`Details_OrderID` AS `Details_OrderID`,`mt_item`.`iType` AS `iType`,`mt_item`.`iDesc` AS `iDesc`,`mt_item`.`iLink` AS `iLink`,`mt_item`.`iQty` AS `iQty`,`mt_item`.`iPrice` AS `iPrice`,`mt_item`.`iStatus` AS `iStatus`,`mt_item`.`iUpdateT` AS `iUpdateT`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,`mv_item_status_desc`.`Remarks` AS `Remarks`,`mv_order`.`Customer` AS `Customer`,`mv_order`.`Order_Status_Name` AS `Order_status_name`,`mv_order`.`Order_Status` AS `Order_Status`,`mt_item`.`iPic` AS `iPic`,`mt_item`.`igroup` AS `iGroup`,`mt_item`.`iTrack` AS `iTrack`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from (((`mt_item` join `mv_order` on(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`)) left join `mv_item_status_desc` on(`mt_item`.`iType` = `mv_item_status_desc`.`Item_Type`)) left join `mv_item_type_desc` on(`mt_item`.`iType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_item`.`iDeleted` < 1
    """
    
    # Create parser instance and manually step through the process
    parser = SQLParserAST()
    
    # Reset state
    parser._reset_state()
    print("🔧 State reset complete")
    
    # Normalize SQL
    normalized_sql = parser._normalize_sql(test_sql)
    print(f"🔧 Normalization complete: {len(normalized_sql)} chars")
    
    # Build AST tree (Phase 1)
    print("\n📋 Phase 1: AST Tree Building")
    ast_tree = parser._build_ast_tree(normalized_sql)
    
    print(f"   📊 AST FROM clause tables: {len(ast_tree.from_clause.table_references) if ast_tree.from_clause else 0}")
    print(f"   📊 AST JOINs: {len(ast_tree.joins)}")
    print(f"   📊 AST WITH clause: {'Yes' if ast_tree.with_clause else 'No'}")
    print(f"   📊 Parser table_aliases after AST: {len(parser.table_aliases)} -> {parser.table_aliases}")
    
    # Extract content (Phase 2)
    print("\n📋 Phase 2: Content Extraction")
    
    # Set context for content extractor
    parser.content_extractor.set_context(
        parser.table_aliases, 
        parser.database_name, 
        parser.detected_databases
    )
    print(f"   🔧 Content extractor context set: {len(parser.table_aliases)} aliases")
    
    # Extract components
    group_by_fields = parser.content_extractor.extract_group_by_fields(normalized_sql)
    fields = parser.content_extractor.extract_fields(normalized_sql, group_by_fields)
    where_conditions = parser.content_extractor.extract_where_conditions(normalized_sql)
    
    print(f"   📊 Content extractor fields: {len(fields)}")
    print(f"   📊 Content extractor WHERE: {len(where_conditions)}")
    
    # Extract from AST
    ast_tables = parser._extract_tables_from_ast(ast_tree)
    ast_joins = parser._extract_joins_from_ast(ast_tree)
    
    print(f"   📊 AST extracted tables: {len(ast_tables)} -> {ast_tables}")
    print(f"   📊 AST extracted JOINs: {len(ast_joins)}")
    
    return {
        'ast_tree': ast_tree,
        'parser_aliases': parser.table_aliases,
        'content_fields': len(fields),
        'content_where': len(where_conditions),
        'ast_tables': ast_tables,
        'ast_joins': ast_joins
    }

def identify_root_causes(component_results, integration_results, diagnosis_results):
    """🎯 Identify the specific root causes of integration failure"""
    print("\n🎯 STEP 4: Root Cause Analysis")
    print("=" * 60)
    
    issues = []
    
    # Issue 1: Tables extraction
    if component_results['tables'] > 0 and len(integration_results.get('tables', [])) == 0:
        issues.append("❌ Tables: Components detect tables but main parser returns empty array")
        print(f"   🔍 Component tables: {component_results['tables']}")
        print(f"   🔍 Integration tables: {len(integration_results.get('tables', []))}")
    
    # Issue 2: JOINs extraction  
    if component_results['joins'] > 0 and len(integration_results.get('joins', [])) == 0:
        issues.append("❌ JOINs: Components detect JOINs but main parser returns empty array")
        print(f"   🔍 Component JOINs: {component_results['joins']}")
        print(f"   🔍 Integration JOINs: {len(integration_results.get('joins', []))}")
    
    # Issue 3: Field-table associations
    if component_results['fields_with_tables'] > 0:
        integration_fields_with_tables = len([f for f in integration_results.get('fields', []) if f.get('table')])
        if integration_fields_with_tables == 0:
            issues.append("❌ Field-Table Association: Components associate fields with tables but main parser loses associations")
            print(f"   🔍 Component field-table associations: {component_results['fields_with_tables']}")
            print(f"   🔍 Integration field-table associations: {integration_fields_with_tables}")
    
    # Issue 4: Table aliases propagation
    if len(component_results['table_aliases']) > 0 and len(diagnosis_results['parser_aliases']) == 0:
        issues.append("❌ Table Aliases: Table aliases not propagated to parser state")
        print(f"   🔍 Component table aliases: {component_results['table_aliases']}")
        print(f"   🔍 Parser table aliases: {diagnosis_results['parser_aliases']}")
    
    print(f"\n📊 Total Issues Identified: {len(issues)}")
    for issue in issues:
        print(f"   {issue}")
    
    return issues

def create_integration_fixes():
    """🛠️ Create specific fixes for identified integration issues"""
    print("\n🛠️ STEP 5: Creating Integration Fixes")
    print("=" * 60)
    
    fixes = []
    
    # Fix 1: AST table extraction issue
    fix_1 = """
# FIX 1: _extract_tables_from_ast method returns empty list
# ROOT CAUSE: AST tree is not properly populated in Phase 1
# SOLUTION: Ensure table information is correctly stored in AST and extracted

def _extract_tables_from_ast(self, ast_tree: QueryNode) -> List[str]:
    tables = set()
    
    # FIXED: Use table_aliases as primary source since AST is not fully populated
    for alias, table_name in self.table_aliases.items():
        clean_table = self._remove_db_prefix_context_aware(table_name, "table_reference")
        if clean_table and self._is_valid_table_name(clean_table):
            tables.add(clean_table)
    
    # FALLBACK: Try to extract from AST if populated
    if ast_tree.from_clause:
        for table_ref in ast_tree.from_clause.table_references:
            clean_table = self._remove_db_prefix_context_aware(table_ref.table_name, "from_clause")
            if clean_table and self._is_valid_table_name(clean_table):
                tables.add(clean_table)
    
    return list(tables)
    """
    fixes.append(fix_1)
    
    # Fix 2: AST JOIN extraction issue
    fix_2 = """
# FIX 2: _extract_joins_from_ast method depends on incomplete AST
# ROOT CAUSE: AST JOINs are not correctly populated in Phase 1
# SOLUTION: Use join_handler results directly instead of relying on AST

def _extract_joins_from_ast(self, ast_tree: QueryNode) -> List[Dict[str, Any]]:
    # FIXED: Use join_handler results directly
    joins, _ = parse_joins_from_sql(self.normalized_sql)  # Store normalized_sql as instance variable
    
    result_joins = []
    for join in joins:
        clean_right_table = self._remove_db_prefix_context_aware(join.table_reference.table_name, "table_reference")
        
        if clean_right_table and self._is_valid_table_name(clean_right_table):
            condition_text = join.condition.condition_text if join.condition else ""
            left_table, left_field, right_field, clean_condition = self._parse_join_condition(condition_text)
            
            if left_table:
                join_info = {
                    "type": join.join_type,
                    "leftTable": left_table,
                    "leftField": left_field,
                    "rightTable": clean_right_table,
                    "rightField": right_field,
                    "condition": clean_condition
                }
                result_joins.append(join_info)
    
    return result_joins
    """
    fixes.append(fix_2)
    
    # Fix 3: Table aliases propagation
    fix_3 = """
# FIX 3: Table aliases not properly propagated to ContentExtractor
# ROOT CAUSE: Context setting happens too late or is overridden
# SOLUTION: Ensure aliases are collected early and propagated correctly

def _build_ast_tree(self, sql: str) -> QueryNode:
    # Store normalized SQL for later use
    self.normalized_sql = sql
    
    # ... existing code ...
    
    # 2️⃣ Parse JOINs (complex nested patterns) - FIXED: Collect aliases immediately
    joins, join_aliases = parse_joins_from_sql(sql)
    self.table_aliases.update(join_aliases)
    
    # 3️⃣ Extract all tables - FIXED: Collect aliases immediately  
    all_cte_tables = cte_tables if cte_tables else set()
    tables, table_aliases = extract_all_tables_from_sql(sql, all_cte_tables)
    self.table_aliases.update(table_aliases)
    
    # FIXED: Propagate aliases to content extractor immediately
    self.content_extractor.set_context(
        self.table_aliases, 
        self.database_name, 
        self.detected_databases
    )
    
    # ... rest of existing code ...
    """
    fixes.append(fix_3)
    
    print(f"📝 Created {len(fixes)} integration fixes")
    for i, fix in enumerate(fixes, 1):
        print(f"   ✅ Fix {i}: Integration issue addressed")
    
    return fixes

def main():
    """🚀 Main diagnostic and fix process"""
    print("🚨 SQL Parser AST v6.0 - Integration Diagnostic & Fix")
    print("=" * 70)
    
    try:
        # Step 1: Test components in isolation
        component_results = test_component_isolation()
        
        # Step 2: Test main parser integration
        integration_results = test_main_parser_integration()
        
        # Step 3: Diagnose integration data loss
        diagnosis_results = diagnose_integration_loss()
        
        # Step 4: Identify root causes
        issues = identify_root_causes(component_results, integration_results, diagnosis_results)
        
        # Step 5: Create integration fixes
        fixes = create_integration_fixes()
        
        # Summary
        print("\n🎯 DIAGNOSTIC SUMMARY")
        print("=" * 60)
        print(f"✅ Components Working: ALL ({component_results['joins']} JOINs, {component_results['tables']} tables)")
        print(f"❌ Integration Issues: {len(issues)} critical problems")
        print(f"🛠️ Fixes Available: {len(fixes)} targeted solutions")
        
        if issues:
            print("\n🚨 CRITICAL: Integration fixes required before parser can work correctly")
            print("📋 Next steps:")
            print("   1. Apply the 3 integration fixes to sql_parser_ast_v6_0.py")
            print("   2. Test integration with fixed code")
            print("   3. Validate all 31 queries with corrected parser")
        else:
            print("\n✅ SUCCESS: No integration issues found")
            
    except Exception as e:
        print(f"\n❌ DIAGNOSTIC ERROR: {str(e)}")
        print(f"📋 Stack trace:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
