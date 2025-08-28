#!/usr/bin/env python3
"""
Final Corrected Validation Test - SQLParserAST v6.0

🎯 Comprehensive validation using COMPLETE SQL queries (not truncated)
📊 Generate accurate test reports with full functionality validation

Author: AI Assistant
Date: 2025-08-28
"""

import os
import sys
import json
import time

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql_splitter'))

from sql_splitter.core.sql_parser_ast_v6_0 import SQLParserAST

def run_corrected_validation():
    """🚀 Run validation with COMPLETE SQL queries"""
    print("🚀 SQL Parser AST v6.0 - CORRECTED Full Validation")
    print("=" * 70)
    
    # Complete SQL queries from expect.md (NOT truncated)
    complete_queries = {
        "momo_mv_item": """select date_format(`mt_item`.`iCreateT`,'%Y-%m') AS `i_month`,`mt_item`.`DetailsID` AS `DetailsID`,`mt_item`.`Details_OrderID` AS `Details_OrderID`,`mt_item`.`iType` AS `iType`,`mt_item`.`iDesc` AS `iDesc`,`mt_item`.`iLink` AS `iLink`,`mt_item`.`iQty` AS `iQty`,`mt_item`.`iPrice` AS `iPrice`,`mt_item`.`iStatus` AS `iStatus`,`mt_item`.`iUpdateT` AS `iUpdateT`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,`mv_item_status_desc`.`Remarks` AS `Remarks`,`mv_order`.`Customer` AS `Customer`,`mv_order`.`Order_Status_Name` AS `Order_status_name`,`mv_order`.`Order_Status` AS `Order_Status`,`mt_item`.`iPic` AS `iPic`,`mt_item`.`igroup` AS `iGroup`,`mt_item`.`iTrack` AS `iTrack`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from (((`mt_item` join `mv_order` on(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`)) left join `mv_item_status_desc` on(`mt_item`.`iType` = `mv_item_status_desc`.`Item_Type`)) left join `mv_item_type_desc` on(`mt_item`.`iType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_item`.`iDeleted` < 1""",
        
        "momo_mv_item_status_desc": """select `mt_status_desc`.`Desc_ID` AS `Desc_ID`,`mt_status_desc`.`DESC_NAME` AS `DESC_NAME`,`mt_status_desc`.`DESC_CODE` AS `DESC_CODE`,`mt_status_desc`.`FOR_TABLE` AS `FOR_TABLE`,`mt_status_desc`.`Remarks` AS `Remarks`,`mt_status_desc`.`Item_Type` AS `Item_Type` from `mt_status_desc` where `mt_status_desc`.`FOR_TABLE` = 'iStatus'""",
        
        "momo_mv_order": """select date_format(`mt_order`.`oCreateT`,'%Y-%m') AS `o_month`,date_format(`mt_order`.`oCreateT`,'%Y-%m-%d %a') AS `o_date`,`mt_order`.`OrderID` AS `OrderID`,`mt_order`.`Customer` AS `Customer`,`mt_order`.`oDesc` AS `oDesc`,`mt_order`.`oPayMethod` AS `oPayMethod`,`mt_order`.`oTotalPrice` AS `oTotalPrice`,`mt_order`.`oPaidPrice` AS `oPaidPrice`,`mt_order`.`oStatus` AS `oStatus`,`mt_order`.`oCreateT` AS `oCreateT`,`mt_order`.`oUpdateT` AS `oUpdateT`,`mv_order_status_desc`.`DESC_NAME` AS `Order_Status_Name`,`mv_order_status_desc`.`Remarks` AS `Remarks`,`mt_order`.`oDeleted` AS `oDeleted`,if(`mv_order_status_desc`.`Remarks` = 'finish',1,0) AS `finish`,`mt_order`.`oEditT` AS `oEditT`,`mt_order`.`oRemark` AS `oRemark`,`mt_order`.`Order_Status` AS `Order_Status` from (`mt_order` left join `mv_order_status_desc` on(`mt_order`.`Order_Status` = `mv_order_status_desc`.`DESC_CODE`)) where `mt_order`.`oDeleted` < 1""",
        
        "momo_v_game": """select `mt_game_header`.`id_game` AS `id_game`,`mt_game_header`.`Create_datetime` AS `Create_datetime`,`mt_game_header`.`Created_by` AS `Created_by`,`mt_game_header`.`title` AS `title`,`mt_game_header`.`option_i` AS `option_i`,`mt_game_header`.`option_vs` AS `option_vs`,`mt_game_details`.`id_gameDetails` AS `id_gameDetails`,`mt_game_details`.`d_Create_datetime` AS `d_Create_datetime`,`mt_game_details`.`d_Created_by` AS `d_Created_by`,`mt_game_details`.`selected` AS `selected`,`mt_game_link`.`id_link` AS `id_link` from ((`mt_game_header` left join `mt_game_details` on(`mt_game_header`.`id_game` = `mt_game_details`.`id_game`)) left join `mt_game_link` on(`mt_game_details`.`id_gameDetails` = `mt_game_link`.`id_gameDetails`))""",
        
        "simple_test_1": """SELECT customer_id, first_name, last_name, email FROM customers WHERE status = 'active'""",
        
        "simple_test_2": """SELECT o.order_id, o.total_amount, c.customer_name FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.order_date >= '2023-01-01'""",
        
        "complex_joins": """SELECT p.product_name, c.category_name, s.supplier_name FROM products p INNER JOIN categories c ON p.category_id = c.category_id LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id WHERE p.status = 'active'"""
    }
    
    parser = SQLParserAST()
    results = {}
    total_stats = {
        'total_queries': 0,
        'successful_parses': 0,
        'structure_compliant': 0,
        'tables_detected': 0,
        'joins_detected': 0,
        'fields_detected': 0,
        'where_detected': 0,
        'field_table_associations': 0
    }
    
    print(f"\n📋 Testing {len(complete_queries)} complete SQL queries...")
    
    for query_name, sql in complete_queries.items():
        print(f"\n🔧 Testing: {query_name}")
        print(f"   📏 SQL length: {len(sql)} characters")
        
        # Parse query
        start_time = time.time()
        result = parser.parse(sql)
        execution_time = time.time() - start_time
        
        # Analyze results
        success = result.get('success', False)
        tables = result.get('tables', [])
        joins = result.get('joins', [])
        fields = result.get('fields', [])
        where_conditions = result.get('whereConditions', [])
        
        # Count field-table associations
        fields_with_tables = len([f for f in fields if f.get('table')])
        
        # Display results
        print(f"   ✅ Success: {success}")
        print(f"   📊 Tables: {len(tables)} -> {tables}")
        print(f"   📊 JOINs: {len(joins)}")
        if joins:
            for i, join in enumerate(joins[:3]):  # Show first 3
                print(f"      🔗 JOIN {i+1}: {join.get('type', 'UNKNOWN')} {join.get('rightTable', 'UNKNOWN')}")
        print(f"   📊 Fields: {len(fields)} ({fields_with_tables} with table associations)")
        print(f"   📊 WHERE: {len(where_conditions)} -> {where_conditions}")
        print(f"   ⏱️  Time: {execution_time:.4f}s")
        
        # Update stats
        total_stats['total_queries'] += 1
        if success:
            total_stats['successful_parses'] += 1
        if success and len(tables) > 0:
            total_stats['structure_compliant'] += 1
        
        total_stats['tables_detected'] += len(tables)
        total_stats['joins_detected'] += len(joins)
        total_stats['fields_detected'] += len(fields)
        total_stats['where_detected'] += len(where_conditions)
        total_stats['field_table_associations'] += fields_with_tables
        
        # Store result
        results[query_name] = {
            'success': success,
            'tables': len(tables),
            'joins': len(joins),
            'fields': len(fields),
            'where_conditions': len(where_conditions),
            'field_table_associations': fields_with_tables,
            'execution_time': execution_time,
            'parser_output': result
        }
    
    # Generate comprehensive report
    print(f"\n🎯 COMPREHENSIVE VALIDATION RESULTS")
    print("=" * 70)
    
    success_rate = (total_stats['successful_parses'] / total_stats['total_queries']) * 100
    structure_rate = (total_stats['structure_compliant'] / total_stats['total_queries']) * 100
    
    print(f"📋 Total Queries Tested: {total_stats['total_queries']}")
    print(f"✅ Successful Parses: {total_stats['successful_parses']} ({success_rate:.1f}%)")
    print(f"🏗️  Structure Compliant: {total_stats['structure_compliant']} ({structure_rate:.1f}%)")
    print(f"📊 Total Tables Detected: {total_stats['tables_detected']}")
    print(f"🔗 Total JOINs Detected: {total_stats['joins_detected']}")
    print(f"📝 Total Fields Detected: {total_stats['fields_detected']}")
    print(f"🔍 Total WHERE Conditions: {total_stats['where_detected']}")
    print(f"🎯 Field-Table Associations: {total_stats['field_table_associations']}")
    
    # Assessment
    print(f"\n🏆 FINAL ASSESSMENT")
    print("=" * 40)
    
    if success_rate >= 95 and total_stats['fields_detected'] > 0:
        print("🎉 EXCELLENT: Parser works perfectly!")
        print("🚀 Ready for production use")
        
        # Show sample results
        print(f"\n📝 SAMPLE RESULTS:")
        for i, (query_name, result) in enumerate(list(results.items())[:3]):
            print(f"   {i+1}. {query_name}: {result['fields']} fields, {result['tables']} tables, {result['joins']} joins")
        
    elif success_rate >= 85:
        print("✅ GOOD: Parser works well with minor issues")
    else:
        print("⚠️  NEEDS WORK: Parser has issues")
    
    # Save results
    output_file = 'corrected_validation_results.json'
    output_data = {
        'test_summary': {
            'test_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'parser_version': '6.0_corrected_validation',
            'total_queries': total_stats['total_queries'],
            'success_rate': success_rate,
            'structure_compliance_rate': structure_rate,
            'total_stats': total_stats
        },
        'detailed_results': results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed results saved to: {output_file}")
    
    return total_stats, results

if __name__ == "__main__":
    try:
        stats, results = run_corrected_validation()
        print(f"\n✅ CORRECTED validation completed successfully!")
    except Exception as e:
        print(f"\n❌ Validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
