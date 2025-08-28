#!/usr/bin/env python3
"""
Field-Table Association Diagnostic

🔍 Debug why field-table association is failing
📊 Test individual methods to find root cause

Author: AI Assistant
Date: 2025-08-28
"""

import sys
import os

# Add local package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql_splitter'))

def diagnose_field_table_association():
    print("🔍 Field-Table Association Diagnostic")
    print("=" * 50)
    
    # Import components
    from sql_splitter.core.content_extractor import ContentExtractor
    
    # Test SQL with clear table aliases
    test_sql = "SELECT o.order_id, c.customer_name FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.status = 'active'"
    
    print(f"Test SQL: {test_sql}")
    print()
    
    extractor = ContentExtractor()
    
    # Set some test table aliases manually
    print("🔧 1. Setting up table aliases manually:")
    test_aliases = {'o': 'orders', 'c': 'customers'}
    extractor.table_aliases = test_aliases
    print(f"   Table aliases: {test_aliases}")
    
    # Test field extraction
    print("\n🔧 2. Testing field extraction:")
    fields = extractor.extract_fields(test_sql)
    print(f"   Fields found: {len(fields)}")
    for i, field in enumerate(fields):
        print(f"   Field {i+1}: {field}")
        
        # Manually test table determination for this field
        field_expr = field.get('field', '')
        print(f"      Field expression: '{field_expr}'")
        
        # Test if _determine_field_table method exists
        if hasattr(extractor, '_determine_field_table'):
            try:
                table_result = extractor._determine_field_table(field_expr)
                print(f"      _determine_field_table result: '{table_result}'")
            except Exception as e:
                print(f"      _determine_field_table error: {e}")
        else:
            print("      ❌ _determine_field_table method does not exist!")
        
        # Test if _resolve_table_alias method exists
        if hasattr(extractor, '_resolve_table_alias'):
            try:
                if '.' in field_expr:
                    alias_part = field_expr.split('.')[0]
                    resolved = extractor._resolve_table_alias(alias_part)
                    print(f"      _resolve_table_alias('{alias_part}') = '{resolved}'")
            except Exception as e:
                print(f"      _resolve_table_alias error: {e}")
        else:
            print("      ❌ _resolve_table_alias method does not exist!")
    
    # Check what methods actually exist
    print(f"\n🔧 3. Available methods in ContentExtractor:")
    methods = [method for method in dir(extractor) if method.startswith('_')]
    for method in sorted(methods):
        print(f"   - {method}")
    
    print("\n✅ Field-Table Association diagnostic completed")

if __name__ == "__main__":
    diagnose_field_table_association()
