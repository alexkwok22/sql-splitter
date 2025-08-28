# SQL Parser v5.4 Final Patch - 使用說明

## 🚨 重要：導入問題解決方案

由於Python不支援直接導入包含連字符(`-`)的文件名，您需要使用以下方法之一：

### 方法一：使用動態導入 (推薦)

```python
import importlib.util
import json

# 動態載入解析器
spec = importlib.util.spec_from_file_location("sql_parser", "sql-parser-final-patch-v5-4.py")
sql_parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sql_parser_module)

# 創建解析器實例
parser = sql_parser_module.SQLSplitParser()

# 使用解析器
sql = """SELECT `u`.`id`, `o`.`total` 
         FROM `users` `u` 
         LEFT JOIN `orders` `o` ON `u`.`id` = `o`.`user_id`"""

result = parser.parse(sql)
print(json.dumps(result, indent=2, ensure_ascii=False))
```

### 方法二：重新命名文件 (簡單)

1. 將 `sql-parser-final-patch-v5-4.py` 重新命名為 `sql_parser_v5_4.py`
2. 然後正常導入：

```python
from sql_parser_v5_4 import SQLSplitParser
import json

# 創建解析器實例
parser = SQLSplitParser()

# 解析SQL
sql = """SELECT `u`.`id`, COUNT(`o`.`id`) AS `order_count`
         FROM `users` `u`
         LEFT JOIN `orders` `o` ON `u`.`id` = `o`.`user_id`
         GROUP BY `u`.`id`"""

result = parser.parse(sql)
print(json.dumps(result, indent=2, ensure_ascii=False))
```

### 方法三：使用包裝器文件

創建一個 `sql_parser.py` 文件作為包裝器：

```python
# sql_parser.py
import importlib.util

# 載入實際的解析器
spec = importlib.util.spec_from_file_location("sql_parser_module", "sql-parser-final-patch-v5-4.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# 匯出主要類別
SQLSplitParser = module.SQLSplitParser
parse_sql = module.parse_sql
parse_sql_to_json = module.parse_sql_to_json
```

然後您可以簡單地使用：
```python
from sql_parser import SQLSplitParser, parse_sql
```

## 📖 完整使用範例

### 基本使用

```python
import importlib.util
import json

# 載入解析器
spec = importlib.util.spec_from_file_location("sql_parser", "sql-parser-final-patch-v5-4.py")
sql_parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sql_parser_module)

parser = sql_parser_module.SQLSplitParser()

# 測試案例 1: 簡單SELECT
sql1 = "SELECT `id`, `name` FROM `users` WHERE `active` = 1"
result1 = parser.parse(sql1)

if result1['success']:
    print("✅ 解析成功!")
    print(f"📋 表格: {result1['tables']}")
    print(f"📄 字段數量: {len(result1['fields'])}")
    print(f"🔗 JOIN數量: {len(result1['joins'])}")
    print(f"🔍 WHERE條件: {result1['whereConditions']}")
else:
    print(f"❌ 解析失败: {result1['error']}")

print("\n" + "="*50)

# 測試案例 2: 複雜JOIN
sql2 = """SELECT `u`.`name`, `o`.`total`, `p`.`status`
          FROM `users` `u`
          LEFT JOIN `orders` `o` ON `u`.`id` = `o`.`user_id`
          JOIN `payments` `p` ON `o`.`id` = `p`.`order_id`
          WHERE `u`.`active` = 1"""

result2 = parser.parse(sql2)

if result2['success']:
    print("✅ 複雜SQL解析成功!")
    print(f"📋 表格: {result2['tables']}")
    
    print("🔗 JOIN詳情:")
    for i, join in enumerate(result2['joins'], 1):
        print(f"  JOIN {i}: {join['type']} {join['rightTable']}")
        print(f"    條件: {join['condition']}")
        
    print("📄 字段詳情:")
    for field in result2['fields']:
        print(f"  - {field['alias']} (來自: {field['table']})")
        
else:
    print(f"❌ 複雜SQL解析失败: {result2['error']}")
```

### 使用便捷函數

```python
import importlib.util

# 載入解析器
spec = importlib.util.spec_from_file_location("sql_parser", "sql-parser-final-patch-v5-4.py")
sql_parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sql_parser_module)

# 使用便捷函數
sql = "SELECT `name` FROM `users` WHERE `id` = 1"

# 方法1: 返回字典
result_dict = sql_parser_module.parse_sql(sql)

# 方法2: 返回JSON字符串
result_json = sql_parser_module.parse_sql_to_json(sql, indent=2)
print(result_json)
```

## 🎯 實際專案集成

### 創建專案包裝器

建議在您的專案中創建一個專用的包裝器模組：

```python
# my_sql_parser.py
"""
SQL Parser 包裝器
專用於您的專案
"""
import importlib.util
import json
import os

class SQLParserWrapper:
    def __init__(self, parser_file="sql-parser-final-patch-v5-4.py"):
        """初始化SQL解析器"""
        if not os.path.exists(parser_file):
            raise FileNotFoundError(f"找不到解析器文件: {parser_file}")
            
        spec = importlib.util.spec_from_file_location("sql_parser", parser_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        self.parser = module.SQLSplitParser()
        self.version = getattr(self.parser, 'version', 'unknown')
        
    def parse(self, sql):
        """解析SQL並返回結果"""
        return self.parser.parse(sql)
        
    def parse_to_json(self, sql, indent=2):
        """解析SQL並返回JSON字符串"""
        return self.parser.parse_to_json(sql, indent)
        
    def get_tables(self, sql):
        """只獲取表格列表"""
        result = self.parse(sql)
        return result.get('tables', []) if result['success'] else []
        
    def get_joins(self, sql):
        """只獲取JOIN資訊"""
        result = self.parse(sql)
        return result.get('joins', []) if result['success'] else []
        
    def get_fields(self, sql):
        """只獲取字段資訊"""
        result = self.parse(sql)
        return result.get('fields', []) if result['success'] else []
        
    def validate_sql(self, sql):
        """驗證SQL是否可以解析"""
        result = self.parse(sql)
        return result['success'], result.get('error', None)

# 使用範例
if __name__ == "__main__":
    # 創建解析器實例
    sql_parser = SQLParserWrapper()
    print(f"✅ SQL Parser 版本: {sql_parser.version}")
    
    # 測試SQL
    test_sql = """SELECT `u`.`name`, COUNT(`o`.`id`) AS `order_count`
                  FROM `users` `u`
                  LEFT JOIN `orders` `o` ON `u`.`id` = `o`.`user_id`
                  GROUP BY `u`.`name`"""
    
    # 驗證SQL
    is_valid, error = sql_parser.validate_sql(test_sql)
    print(f"SQL有效性: {is_valid}")
    
    if is_valid:
        print(f"📋 表格: {sql_parser.get_tables(test_sql)}")
        print(f"🔗 JOIN: {len(sql_parser.get_joins(test_sql))} 個")
        print(f"📄 字段: {len(sql_parser.get_fields(test_sql))} 個")
    else:
        print(f"❌ 錯誤: {error}")
```

然後在您的專案中：

```python
from my_sql_parser import SQLParserWrapper

# 簡單使用
parser = SQLParserWrapper()
tables = parser.get_tables("SELECT * FROM users")
print(f"涉及的表格: {tables}")
```

## 🧪 測試建議

### 運行內建測試

使用提供的測試腳本驗證功能：

```bash
python test_final_patch_complete.py
```

### 創建自己的測試

```python
# my_test.py
import importlib.util

def test_my_sql():
    # 載入解析器
    spec = importlib.util.spec_from_file_location("sql_parser", "sql-parser-final-patch-v5-4.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    parser = module.SQLSplitParser()
    
    # 您的實際SQL測試案例
    my_sql = """
    SELECT your_actual_sql_here
    """
    
    result = parser.parse(my_sql)
    
    if result['success']:
        print("✅ 您的SQL解析成功!")
        print(f"表格: {result['tables']}")
        print(f"字段: {len(result['fields'])}")
        print(f"JOIN: {len(result['joins'])}")
    else:
        print(f"❌ 解析失敗: {result['error']}")

if __name__ == "__main__":
    test_my_sql()
```

## 🔧 常見問題解決

### Q1: 為什麼不能直接 import？
A: Python模組名稱不能包含連字符(`-`)，必須使用動態導入或重新命名文件。

### Q2: 如何處理複雜的SQL？
A: 解析器已通過100%基础兼容性測試，支援大部分複雜SQL語法。

### Q3: 如何獲得更好的錯誤資訊？
A: 檢查返回結果中的 `success` 字段和 `error` 資訊。

### Q4: 性能如何？
A: 解析器設計為生產就緒，可處理中等複雜度的SQL語句。

## 📋 功能檢查清單

使用前請確認以下功能正常：

- [ ] ✅ 基本SELECT語句解析
- [ ] ✅ LEFT/RIGHT/INNER JOIN解析  
- [ ] ✅ WHERE條件提取
- [ ] ✅ 字段別名識別
- [ ] ✅ 表格別名處理
- [ ] ✅ GROUP BY支援
- [ ] ✅ MySQL函數識別
- [ ] ⚠️  帶括號FROM子句JOIN (部分支援)

## 🎊 您現在可以開始使用了！

選擇上述任一方法，開始在您的專案中使用這個功能完整的SQL解析器。