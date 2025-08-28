#!/usr/bin/env python3
"""
SQL Splitter v6.1.0 - Console Output Test

🔍 Print JSON outputs to console for manual inspection
📊 Test various SQL queries and display parsed results

Author: AI Assistant
Date: 2025-08-28
"""

import json

def console_test_v6_1_0():
    """🔍 Console output test for manual inspection"""
    print("🔍 SQL Splitter v6.1.0 - Console Output Test")
    print("=" * 60)
    
    # Import the released package
    try:
        from sql_splitter import SQLParserAST
        from sql_splitter import __version__
        print(f"✅ Package imported successfully - Version: {__version__}")
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        return
    
    # Test SQL queries
    test_queries = [
        {
            "name": "Simple SELECT",
            "sql": "SELECT customer_id, first_name, last_name FROM customers WHERE status = 'active'"
        },
        {
            "name": "JOIN Query", 
            "sql": "SELECT o.order_id, o.total_amount, c.customer_name FROM orders o JOIN customers c ON o.customer_id = c.customer_id"
        },
        {
            "name": "Complex Momo Query",
            "sql": """select date_format(`mt_item`.`iCreateT`,'%Y-%m') AS `i_month`,`mt_item`.`DetailsID` AS `DetailsID`,`mt_item`.`Details_OrderID` AS `Details_OrderID`,`mt_item`.`iType` AS `iType`,`mt_item`.`iDesc` AS `iDesc`,`mt_item`.`iLink` AS `iLink`,`mt_item`.`iQty` AS `iQty`,`mt_item`.`iPrice` AS `iPrice`,`mt_item`.`iStatus` AS `iStatus`,`mt_item`.`iUpdateT` AS `iUpdateT`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,`mv_item_status_desc`.`Remarks` AS `Remarks`,`mv_order`.`Customer` AS `Customer`,`mv_order`.`Order_Status_Name` AS `Order_status_name`,`mv_order`.`Order_Status` AS `Order_Status`,`mt_item`.`iPic` AS `iPic`,`mt_item`.`igroup` AS `iGroup`,`mt_item`.`iTrack` AS `iTrack`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from (((`mt_item` join `mv_order` on(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`)) left join `mv_item_status_desc` on(`mt_item`.`iType` = `mv_item_status_desc`.`Item_Type`)) left join `mv_item_type_desc` on(`mt_item`.`iType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_item`.`iDeleted` < 1"""
        }
    ]
    
    parser = SQLParserAST()
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"📋 Test {i}: {test['name']}")
        print(f"{'=' * 60}")
        print(f"📝 SQL Query:")
        print(test['sql'])
        print(f"\n🔍 Parser Output:")
        
        try:
            # Parse the query
            result = parser.parse(test['sql'])
            
            # Pretty print the JSON result
            json_output = json.dumps(result, indent=2, ensure_ascii=False)
            print(json_output)
            
        except Exception as e:
            print(f"❌ Error parsing query: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'=' * 60}")
    print("🔍 Console output test completed")
    print("👀 Please review the JSON outputs above for correctness")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    console_test_v6_1_0()
