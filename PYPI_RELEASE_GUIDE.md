# PyPI 發布指南 - SQL Splitter

## 📋 **發布前檢查清單**

### ✅ **包結構驗證**
- [x] setup.py 配置完整
- [x] __init__.py 文件存在
- [x] README.md 文檔完整  
- [x] LICENSE 文件存在
- [x] requirements.txt 依賴清單
- [x] 核心功能測試通過 (100% success rate)

### ✅ **版本管理**
- [x] 當前版本: 6.0.0
- [ ] 確認版本號遵循語義化版本控制 (SemVer)
- [ ] 更新 CHANGELOG.md (可選)

---

## 🔧 **第一步：安裝發布工具**

```bash
pip install --upgrade build twine
```

## 🏗️ **第二步：構建包**

在 `final_version` 目錄中執行：

```bash
# 清理舊的構建文件
rm -rf dist/ build/ *.egg-info/

# 構建包
python -m build
```

這將在 `dist/` 目錄中生成：
- `sql-splitter-6.0.0.tar.gz` (源碼分發)
- `sql_splitter-6.0.0-py3-none-any.whl` (輪子分發)

## 🧪 **第三步：本地測試**

### **測試構建的包：**
```bash
# 創建虛擬環境測試
python -m venv test_env
test_env\Scripts\activate  # Windows
# source test_env/bin/activate  # Linux/Mac

# 安裝構建的包
pip install dist/sql_splitter-6.0.0-py3-none-any.whl

# 測試導入
python -c "from sql_splitter import SQLParserAST; print('✅ Import successful')"
```

## 📦 **第四步：PyPI 帳戶設置**

### **1. 註冊 PyPI 帳戶**
- 前往 https://pypi.org/account/register/
- 註冊新帳戶並驗證郵箱

### **2. 註冊 TestPyPI 帳戶 (推薦先測試)**
- 前往 https://test.pypi.org/account/register/
- 註冊測試環境帳戶

### **3. 創建 API Token**
在 PyPI 帳戶設置中：
- Account settings → API tokens → Add API token
- 保存 token 到安全位置

## 🚀 **第五步：上傳到 TestPyPI (測試)**

### **使用 API Token 上傳：**
```bash
# 上傳到 TestPyPI 測試
python -m twine upload --repository testpypi dist/*

# 會要求輸入：
# Username: __token__
# Password: [你的 TestPyPI API token]
```

### **測試從 TestPyPI 安裝：**
```bash
# 從 TestPyPI 安裝測試
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ sql-splitter

# 測試功能
python -c "
from sql_splitter import parse_sql
result = parse_sql('SELECT * FROM users')
print(f'✅ Test successful: {result[\"success\"]}')
"
```

## 🎯 **第六步：正式發布到 PyPI**

確認 TestPyPI 測試成功後：

```bash
# 上傳到正式 PyPI
python -m twine upload dist/*

# 輸入正式 PyPI API token
```

## 📝 **第七步：驗證發布成功**

### **檢查 PyPI 頁面：**
- 前往 https://pypi.org/project/sql-splitter/
- 確認頁面顯示正確

### **測試安裝：**
```bash
# 創建新的測試環境
python -m venv verify_env
verify_env\Scripts\activate

# 從 PyPI 安裝
pip install sql-splitter

# 完整功能測試
python -c "
from sql_splitter import SQLParserAST

# 測試解析
parser = SQLParserAST()
sql = '''
SELECT users.name, COUNT(*) as total 
FROM users 
JOIN orders ON users.id = orders.user_id 
GROUP BY users.name
'''

result = parser.parse(sql)
print(f'✅ Parse success: {result[\"success\"]}')
print(f'📊 Tables: {result[\"tables\"]}')
print(f'🔗 JOINs: {len(result[\"joins\"])}')
print(f'📝 Fields: {len(result[\"fields\"])}')
"
```

---

## ⚙️ **進階配置選項**

### **設定 .pypirc 文件 (可選):**
創建 `~/.pypirc` 文件：
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = [你的 PyPI API token]

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = [你的 TestPyPI API token]
```

### **GitHub Actions 自動發布 (可選):**
創建 `.github/workflows/publish.yml`：
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

---

## 🎊 **發布後步驟**

### **1. 更新文檔**
- 更新 README.md 的安裝說明
- 添加 PyPI badge: `[![PyPI version](https://badge.fury.io/py/sql-splitter.svg)](https://badge.fury.io/py/sql-splitter)`
- GitHub 項目地址: https://github.com/alexkwok22/sql-splitter

### **2. 宣傳推廣**
- 在 GitHub 創建 Release
- 分享到相關開發者社群
- 寫部落格文章介紹功能

### **3. 版本管理**
- 為未來更新準備語義化版本控制
- 設置 CI/CD 自動測試和發布流程

---

## 🛠️ **故障排除**

### **常見問題：**

**問題：上傳被拒絕**
```
ERROR: Package 'sql-splitter' already exists
```
**解決：** 更新 setup.py 中的版本號

**問題：導入錯誤**
```
ModuleNotFoundError: No module named 'sql_splitter'
```
**解決：** 檢查包結構和 __init__.py 文件

**問題：依賴衝突**
**解決：** 檢查 requirements.txt 和 setup.py 的依賴版本

---

## 📞 **支援資源**

- **PyPI 官方文檔**: https://packaging.python.org/
- **Twine 文檔**: https://twine.readthedocs.io/
- **包結構指南**: https://packaging.python.org/tutorials/packaging-projects/

**🎯 記住：先在 TestPyPI 測試，確認無誤後再發布到正式 PyPI！**
