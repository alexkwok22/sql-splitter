#!/usr/bin/env python3
"""
SQL Splitter - Basic Usage Examples

Demonstrates core functionality of the SQL Splitter parser
with real-world SQL queries and visualization-ready outputs.
"""

import sys
import os
import json

# Add the sql_splitter package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sql_splitter import SQLParserAST, parse_sql


def example_1_simple_query():
    """Example 1: Simple SELECT with JOIN"""
    print("🎯 Example 1: Simple SELECT with JOIN")
    print("=" * 50)
    
    sql = """
    SELECT users.name, users.email, orders.total
    FROM users 
    JOIN orders ON users.id = orders.user_id
    WHERE users.status = 'active'
    """
    
    result = parse_sql(sql)
    print(f"✅ Success: {result['success']}")
    print(f"📊 Tables: {result['tables']}")
    print(f"🔗 JOINs: {len(result['joins'])}")
    print(f"📝 Fields: {len(result['fields'])}")
    print()


def example_2_aggregation_query():
    """Example 2: Aggregation with GROUP BY"""
    print("🎯 Example 2: Aggregation with GROUP BY")
    print("=" * 50)
    
    sql = """
    SELECT 
        users.department,
        COUNT(*) as employee_count,
        AVG(users.salary) as avg_salary,
        SUM(orders.amount) as total_revenue
    FROM users 
    LEFT JOIN orders ON users.id = orders.user_id
    WHERE users.active = 1
    GROUP BY users.department
    """
    
    result = parse_sql(sql)
    
    print(f"✅ Success: {result['success']}")
    print(f"📊 Aggregation Fields:")
    for field in result['fields']:
        if field['fieldType'] == 'aggregation':
            print(f"   - {field['field']} (scope: {field.get('aggregationScope', 'N/A')})")
    print()


def example_3_complex_joins():
    """Example 3: Complex nested JOINs"""
    print("🎯 Example 3: Complex nested JOINs")
    print("=" * 50)
    
    sql = """
    SELECT 
        u.name,
        o.order_date,
        p.product_name,
        od.quantity
    FROM users u
    JOIN orders o ON u.id = o.user_id
    JOIN order_details od ON o.id = od.order_id
    JOIN products p ON od.product_id = p.id
    WHERE o.status = 'completed'
    """
    
    result = parse_sql(sql)
    
    print(f"✅ Success: {result['success']}")
    print(f"🔗 JOINs detected: {len(result['joins'])}")
    for i, join in enumerate(result['joins'], 1):
        print(f"   JOIN {i}: {join['leftTable']}.{join['leftField']} = {join['rightTable']}.{join['rightField']}")
    print()


def example_4_mysql_specific():
    """Example 4: MySQL-specific syntax"""
    print("🎯 Example 4: MySQL-specific syntax")
    print("=" * 50)
    
    sql = """
    SELECT 
        `users`.`name`,
        DATE_FORMAT(`orders`.`created_at`, '%Y-%m') as order_month,
        COUNT(*) as monthly_orders
    FROM `users` 
    JOIN `orders` ON `users`.`id` = `orders`.`user_id`
    WHERE `users`.`status` = 'active'
    GROUP BY `users`.`name`, DATE_FORMAT(`orders`.`created_at`, '%Y-%m')
    """
    
    result = parse_sql(sql)
    
    print(f"✅ Success: {result['success']}")
    print(f"📝 Field Types:")
    for field in result['fields']:
        print(f"   - {field['field']}: {field['fieldType']}")
    print()


def example_5_visualization_metadata():
    """Example 5: Visualization metadata extraction"""
    print("🎯 Example 5: Visualization metadata extraction")
    print("=" * 50)
    
    sql = """
    SELECT 
        users.department,
        COUNT(*) as total_employees,
        CASE 
            WHEN AVG(salary) > 50000 THEN 'High'
            WHEN AVG(salary) > 30000 THEN 'Medium' 
            ELSE 'Low' 
        END as salary_category
    FROM users
    GROUP BY users.department
    """
    
    parser = SQLParserAST()
    result = parser.parse(sql)
    
    print(f"✅ Success: {result['success']}")
    print("🎨 Metadata for visualization:")
    metadata = result.get('metadata', {})
    
    print(f"   - Aggregation fields: {metadata.get('aggregationFields', [])}")
    print(f"   - Computed fields: {metadata.get('computedFields', [])}")
    print(f"   - Alias mapping: {metadata.get('aliasMapping', {})}")
    
    print("\n📊 Full JSON output:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    print("🚀 SQL Splitter - Basic Usage Examples")
    print("=" * 70)
    print()
    
    # Run all examples
    example_1_simple_query()
    example_2_aggregation_query() 
    example_3_complex_joins()
    example_4_mysql_specific()
    example_5_visualization_metadata()
    
    print("🎉 All examples completed successfully!")
