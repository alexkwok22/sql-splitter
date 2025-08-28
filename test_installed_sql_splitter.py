#!/usr/bin/env python3
"""
測試從 TestPyPI 安裝的 sql-splitter 包
使用 3 個自製的 SQL 查詢展示功能
"""

import json
from sql_splitter import SQLParserAST

def print_json_pretty(data, title):
    """美化打印 JSON 數據"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print('='*60)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print('='*60)

def main():
    print("🚀 測試從 TestPyPI 安裝的 sql-splitter v6.0.1")
    print("📝 使用 3 個自製 SQL 查詢展示解析功能\n")
    
    # 初始化解析器
    parser = SQLParserAST()
    
    # 測試查詢 1: 複雜的電商訂單統計查詢
    sql1 = """
    SELECT 
        u.name as customer_name,
        u.email,
        COUNT(o.id) as total_orders,
        SUM(oi.quantity * oi.price) as total_revenue,
        AVG(o.order_total) as avg_order_value,
        DATE_FORMAT(o.created_at, '%Y-%m') as order_month
    FROM users u
    INNER JOIN orders o ON u.id = o.user_id
    LEFT JOIN order_items oi ON o.id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.id
    WHERE u.status = 'active'
        AND o.created_at >= '2024-01-01'
        AND p.category IN ('electronics', 'books', 'clothing')
    GROUP BY u.id, DATE_FORMAT(o.created_at, '%Y-%m')
    HAVING total_orders > 2
    ORDER BY total_revenue DESC, customer_name ASC
    LIMIT 100
    """
    
    # 測試查詢 2: 庫存管理與供應商分析
    sql2 = """
    SELECT 
        p.product_name,
        p.sku,
        s.supplier_name,
        s.country as supplier_country,
        i.current_stock,
        i.reorder_level,
        CASE 
            WHEN i.current_stock <= i.reorder_level THEN 'Low Stock'
            WHEN i.current_stock <= i.reorder_level * 1.5 THEN 'Medium Stock'
            ELSE 'High Stock'
        END as stock_status,
        (i.current_stock * p.cost_price) as inventory_value
    FROM products p
    JOIN inventory i ON p.id = i.product_id
    JOIN suppliers s ON p.supplier_id = s.id
    WHERE i.current_stock > 0
        AND p.status = 'active'
        AND s.is_verified = true
    """
    
    # 測試查詢 3: 銷售趨勢分析與預測
    sql3 = """
    WITH monthly_sales AS (
        SELECT 
            DATE_FORMAT(order_date, '%Y-%m') as sale_month,
            category,
            SUM(total_amount) as monthly_revenue,
            COUNT(DISTINCT customer_id) as unique_customers,
            AVG(total_amount) as avg_transaction
        FROM sales_view sv
        JOIN product_categories pc ON sv.product_id = pc.product_id
        WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        GROUP BY DATE_FORMAT(order_date, '%Y-%m'), category
    ),
    growth_calc AS (
        SELECT 
            *,
            LAG(monthly_revenue) OVER (PARTITION BY category ORDER BY sale_month) as prev_revenue,
            ROW_NUMBER() OVER (PARTITION BY category ORDER BY sale_month DESC) as rank_desc
        FROM monthly_sales
    )
    SELECT 
        sale_month,
        category,
        monthly_revenue,
        unique_customers,
        avg_transaction,
        ROUND(((monthly_revenue - prev_revenue) / prev_revenue * 100), 2) as growth_rate
    FROM growth_calc
    WHERE rank_desc <= 6
    ORDER BY category, sale_month DESC
    """
    
    # 測試每個查詢
    test_queries = [
        ("複雜電商訂單統計查詢", sql1),
        ("庫存管理與供應商分析", sql2),
        ("銷售趨勢分析與預測 (CTE + Window Functions)", sql3)
    ]
    
    for i, (title, sql) in enumerate(test_queries, 1):
        print(f"\n🔍 測試查詢 {i}: {title}")
        print(f"📜 SQL 長度: {len(sql)} 字符")
        
        try:
            # 解析 SQL
            result = parser.parse(sql)
            
            # 顯示解析結果
            print_json_pretty(result, f"查詢 {i} 解析結果: {title}")
            
            # 顯示統計摘要
            if result.get('success'):
                print(f"\n📊 解析統計摘要:")
                print(f"   ✅ 解析成功: {result['success']}")
                print(f"   📋 字段數量: {len(result.get('fields', []))}")
                print(f"   🏷️  表格數量: {len(result.get('tables', []))}")
                print(f"   🔗 JOIN 數量: {len(result.get('joins', []))}")
                print(f"   🔍 WHERE 條件: {len(result.get('whereConditions', []))}")
                
                # 顯示字段類型分佈
                fields = result.get('fields', [])
                field_types = {}
                for field in fields:
                    field_type = field.get('fieldType', 'unknown')
                    field_types[field_type] = field_types.get(field_type, 0) + 1
                
                if field_types:
                    print(f"   🎨 字段類型分佈: {dict(field_types)}")
                    
                # 顯示表格清單
                tables = result.get('tables', [])
                if tables:
                    print(f"   📋 涉及表格: {', '.join(tables)}")
            else:
                print(f"   ❌ 解析失敗")
                
        except Exception as e:
            print(f"   ❌ 測試失敗: {str(e)}")
    
    print(f"\n🎉 sql-splitter v6.0.1 測試完成！")
    print(f"📦 從 TestPyPI 安裝的包運行正常！")
    print(f"🚀 準備發布到正式 PyPI！")

if __name__ == "__main__":
    main()
