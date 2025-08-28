#!/usr/bin/env python3
"""
Final Version Package Test Script

Tests the complete final_version sql_splitter package with all 31 SQL queries
to validate GitHub release functionality and expect.md compliance.
"""

import sys
import os
import json
import time
from typing import Dict, List, Any

# Add the sql_splitter package to path
sys.path.insert(0, os.path.dirname(__file__))

# Import from the new final_version package
try:
    from sql_splitter import SQLParserAST, parse_sql, parse_sql_to_json
    print("✅ Successfully imported final_version sql_splitter package")
except ImportError as e:
    print(f"❌ Failed to import sql_splitter package: {e}")
    sys.exit(1)

def load_normalized_queries() -> Dict[str, str]:
    """Load the 31 normalized SQL queries"""
    queries_file = "../05_results_outputs/normalized_queries_mysql.json"
    
    try:
        with open(queries_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('normalized_queries', {})
    except FileNotFoundError:
        print(f"❌ Normalized queries file not found: {queries_file}")
        return {}

def validate_expect_md_compliance(result: Dict[str, Any], query_name: str) -> Dict[str, Any]:
    """Validate result against expect.md specification"""
    
    validation_result = {
        "query_name": query_name,
        "structure_valid": True,
        "content_valid": True,
        "structure_errors": [],
        "content_errors": []
    }
    
    # Structure validation
    required_fields = ["success", "fields", "tables", "joins", "whereConditions", "parser"]
    
    for field in required_fields:
        if field not in result:
            validation_result["structure_valid"] = False
            validation_result["structure_errors"].append(f"Missing required field: {field}")
    
    if not validation_result["structure_valid"]:
        return validation_result
    
    # Content validation
    if not isinstance(result["fields"], list):
        validation_result["content_valid"] = False
        validation_result["content_errors"].append("Fields must be a list")
    
    if not isinstance(result["tables"], list):
        validation_result["content_valid"] = False
        validation_result["content_errors"].append("Tables must be a list")
    
    if not isinstance(result["joins"], list):
        validation_result["content_valid"] = False
        validation_result["content_errors"].append("Joins must be a list")
    
    if not isinstance(result["whereConditions"], list):
        validation_result["content_valid"] = False
        validation_result["content_errors"].append("WhereConditions must be a list")
    
    # Field validation
    for i, field in enumerate(result.get("fields", [])):
        if not isinstance(field, dict):
            validation_result["content_valid"] = False
            validation_result["content_errors"].append(f"Field {i} must be a dict")
            continue
            
        if "field" not in field or not field["field"]:
            validation_result["content_valid"] = False
            validation_result["content_errors"].append(f"Field {i} has empty field name")
    
    # JOIN validation
    for i, join in enumerate(result.get("joins", [])):
        if not isinstance(join, dict):
            validation_result["content_valid"] = False
            validation_result["content_errors"].append(f"Join {i} must be a dict")
            continue
            
        required_join_fields = ["type", "leftTable", "leftField", "rightTable", "rightField"]
        for req_field in required_join_fields:
            if req_field not in join or not join[req_field]:
                validation_result["content_valid"] = False
                validation_result["content_errors"].append(f"Join {i} missing {req_field}")
    
    return validation_result

def test_single_query(query_name: str, sql: str, parser: SQLParserAST) -> Dict[str, Any]:
    """Test a single SQL query with the parser"""
    
    test_result = {
        "query_name": query_name,
        "parsing_success": False,
        "parsing_error": None,
        "parsing_time": 0,
        "result": None,
        "validation": None
    }
    
    try:
        start_time = time.time()
        result = parser.parse(sql)
        end_time = time.time()
        
        test_result["parsing_success"] = result.get("success", False)
        test_result["parsing_time"] = round(end_time - start_time, 4)
        test_result["result"] = result
        
        if not result.get("success", False):
            test_result["parsing_error"] = result.get("error", "Unknown parsing error")
        else:
            # Validate against expect.md compliance
            test_result["validation"] = validate_expect_md_compliance(result, query_name)
        
    except Exception as e:
        test_result["parsing_error"] = str(e)
        test_result["parsing_time"] = 0
    
    return test_result

def run_comprehensive_test() -> Dict[str, Any]:
    """Run comprehensive test on all 31 queries"""
    
    print("🚀 Final Version Package Comprehensive Test")
    print("=" * 70)
    print()
    
    # Load normalized queries
    print("📂 Loading normalized SQL queries...")
    queries = load_normalized_queries()
    
    if not queries:
        print("❌ No queries loaded. Exiting.")
        return {"error": "No queries loaded"}
    
    print(f"✅ Loaded {len(queries)} SQL queries")
    print()
    
    # Initialize parser
    print("🔧 Initializing SQLParserAST from final_version package...")
    parser = SQLParserAST(enable_normalization=True)
    parser_info = parser.get_parser_info()
    
    print(f"✅ Parser: {parser_info['parser_id']} v{parser_info['version']}")
    print(f"✅ Architecture: {parser_info['architecture']}")
    print(f"✅ Components: {len(parser_info['components'])} modules")
    print()
    
    # Test all queries
    print("🧪 Testing all 31 SQL queries...")
    print("-" * 50)
    
    test_results = {}
    parsing_success_count = 0
    structure_valid_count = 0
    content_valid_count = 0
    total_parsing_time = 0
    
    for i, (query_name, sql) in enumerate(queries.items(), 1):
        print(f"📊 Testing {i:2d}/31: {query_name[:40]:<40}", end="")
        
        test_result = test_single_query(query_name, sql, parser)
        test_results[query_name] = test_result
        
        total_parsing_time += test_result["parsing_time"]
        
        if test_result["parsing_success"]:
            parsing_success_count += 1
            
            if test_result["validation"]:
                if test_result["validation"]["structure_valid"]:
                    structure_valid_count += 1
                if test_result["validation"]["content_valid"]:
                    content_valid_count += 1
                
                # Status indicators
                structure_status = "✅" if test_result["validation"]["structure_valid"] else "❌"
                content_status = "✅" if test_result["validation"]["content_valid"] else "❌"
                print(f" Parse:✅ Struct:{structure_status} Content:{content_status}")
            else:
                print(f" Parse:✅ Valid:❓")
        else:
            print(f" Parse:❌ Error: {test_result['parsing_error'][:20]}...")
    
    print("-" * 50)
    print()
    
    # Summary statistics
    success_rate = (parsing_success_count / len(queries)) * 100
    structure_rate = (structure_valid_count / len(queries)) * 100
    content_rate = (content_valid_count / len(queries)) * 100
    avg_parse_time = total_parsing_time / len(queries)
    
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"🔍 Total Queries:        {len(queries)}")
    print(f"✅ Parsing Success:      {parsing_success_count}/{len(queries)} ({success_rate:.1f}%)")
    print(f"🏗️  Structure Valid:      {structure_valid_count}/{len(queries)} ({structure_rate:.1f}%)")
    print(f"📝 Content Valid:        {content_valid_count}/{len(queries)} ({content_rate:.1f}%)")
    print(f"⏱️  Average Parse Time:   {avg_parse_time:.4f}s")
    print(f"🎯 expect.md Compliance: {content_valid_count}/{len(queries)} ({content_rate:.1f}%)")
    print()
    
    # Detailed error analysis
    parsing_errors = []
    structure_errors = []
    content_errors = []
    
    for query_name, result in test_results.items():
        if not result["parsing_success"]:
            parsing_errors.append({
                "query": query_name,
                "error": result["parsing_error"]
            })
        
        if result["validation"]:
            if not result["validation"]["structure_valid"]:
                structure_errors.append({
                    "query": query_name,
                    "errors": result["validation"]["structure_errors"]
                })
            
            if not result["validation"]["content_valid"]:
                content_errors.append({
                    "query": query_name,
                    "errors": result["validation"]["content_errors"]
                })
    
    # Error reporting
    if parsing_errors:
        print("❌ Parsing Errors:")
        for error in parsing_errors:
            print(f"   • {error['query']}: {error['error']}")
        print()
    
    if structure_errors:
        print("🏗️ Structure Errors:")
        for error in structure_errors:
            print(f"   • {error['query']}: {', '.join(error['errors'])}")
        print()
    
    if content_errors:
        print("📝 Content Errors:")
        for error in content_errors:
            print(f"   • {error['query']}: {', '.join(error['errors'][:3])}")
        print()
    
    # Final assessment
    print("🎯 Final Assessment")
    print("=" * 50)
    
    if content_rate >= 95:
        print("🎉 EXCELLENT: Final version package achieves excellent expect.md compliance!")
    elif content_rate >= 90:
        print("✅ GOOD: Final version package achieves good expect.md compliance!")
    elif content_rate >= 80:
        print("⚠️ FAIR: Final version package achieves fair expect.md compliance.")
    else:
        print("❌ POOR: Final version package needs improvement for expect.md compliance.")
    
    print(f"📦 Package Status: {'READY FOR GITHUB RELEASE' if content_rate >= 90 else 'NEEDS REFINEMENT'}")
    print()
    
    # Save detailed results
    output_file = "final_version_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_summary": {
                "total_queries": len(queries),
                "parsing_success_count": parsing_success_count,
                "structure_valid_count": structure_valid_count,
                "content_valid_count": content_valid_count,
                "success_rate": success_rate,
                "structure_rate": structure_rate,
                "content_rate": content_rate,
                "average_parse_time": avg_parse_time
            },
            "detailed_results": test_results,
            "parser_info": parser_info
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Detailed results saved to: {output_file}")
    
    return {
        "success_rate": success_rate,
        "structure_rate": structure_rate,
        "content_rate": content_rate,
        "test_results": test_results
    }

if __name__ == "__main__":
    try:
        results = run_comprehensive_test()
        
        if results.get("content_rate", 0) >= 90:
            print("\n🚀 Final version package is READY FOR GITHUB RELEASE!")
            sys.exit(0)
        else:
            print("\n⚠️ Final version package needs refinement before release.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
