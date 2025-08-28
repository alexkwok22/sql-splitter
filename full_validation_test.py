#!/usr/bin/env python3
"""
Full Validation Test - SQLParserAST v6.0

🚀 Comprehensive validation of all queries after integration fixes
📊 Generate complete test reports with detailed analysis

Author: AI Assistant
Date: 2025-08-28
"""

import os
import sys
import json
import time
import traceback
from typing import Dict, List, Any

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sql_splitter'))

from sql_splitter.core.sql_parser_ast_v6_0 import SQLParserAST

def run_full_validation():
    """🚀 Run full validation on all available test queries"""
    print("🚀 SQL Parser AST v6.0 - Full Validation Test")
    print("=" * 70)
    
    # Load test queries from existing test files
    test_files = [
        'test_original_sql_results.json',
        'new_sql_examples_test_results.json'
    ]
    
    all_results = {}
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
    
    parser = SQLParserAST()
    
    # Load and test each file's queries
    for test_file in test_files:
        file_path = os.path.join(os.path.dirname(__file__), test_file)
        if os.path.exists(file_path):
            print(f"\n📂 Testing queries from: {test_file}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'detailed_results' in data:
                for result in data['detailed_results']:
                    query_name = result.get('query_name', 'unknown')
                    sql = result.get('sql', '')
                    
                    if sql:
                        print(f"   🔧 Testing: {query_name}")
                        
                        # Parse with updated parser
                        start_time = time.time()
                        parse_result = parser.parse(sql)
                        execution_time = time.time() - start_time
                        
                        # Analyze results
                        tables_count = len(parse_result.get('tables', []))
                        joins_count = len(parse_result.get('joins', []))
                        fields_count = len(parse_result.get('fields', []))
                        where_count = len(parse_result.get('whereConditions', []))
                        
                        # Count field-table associations
                        fields_with_tables = len([f for f in parse_result.get('fields', []) if f.get('table')])
                        
                        # Update stats
                        total_stats['total_queries'] += 1
                        if parse_result.get('success', False):
                            total_stats['successful_parses'] += 1
                        if parse_result.get('success', False) and tables_count > 0:
                            total_stats['structure_compliant'] += 1
                        
                        total_stats['tables_detected'] += tables_count
                        total_stats['joins_detected'] += joins_count
                        total_stats['fields_detected'] += fields_count
                        total_stats['where_detected'] += where_count
                        total_stats['field_table_associations'] += fields_with_tables
                        
                        # Store result
                        all_results[query_name] = {
                            'success': parse_result.get('success', False),
                            'tables': tables_count,
                            'joins': joins_count,
                            'fields': fields_count,
                            'where_conditions': where_count,
                            'field_table_associations': fields_with_tables,
                            'execution_time': execution_time,
                            'parser_output': parse_result
                        }
                        
                        print(f"      ✅ Tables: {tables_count}, JOINs: {joins_count}, Fields: {fields_count} ({fields_with_tables} with table), WHERE: {where_count}")
    
    # Generate comprehensive report
    print(f"\n📊 COMPREHENSIVE VALIDATION RESULTS")
    print("=" * 70)
    
    success_rate = (total_stats['successful_parses'] / total_stats['total_queries']) * 100 if total_stats['total_queries'] > 0 else 0
    structure_rate = (total_stats['structure_compliant'] / total_stats['total_queries']) * 100 if total_stats['total_queries'] > 0 else 0
    
    print(f"📋 Total Queries Tested: {total_stats['total_queries']}")
    print(f"✅ Successful Parses: {total_stats['successful_parses']} ({success_rate:.1f}%)")
    print(f"🏗️  Structure Compliant: {total_stats['structure_compliant']} ({structure_rate:.1f}%)")
    print(f"📊 Total Tables Detected: {total_stats['tables_detected']}")
    print(f"🔗 Total JOINs Detected: {total_stats['joins_detected']}")
    print(f"📝 Total Fields Detected: {total_stats['fields_detected']}")
    print(f"🔍 Total WHERE Conditions: {total_stats['where_detected']}")
    print(f"🎯 Field-Table Associations: {total_stats['field_table_associations']}")
    
    # Detailed analysis
    print(f"\n🔍 DETAILED ANALYSIS")
    print("=" * 50)
    
    # Queries with issues
    issues = []
    perfect_queries = []
    
    for query_name, result in all_results.items():
        if not result['success']:
            issues.append(f"❌ {query_name}: Parse failed")
        elif result['tables'] == 0:
            issues.append(f"⚠️  {query_name}: No tables detected")
        elif result['fields'] > 0 and result['field_table_associations'] == 0:
            issues.append(f"⚠️  {query_name}: No field-table associations")
        else:
            perfect_queries.append(query_name)
    
    print(f"🎉 Perfect Queries: {len(perfect_queries)}/{total_stats['total_queries']}")
    for query in perfect_queries[:10]:  # Show first 10
        print(f"   ✅ {query}")
    if len(perfect_queries) > 10:
        print(f"   ... and {len(perfect_queries) - 10} more")
    
    if issues:
        print(f"\n⚠️  Queries with Issues: {len(issues)}")
        for issue in issues[:10]:  # Show first 10
            print(f"   {issue}")
        if len(issues) > 10:
            print(f"   ... and {len(issues) - 10} more")
    
    # Save detailed results
    output_file = 'comprehensive_validation_results.json'
    output_data = {
        'test_summary': {
            'test_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'parser_version': '6.0_integration_fixed',
            'total_queries': total_stats['total_queries'],
            'success_rate': success_rate,
            'structure_compliance_rate': structure_rate,
            'total_stats': total_stats
        },
        'detailed_results': all_results,
        'perfect_queries': perfect_queries,
        'issues': issues
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed results saved to: {output_file}")
    
    # Final assessment
    print(f"\n🏆 FINAL ASSESSMENT")
    print("=" * 40)
    
    if success_rate >= 95 and structure_rate >= 90:
        print("🎉 EXCELLENT: Parser performs exceptionally well!")
        print("🚀 Ready for production use and final release")
    elif success_rate >= 85 and structure_rate >= 80:
        print("✅ GOOD: Parser performs well with minor issues")
        print("🔧 Consider addressing remaining edge cases")
    elif success_rate >= 70:
        print("⚠️  FAIR: Parser works but has notable issues")
        print("🛠️  Additional fixes recommended")
    else:
        print("❌ POOR: Parser has significant issues")
        print("🚨 Major fixes required")
    
    return total_stats, all_results

if __name__ == "__main__":
    try:
        stats, results = run_full_validation()
        print(f"\n✅ Validation completed successfully!")
    except Exception as e:
        print(f"\n❌ Validation failed: {str(e)}")
        traceback.print_exc()
