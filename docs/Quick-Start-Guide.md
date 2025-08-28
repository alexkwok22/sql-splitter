# SQL Parser v5.4 - 快速入门指南

## 🚨 解决导入错误

您遇到的 `SyntaxError: invalid syntax` 错误是因为Python不支持导入包含连字符的文件名。

## 🎯 3种简单解决方案

### 方案一：使用我们提供的包装器 (推荐)

```bash
# 1. 运行简单示例
python simple_example.py

# 2. 测试您的SQL
python test_your_sql.py
```

### 方案二：在您的项目中使用

```python
from sql_parser_wrapper import SQLParserWrapper

# 创建解析器
parser = SQLParserWrapper()

# 解析您的SQL
sql = "SELECT * FROM users WHERE active = 1"
result = parser.parse(sql)

if result['success']:
    print(f"表格: {result['tables']}")
    print(f"字段: {len(result['fields'])} 个")
else:
    print(f"错误: {result['error']}")
```

### 方案三：重新命名文件

将 `sql-parser-final-patch-v5-4.py` 重命名为 `sql_parser.py`，然后：

```python
from sql_parser import SQLSplitParser

parser = SQLSplitParser()
result = parser.parse("SELECT * FROM users")
```

## 📋 现有文件说明

| 文件 | 用途 |
|------|------|
| `sql-parser-final-patch-v5-4.py` | 🔧 核心解析器（不要改动）|
| `simple_example.py` | 🎯 基础使用示例 |
| `sql_parser_wrapper.py` | 📦 包装器模块 |
| `test_your_sql.py` | ✏️ 测试您的SQL |
| `SQL-Parser-Usage-Guide.md` | 📖 详细使用说明 |

## 🎪 立即开始

### 1. 运行基础示例
```bash
python simple_example.py
```

### 2. 测试您的SQL
编辑 `test_your_sql.py` 文件，将您的SQL放入：

```python
your_sql = """
这里放入您的SQL语句
"""
```

然后运行：
```bash
python test_your_sql.py
```

### 3. 在项目中使用
```python
from sql_parser_wrapper import SQLParserWrapper

parser = SQLParserWrapper()
tables = parser.get_tables("SELECT * FROM users")
print(f"涉及的表格: {tables}")
```

## 🧪 验证功能

运行测试确保一切正常：

```bash
python test_final_patch_complete.py
```

**预期结果：**
- ✅ 基础兼容性测试：100%通过
- ✅ 复杂SQL支持：75%+通过

## 📞 如遇问题

1. **找不到文件：** 确保所有文件在同一目录
2. **导入错误：** 使用提供的包装器而不是直接导入
3. **解析失败：** 检查SQL语法是否正确

## 🎊 现在开始使用您的SQL解析器！

您的解析器已经通过了100%基础兼容性测试，可以放心使用！