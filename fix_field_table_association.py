#!/usr/bin/env python3
"""
Fix Field-Table Association

🔧 Diagnose and fix why fields don't map to their tables correctly
📊 Test and validate field-table mapping logic

Author: AI Assistant
Date: 2025-08-28
"""

import sys
import os
import re

# Add local package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql_splitter'))

def fix_field_table_association():
    print("🔧 Field-Table Association Fix")
    print("=" * 50)
    
    # Import components
    from sql_splitter.core.sql_parser_ast_v6_0 import SQLParserAST
    
    # Test SQL with clear table aliases
    test_sql = "SELECT o.order_id, c.customer_name FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.status = 'active'"
    
    print(f"Test SQL: {test_sql}")
    print()
    
    # Parse with main parser
    parser = SQLParserAST()
    
    print("🔧 1. Check table aliases extraction:")
    # Manually extract FROM clause to see aliases
    from_pattern = r'\bFROM\s+([^;]+?)(?:\s+WHERE|\s+GROUP\s+BY|\s+ORDER\s+BY|\s+HAVING|\s+LIMIT|$)'
    from_match = re.search(from_pattern, test_sql, re.IGNORECASE | re.DOTALL)
    
    if from_match:
        from_clause = from_match.group(1).strip()
        print(f"   FROM clause: {from_clause}")
        
        # Extract table aliases manually
        # Pattern: table_name alias (without JOIN)
        # Pattern: table_name alias JOIN other_table other_alias
        table_aliases = {}
        
        # Simple approach: find "tablename alias" patterns
        alias_patterns = [
            r'\b([a-zA-Z_][a-zA-Z0-9_]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+(?:JOIN|WHERE|$)',
            r'\b([a-zA-Z_][a-zA-Z0-9_]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*$'
        ]
        
        for pattern in alias_patterns:
            matches = re.findall(pattern, from_clause, re.IGNORECASE)
            for table, alias in matches:
                if len(alias) <= 3 and alias.lower() not in ['join', 'on', 'where', 'and', 'or']:  # Short aliases
                    table_aliases[alias] = table
                    print(f"   Found alias: {alias} -> {table}")
    
    print(f"   Expected table aliases: {{'o': 'orders', 'c': 'customers'}}")
    
    # Parse the SQL
    result = parser.parse(test_sql)
    
    print(f"\n🔧 2. Parser results:")
    print(f"   Tables: {result.get('tables', [])}")
    print(f"   JOINs: {len(result.get('joins', []))}")
    print(f"   Fields: {len(result.get('fields', []))}")
    print(f"   WHERE: {len(result.get('whereConditions', []))}")
    
    print(f"\n🔧 3. Field details:")
    fields = result.get('fields', [])
    for i, field in enumerate(fields):
        print(f"   Field {i+1}: {field}")
        field_expr = field.get('field', '')
        current_table = field.get('table', '')
        
        print(f"      Expression: '{field_expr}'")
        print(f"      Current table: '{current_table}'")
        
        # Manual fix attempt
        if not current_table and '.' in field_expr:
            alias = field_expr.split('.')[0]
            expected_table = {'o': 'orders', 'c': 'customers'}.get(alias, '')
            print(f"      Expected table: '{expected_table}' (from alias '{alias}')")
            
            if expected_table:
                print(f"      🔧 Should fix: table = '{expected_table}'")
    
    print(f"\n🔧 4. Testing direct fix in ContentExtractor:")
    
    # Test ContentExtractor directly with correct context
    from sql_splitter.core.content_extractor import ContentExtractor
    
    extractor = ContentExtractor()
    # Set table aliases manually
    extractor.table_aliases = {'o': 'orders', 'c': 'customers'}
    print(f"   Set table aliases: {extractor.table_aliases}")
    
    # Extract fields with proper context
    fields_direct = extractor.extract_fields(test_sql)
    print(f"   Direct extraction results:")
    for i, field in enumerate(fields_direct):
        print(f"   Field {i+1}: {field}")

if __name__ == "__main__":
    fix_field_table_association()
