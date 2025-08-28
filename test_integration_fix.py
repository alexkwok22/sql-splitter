#!/usr/bin/env python3
"""
Integration Fix Test Script

🎯 Test the integration fixes for SQLParserAST v6.0
🚀 Verify that tables, joins, and field-table associations are now correctly populated

Author: AI Assistant
Date: 2025-08-26
"""

import os
import sys
import json

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql_splitter'))

from sql_splitter.core.sql_parser_ast_v6_0 import SQLParserAST

def test_integration_fix():
    """🎯 Test integration fix with known problematic query"""
    print("🚀 Testing Integration Fix - SQLParserAST v6.0")
    print("=" * 60)
    
    # Test SQL from momo_mv_item (previously had empty tables/joins)
    test_sql = """
    select date_format(`mt_item`.`iCreateT`,'%Y-%m') AS `i_month`,`mt_item`.`DetailsID` AS `DetailsID`,`mt_item`.`Details_OrderID` AS `Details_OrderID`,`mt_item`.`iType` AS `iType`,`mt_item`.`iDesc` AS `iDesc`,`mt_item`.`iLink` AS `iLink`,`mt_item`.`iQty` AS `iQty`,`mt_item`.`iPrice` AS `iPrice`,`mt_item`.`iStatus` AS `iStatus`,`mt_item`.`iUpdateT` AS `iUpdateT`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,`mv_item_status_desc`.`Remarks` AS `Remarks`,`mv_order`.`Customer` AS `Customer`,`mv_order`.`Order_Status_Name` AS `Order_status_name`,`mv_order`.`Order_Status` AS `Order_Status`,`mt_item`.`iPic` AS `iPic`,`mt_item`.`igroup` AS `iGroup`,`mt_item`.`iTrack` AS `iTrack`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from (((`mt_item` join `mv_order` on(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`)) left join `mv_item_status_desc` on(`mt_item`.`iType` = `mv_item_status_desc`.`Item_Type`)) left join `mv_item_type_desc` on(`mt_item`.`iType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_item`.`iDeleted` < 1
    """
    
    print("🔧 Testing with complex triple-nested JOIN query...")
    
    # Parse with fixed parser
    parser = SQLParserAST()
    result = parser.parse(test_sql)
    
    # Display results
    print(f"\n📊 RESULTS:")
    print(f"   ✅ Success: {result.get('success', False)}")
    print(f"   📋 Tables: {len(result.get('tables', []))} detected")
    print(f"       → {result.get('tables', [])}")
    print(f"   📋 JOINs: {len(result.get('joins', []))} detected")
    
    # Display JOIN details
    joins = result.get('joins', [])
    for i, join in enumerate(joins):
        print(f"       → JOIN {i+1}: {join.get('type', 'UNKNOWN')} {join.get('rightTable', 'UNKNOWN')}")
    
    print(f"   📋 Fields: {len(result.get('fields', []))} detected")
    print(f"   📋 WHERE: {len(result.get('whereConditions', []))} detected")
    print(f"       → {result.get('whereConditions', [])}")
    
    # Check field-table associations
    fields = result.get('fields', [])
    fields_with_tables = [f for f in fields if f.get('table')]
    print(f"   📋 Field-table associations: {len(fields_with_tables)}/{len(fields)}")
    
    # Show first few field associations
    print(f"\n🔍 SAMPLE FIELD-TABLE ASSOCIATIONS:")
    for i, field in enumerate(fields[:5]):
        table = field.get('table', 'NO_TABLE')
        field_name = field.get('field', 'NO_FIELD')[:50] + ('...' if len(field.get('field', '')) > 50 else '')
        print(f"   📝 Field {i+1}: {table} → {field_name}")
    
    # Validation check
    print(f"\n🎯 VALIDATION:")
    
    # Check for previous issues
    issues = []
    if len(result.get('tables', [])) == 0:
        issues.append("❌ Tables array still empty")
    else:
        issues.append("✅ Tables array populated")
    
    if len(result.get('joins', [])) == 0:
        issues.append("❌ JOINs array still empty")
    else:
        issues.append("✅ JOINs array populated")
    
    if len(fields_with_tables) == 0:
        issues.append("❌ Field-table associations still missing")
    else:
        issues.append("✅ Field-table associations present")
    
    for issue in issues:
        print(f"   {issue}")
    
    # Overall assessment
    success_count = len([i for i in issues if i.startswith('✅')])
    total_count = len(issues)
    
    print(f"\n🏆 INTEGRATION FIX ASSESSMENT:")
    print(f"   📊 Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("   🎉 SUCCESS: All integration issues resolved!")
        print("   🚀 Ready for full validation on all 31 queries")
    elif success_count > 0:
        print("   ⚠️  PARTIAL: Some integration issues resolved, others remain")
        print("   🔧 Additional fixes may be needed")
    else:
        print("   ❌ FAILURE: Integration issues persist")
        print("   🚨 Further debugging required")
    
    return result, success_count, total_count

def main():
    """🚀 Main test execution"""
    try:
        result, success_count, total_count = test_integration_fix()
        
        print(f"\n📝 SUMMARY:")
        print(f"✅ Integration fix test completed")
        print(f"📊 Success rate: {success_count}/{total_count} components fixed")
        
        if success_count == total_count:
            print("🎯 READY: Parser is ready for full validation testing")
        else:
            print("🔧 NEEDS WORK: Additional fixes required")
            
    except Exception as e:
        print(f"\n❌ TEST ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
