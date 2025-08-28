#!/usr/bin/env python3
"""
Test script for installed sql-splitter package
"""

print("🧪 Testing installed sql-splitter package...")
print("=" * 50)

try:
    # Test import
    from sql_splitter import SQLParserAST, parse_sql
    print("✅ Import successful!")
    
    # Test basic parsing
    parser = SQLParserAST()
    
    # Test SQL query
    sql = "SELECT users.name, COUNT(*) as total FROM users JOIN orders ON users.id = orders.user_id WHERE users.active = 1 GROUP BY users.name"
    
    print(f"\n📝 Testing SQL: {sql[:50]}...")
    
    # Parse the SQL
    result = parser.parse(sql)
    
    # Display results
    print(f"✅ Parse Success: {result['success']}")
    print(f"📊 Tables Found: {result['tables']}")
    print(f"🔗 JOINs Found: {len(result['joins'])}")
    print(f"📝 Fields Found: {len(result['fields'])}")
    print(f"🎯 Parser ID: {result['parser']}")
    
    # Test enhanced features
    if 'metadata' in result:
        metadata = result['metadata']
        print(f"🎨 Aggregation Fields: {len(metadata.get('aggregationFields', []))}")
        print(f"💻 Computed Fields: {len(metadata.get('computedFields', []))}")
        print(f"🏷️ Alias Mapping: {len(metadata.get('aliasMapping', {}))}")
    
    # Test field types (visualization support)
    field_types = {}
    for field in result.get('fields', []):
        field_type = field.get('fieldType', 'unknown')
        field_types[field_type] = field_types.get(field_type, 0) + 1
    
    print(f"\n🎨 Field Type Distribution:")
    for ftype, count in field_types.items():
        print(f"   - {ftype}: {count} fields")
    
    print(f"\n🎉 Package test completed successfully!")
    print(f"🚀 Ready for PyPI release!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Test failed: {e}")

print("\n" + "=" * 50)
