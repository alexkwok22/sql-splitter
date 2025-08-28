# SQL Parser Module - Test Specifications (Enhanced for SQL Visualization Components)

## Module Requirements

### 功能需求
此 SQL 分拆模組需要能夠解析複雜的 SQL SELECT 語句，並提取以下結構化資訊以支援 SQL 圖像化元件開發：

1. **Tables (資料表)**
   - 主表格識別
   - 所有引用的表格（包含 JOIN 的表格）
   - 表格別名處理
   - 別名映射追蹤

2. **Fields (欄位) - 增強版**
   - SELECT 子句中的所有欄位
   - 欄位別名（AS 語法）
   - 複雜表達式（函數、運算）
   - 聚合函數識別
   - **新增：欄位類型分類** (column, aggregation, expression, computed)
   - **新增：聚合範圍追蹤** (涉及的表格列表)
   - **新增：支援無特定表格歸屬** (例如 COUNT(*))

3. **Joins (連接)**
   - JOIN 類型識別（INNER, LEFT, RIGHT, FULL）
   - JOIN 條件解析
   - 連接表格與條件對應

4. **Where Conditions (條件)**
   - WHERE 子句條件分析
   - 邏輯運算符處理（AND, OR, NOT）
   - 比較運算符與值

5. **Metadata (元數據) - 新增**
   - 別名映射信息
   - 未解析項目追蹤
   - 聚合和計算欄位分類

### 技術規格
- **輸入：** SQL SELECT 語句（字串）
- **輸出：** JSON 格式的結構化資料（支援 SQL 圖像化元件）
- **Parser 識別碼：** "sqlsplit"
- **SQL 方言：** MySQL 語法（支援舊式逗號分隔 FROM 語法）
- **引號格式：** MySQL 反引號 (`) 和標準 SQL（兩者皆支援）
- **錯誤處理：** 對於無法解析的 SQL，需回傳錯誤資訊
- **編碼：** 支援 UTF-8 中文字元
- **圖像化支援：** 提供足夠信息用於 SQL 關係圖生成

### JSON 輸出格式（增強版）
```json
{
  "success": true,
  "fields": [
    {
      "table": "table_name",
      "field": "`table`.`column` AS `alias`",
      "alias": "alias_name", 
      "groupBy": false,
      "fieldType": "column",
      "involvedTables": ["table_name"]
    },
    {
      "table": null,
      "field": "COUNT(*)",
      "alias": "total_count",
      "groupBy": false,
      "fieldType": "aggregation",
      "aggregationScope": ["table1", "table2"],
      "involvedTables": ["table1", "table2"]
    },
    {
      "table": "primary_table",
      "field": "SUM(table1.amount + COALESCE(table2.bonus, 0))",
      "alias": "total_amount",
      "groupBy": false,
      "fieldType": "expression",
      "involvedTables": ["table1", "table2"]
    }
  ],
  "tables": ["table1", "table2"],
  "joins": [
    {
      "type": "LEFT|INNER|RIGHT|FULL",
      "leftTable": "table1",
      "leftField": "field1",
      "rightTable": "table2", 
      "rightField": "field2",
      "condition": "(`table1`.`field1` = `table2`.`field2`)"
    }
  ],
  "whereConditions": ["`table`.`field` = 'value'"],
  "parser": "sqlsplit",
  "metadata": {
    "aliasMapping": {
      "t1": "table1",
      "t2": "table2"
4. 驗證錯誤處理機制
5. 檢查 MySQL 函數與語法正確解析

---

## Test Cases

以下測試案例基於 momo 資料庫的實際 view 定義：

### Test Case 1: mv_item

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `mv_item` AS select date_format(`mt_item`.`iCreateT`,'%Y-%m') AS `i_month`,`mt_item`.`DetailsID` AS `DetailsID`,`mt_item`.`Details_OrderID` AS `Details_OrderID`,`mt_item`.`iType` AS `iType`,`mt_item`.`iDesc` AS `iDesc`,`mt_item`.`iLink` AS `iLink`,`mt_item`.`iQty` AS `iQty`,`mt_item`.`iPrice` AS `iPrice`,`mt_item`.`iStatus` AS `iStatus`,`mt_item`.`iUpdateT` AS `iUpdateT`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,`mv_item_status_desc`.`Remarks` AS `Remarks`,`mv_order`.`Customer` AS `Customer`,`mv_order`.`Order_Status_Name` AS `Order_status_name`,`mv_order`.`Order_Status` AS `Order_Status`,`mt_item`.`iPic` AS `iPic`,`mt_item`.`igroup` AS `iGroup`,`mt_item`.`iTrack` AS `iTrack`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from (((`mt_item` join `mv_order` on(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`)) left join `mv_item_status_desc` on(`mt_item`.`iType` = `mv_item_status_desc`.`Item_Type` and `mt_item`.`iStatus` = `mv_item_status_desc`.`DESC_CODE`)) left join `mv_item_type_desc` on(`mt_item`.`iType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_item`.`iDeleted` < 1
```

#### Extracted SELECT SQL:
```sql
select date_format(`mt_item`.`iCreateT`,'%Y-%m') AS `i_month`,`mt_item`.`DetailsID` AS `DetailsID`,`mt_item`.`Details_OrderID` AS `Details_OrderID`,`mt_item`.`iType` AS `iType`,`mt_item`.`iDesc` AS `iDesc`,`mt_item`.`iLink` AS `iLink`,`mt_item`.`iQty` AS `iQty`,`mt_item`.`iPrice` AS `iPrice`,`mt_item`.`iStatus` AS `iStatus`,`mt_item`.`iUpdateT` AS `iUpdateT`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,`mv_item_status_desc`.`Remarks` AS `Remarks`,`mv_order`.`Customer` AS `Customer`,`mv_order`.`Order_Status_Name` AS `Order_status_name`,`mv_order`.`Order_Status` AS `Order_Status`,`mt_item`.`iPic` AS `iPic`,`mt_item`.`igroup` AS `iGroup`,`mt_item`.`iTrack` AS `iTrack`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from (((`mt_item` join `mv_order` on(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`)) left join `mv_item_status_desc` on(`mt_item`.`iType` = `mv_item_status_desc`.`Item_Type` and `mt_item`.`iStatus` = `mv_item_status_desc`.`DESC_CODE`)) left join `mv_item_type_desc` on(`mt_item`.`iType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_item`.`iDeleted` < 1
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "mt_item",
      "field": "DATE_FORMAT(`mt_item`.`iCreateT`, '%Y-%m') AS `i_month`",
      "alias": "i_month",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`DetailsID` AS `DetailsID`",
      "alias": "DetailsID",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`Details_OrderID` AS `Details_OrderID`",
      "alias": "Details_OrderID",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`iType` AS `iType`",
      "alias": "iType",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`iDesc` AS `iDesc`",
      "alias": "iDesc",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`iLink` AS `iLink`",
      "alias": "iLink",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`iQty` AS `iQty`",
      "alias": "iQty",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`iPrice` AS `iPrice`",
      "alias": "iPrice",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`iStatus` AS `iStatus`",
      "alias": "iStatus",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`iUpdateT` AS `iUpdateT`",
      "alias": "iUpdateT",
      "groupBy": false
    },
    {
      "table": "mv_item_type_desc",
      "field": "`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`",
      "alias": "Type_Name",
      "groupBy": false
    },
    {
      "table": "mv_item_status_desc",
      "field": "`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`",
      "alias": "Status_NAME",
      "groupBy": false
    },
    {
      "table": "mv_item_status_desc",
      "field": "`mv_item_status_desc`.`Remarks` AS `Remarks`",
      "alias": "Remarks",
      "groupBy": false
    },
    {
      "table": "mv_order",
      "field": "`mv_order`.`Customer` AS `Customer`",
      "alias": "Customer",
      "groupBy": false
    },
    {
      "table": "mv_order",
      "field": "`mv_order`.`Order_Status_Name` AS `Order_status_name`",
      "alias": "Order_status_name",
      "groupBy": false
    },
    {
      "table": "mv_order",
      "field": "`mv_order`.`Order_Status` AS `Order_Status`",
      "alias": "Order_Status",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`iPic` AS `iPic`",
      "alias": "iPic",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`igroup` AS `iGroup`",
      "alias": "iGroup",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "`mt_item`.`iTrack` AS `iTrack`",
      "alias": "iTrack",
      "groupBy": false
    },
    {
      "table": "mv_item_status_desc",
      "field": "IF(`mv_item_status_desc`.`Remarks` = 'finish', 1, 0) AS `finish`",
      "alias": "finish",
      "groupBy": false
    }
  ],
  "tables": [
    "mt_item",
    "mv_item_type_desc",
    "mv_item_status_desc",
    "mv_order"
  ],
  "joins": [
    {
      "type": "INNER",
      "leftTable": "mt_item",
      "leftField": "Details_OrderID",
      "rightTable": "mv_order",
      "rightField": "OrderID",
      "condition": "(`mt_item`.`Details_OrderID` = `mv_order`.`OrderID`)"
    },
    {
      "type": "LEFT",
      "leftTable": "mt_item",
      "leftField": "iType",
      "rightTable": "mv_item_status_desc",
      "rightField": "Item_Type",
      "condition": "(`mt_item`.`iType` = `mv_item_status_desc`.`Item_Type` AND `mt_item`.`iStatus` = `mv_item_status_desc`.`DESC_CODE`)"
    },
    {
      "type": "LEFT",
      "leftTable": "mt_item",
      "leftField": "iType",
      "rightTable": "mv_item_type_desc",
      "rightField": "DESC_CODE",
      "condition": "(`mt_item`.`iType` = `mv_item_type_desc`.`DESC_CODE`)"
    }
  ],
  "whereConditions": [
    "`mt_item`.`iDeleted` < 1"
  ],
  "parser": "sqlsplit"
}
```

---

---


### Test Case 2: mv_item_status_desc

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `mv_item_status_desc` AS select `mt_status_desc`.`Desc_ID` AS `Desc_ID`,`mt_status_desc`.`DESC_NAME` AS `DESC_NAME`,`mt_status_desc`.`DESC_CODE` AS `DESC_CODE`,`mt_status_desc`.`FOR_TABLE` AS `FOR_TABLE`,`mt_status_desc`.`Remarks` AS `Remarks`,`mt_status_desc`.`Item_Type` AS `Item_Type` from `mt_status_desc` where `mt_status_desc`.`FOR_TABLE` = 'iStatus'
```

#### Extracted SELECT SQL:
```sql
select `mt_status_desc`.`Desc_ID` AS `Desc_ID`,`mt_status_desc`.`DESC_NAME` AS `DESC_NAME`,`mt_status_desc`.`DESC_CODE` AS `DESC_CODE`,`mt_status_desc`.`FOR_TABLE` AS `FOR_TABLE`,`mt_status_desc`.`Remarks` AS `Remarks`,`mt_status_desc`.`Item_Type` AS `Item_Type` from `mt_status_desc` where `mt_status_desc`.`FOR_TABLE` = 'iStatus'
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`Desc_ID` AS `Desc_ID`",
      "alias": "Desc_ID",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`DESC_NAME` AS `DESC_NAME`",
      "alias": "DESC_NAME",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`DESC_CODE` AS `DESC_CODE`",
      "alias": "DESC_CODE",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`FOR_TABLE` AS `FOR_TABLE`",
      "alias": "FOR_TABLE",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`Remarks` AS `Remarks`",
      "alias": "Remarks",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`Item_Type` AS `Item_Type`",
      "alias": "Item_Type",
      "groupBy": false
    }
  ],
  "tables": [
    "mt_status_desc"
  ],
  "joins": [],
  "whereConditions": [
    "`mt_status_desc`.`FOR_TABLE` = 'iStatus'"
  ],
  "parser": "sqlsplit"
}
```

---

---


### Test Case 3: mv_item_type_desc

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `mv_item_type_desc` AS select `mt_status_desc`.`Desc_ID` AS `Desc_ID`,`mt_status_desc`.`DESC_NAME` AS `DESC_NAME`,`mt_status_desc`.`DESC_CODE` AS `DESC_CODE`,`mt_status_desc`.`FOR_TABLE` AS `FOR_TABLE`,`mt_status_desc`.`Remarks` AS `Remarks` from `mt_status_desc` where `mt_status_desc`.`FOR_TABLE` = 'itype'
```

#### Extracted SELECT SQL:
```sql
select `mt_status_desc`.`Desc_ID` AS `Desc_ID`,`mt_status_desc`.`DESC_NAME` AS `DESC_NAME`,`mt_status_desc`.`DESC_CODE` AS `DESC_CODE`,`mt_status_desc`.`FOR_TABLE` AS `FOR_TABLE`,`mt_status_desc`.`Remarks` AS `Remarks` from `mt_status_desc` where `mt_status_desc`.`FOR_TABLE` = 'itype'
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`Desc_ID` AS `Desc_ID`",
      "alias": "Desc_ID",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`DESC_NAME` AS `DESC_NAME`",
      "alias": "DESC_NAME",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`DESC_CODE` AS `DESC_CODE`",
      "alias": "DESC_CODE",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`FOR_TABLE` AS `FOR_TABLE`",
      "alias": "FOR_TABLE",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`Remarks` AS `Remarks`",
      "alias": "Remarks",
      "groupBy": false
    }
  ],
  "tables": [
    "mt_status_desc"
  ],
  "joins": [],
  "whereConditions": [
    "`mt_status_desc`.`FOR_TABLE` = 'itype'"
  ],
  "parser": "sqlsplit"
}
```

---

---


### Test Case 4: mv_opic

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `mv_opic` AS select `mt_opic`.`op_orderid` AS `op_orderid`,sum(`mt_opic`.`op_price`) AS `paid` from `mt_opic` group by `mt_opic`.`op_orderid`
```

#### Extracted SELECT SQL:
```sql
select `mt_opic`.`op_orderid` AS `op_orderid`,sum(`mt_opic`.`op_price`) AS `paid` from `mt_opic` group by `mt_opic`.`op_orderid`
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "mt_opic",
      "field": "`mt_opic`.`op_orderid` AS `op_orderid`",
      "alias": "op_orderid",
      "groupBy": true
    },
    {
      "table": "mt_opic",
      "field": "SUM(`mt_opic`.`op_price`) AS `paid`",
      "alias": "paid",
      "groupBy": false
    }
  ],
  "tables": [
    "mt_opic"
  ],
  "joins": [],
  "whereConditions": [],
  "parser": "sqlsplit"
}
```

---

---


### Test Case 5: mv_order

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `mv_order` AS select date_format(`mt_order`.`Create_date`,'%Y-%m') AS `o_month`,`mt_order`.`OrderID` AS `OrderID`,`mt_order`.`Customer` AS `Customer`,`mt_order`.`Order_Status` AS `Order_Status`,`mt_order`.`Create_date` AS `Create_date`,`mt_order`.`last_update` AS `last_update`,`mt_order`.`Order_Remarks1` AS `Order_Remarks1`,`mt_order`.`Order_Remarks2` AS `Order_Remarks2`,`mt_order`.`IG` AS `IG`,`mt_order`.`WHATAPP` AS `WHATAPP`,`mt_order`.`DeliveryAdress1` AS `DeliveryAdress1`,`mt_order`.`DeliveryAdress2` AS `DeliveryAdress2`,`mt_order`.`Contact_name` AS `Contact_name`,`mt_order`.`Contact_number` AS `Contact_number`,`mt_order`.`Contact_email` AS `Contact_email`,`mt_order`.`State` AS `State`,`mt_order`.`Token` AS `Token`,`mt_order`.`Pic` AS `Pic`,`mt_order`.`PaymentStatus` AS `PaymentStatus`,`mv_order_patmentstatus`.`DESC_NAME` AS `P_name`,`mt_status_desc`.`DESC_NAME` AS `Order_Status_Name`,`mv_ordervalue`.`OrderQty` AS `OrderQty`,`mv_ordervalue`.`TotalPrice` AS `TotalPrice`,`mt_order`.`bookmark` AS `bookmark`,`mv_opic`.`paid` AS `paid` from ((((`mt_order` left join `mv_ordervalue` on(`mv_ordervalue`.`Details_OrderID` = `mt_order`.`OrderID`)) join `mv_order_patmentstatus` on(`mv_order_patmentstatus`.`DESC_CODE` = `mt_order`.`PaymentStatus`)) join `mt_status_desc` on(`mt_status_desc`.`DESC_CODE` = `mt_order`.`Order_Status`)) left join `mv_opic` on(`mv_opic`.`op_orderid` = `mt_order`.`OrderID`)) where `mt_status_desc`.`FOR_TABLE` = 'Order'
```

#### Extracted SELECT SQL:
```sql
select date_format(`mt_order`.`Create_date`,'%Y-%m') AS `o_month`,`mt_order`.`OrderID` AS `OrderID`,`mt_order`.`Customer` AS `Customer`,`mt_order`.`Order_Status` AS `Order_Status`,`mt_order`.`Create_date` AS `Create_date`,`mt_order`.`last_update` AS `last_update`,`mt_order`.`Order_Remarks1` AS `Order_Remarks1`,`mt_order`.`Order_Remarks2` AS `Order_Remarks2`,`mt_order`.`IG` AS `IG`,`mt_order`.`WHATAPP` AS `WHATAPP`,`mt_order`.`DeliveryAdress1` AS `DeliveryAdress1`,`mt_order`.`DeliveryAdress2` AS `DeliveryAdress2`,`mt_order`.`Contact_name` AS `Contact_name`,`mt_order`.`Contact_number` AS `Contact_number`,`mt_order`.`Contact_email` AS `Contact_email`,`mt_order`.`State` AS `State`,`mt_order`.`Token` AS `Token`,`mt_order`.`Pic` AS `Pic`,`mt_order`.`PaymentStatus` AS `PaymentStatus`,`mv_order_patmentstatus`.`DESC_NAME` AS `P_name`,`mt_status_desc`.`DESC_NAME` AS `Order_Status_Name`,`mv_ordervalue`.`OrderQty` AS `OrderQty`,`mv_ordervalue`.`TotalPrice` AS `TotalPrice`,`mt_order`.`bookmark` AS `bookmark`,`mv_opic`.`paid` AS `paid` from ((((`mt_order` left join `mv_ordervalue` on(`mv_ordervalue`.`Details_OrderID` = `mt_order`.`OrderID`)) join `mv_order_patmentstatus` on(`mv_order_patmentstatus`.`DESC_CODE` = `mt_order`.`PaymentStatus`)) join `mt_status_desc` on(`mt_status_desc`.`DESC_CODE` = `mt_order`.`Order_Status`)) left join `mv_opic` on(`mv_opic`.`op_orderid` = `mt_order`.`OrderID`)) where `mt_status_desc`.`FOR_TABLE` = 'Order'
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "mt_order",
      "field": "DATE_FORMAT(`mt_order`.`Create_date`, '%Y-%m') AS `o_month`",
      "alias": "o_month",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`OrderID` AS `OrderID`",
      "alias": "OrderID",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`Customer` AS `Customer`",
      "alias": "Customer",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`Order_Status` AS `Order_Status`",
      "alias": "Order_Status",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`Create_date` AS `Create_date`",
      "alias": "Create_date",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`last_update` AS `last_update`",
      "alias": "last_update",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`Order_Remarks1` AS `Order_Remarks1`",
      "alias": "Order_Remarks1",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`Order_Remarks2` AS `Order_Remarks2`",
      "alias": "Order_Remarks2",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`IG` AS `IG`",
      "alias": "IG",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`WHATAPP` AS `WHATAPP`",
      "alias": "WHATAPP",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`DeliveryAdress1` AS `DeliveryAdress1`",
      "alias": "DeliveryAdress1",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`DeliveryAdress2` AS `DeliveryAdress2`",
      "alias": "DeliveryAdress2",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`Contact_name` AS `Contact_name`",
      "alias": "Contact_name",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`Contact_number` AS `Contact_number`",
      "alias": "Contact_number",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`Contact_email` AS `Contact_email`",
      "alias": "Contact_email",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`State` AS `State`",
      "alias": "State",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`Token` AS `Token`",
      "alias": "Token",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`Pic` AS `Pic`",
      "alias": "Pic",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`PaymentStatus` AS `PaymentStatus`",
      "alias": "PaymentStatus",
      "groupBy": false
    },
    {
      "table": "mv_order_patmentstatus",
      "field": "`mv_order_patmentstatus`.`DESC_NAME` AS `P_name`",
      "alias": "P_name",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`DESC_NAME` AS `Order_Status_Name`",
      "alias": "Order_Status_Name",
      "groupBy": false
    },
    {
      "table": "mv_ordervalue",
      "field": "`mv_ordervalue`.`OrderQty` AS `OrderQty`",
      "alias": "OrderQty",
      "groupBy": false
    },
    {
      "table": "mv_ordervalue",
      "field": "`mv_ordervalue`.`TotalPrice` AS `TotalPrice`",
      "alias": "TotalPrice",
      "groupBy": false
    },
    {
      "table": "mt_order",
      "field": "`mt_order`.`bookmark` AS `bookmark`",
      "alias": "bookmark",
      "groupBy": false
    },
    {
      "table": "mv_opic",
      "field": "`mv_opic`.`paid` AS `paid`",
      "alias": "paid",
      "groupBy": false
    }
  ],
  "tables": [
    "mv_opic",
    "mt_order",
    "mt_status_desc",
    "mv_order_patmentstatus",
    "mv_ordervalue"
  ],
  "joins": [
    {
      "type": "LEFT",
      "leftTable": "mt_order",
      "leftField": "OrderID",
      "rightTable": "mv_ordervalue",
      "rightField": "Details_OrderID",
      "condition": "(`mv_ordervalue`.`Details_OrderID` = `mt_order`.`OrderID`)"
    },
    {
      "type": "INNER",
      "leftTable": "mt_order",
      "leftField": "PaymentStatus",
      "rightTable": "mv_order_patmentstatus",
      "rightField": "DESC_CODE",
      "condition": "(`mv_order_patmentstatus`.`DESC_CODE` = `mt_order`.`PaymentStatus`)"
    },
    {
      "type": "INNER",
      "leftTable": "mt_order",
      "leftField": "Order_Status",
      "rightTable": "mt_status_desc",
      "rightField": "DESC_CODE",
      "condition": "(`mt_status_desc`.`DESC_CODE` = `mt_order`.`Order_Status`)"
    },
    {
      "type": "LEFT",
      "leftTable": "mt_order",
      "leftField": "OrderID",
      "rightTable": "mv_opic",
      "rightField": "op_orderid",
      "condition": "(`mv_opic`.`op_orderid` = `mt_order`.`OrderID`)"
    }
  ],
  "whereConditions": [
    "`mt_status_desc`.`FOR_TABLE` = 'Order'"
  ],
  "parser": "sqlsplit"
}
```

---

---


### Test Case 6: mv_order_patmentstatus

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `mv_order_patmentstatus` AS select `mt_status_desc`.`Desc_ID` AS `Desc_ID`,`mt_status_desc`.`DESC_NAME` AS `DESC_NAME`,`mt_status_desc`.`DESC_CODE` AS `DESC_CODE`,`mt_status_desc`.`FOR_TABLE` AS `FOR_TABLE`,`mt_status_desc`.`Remarks` AS `Remarks` from `mt_status_desc` where `mt_status_desc`.`FOR_TABLE` = 'Pstatus'
```

#### Extracted SELECT SQL:
```sql
select `mt_status_desc`.`Desc_ID` AS `Desc_ID`,`mt_status_desc`.`DESC_NAME` AS `DESC_NAME`,`mt_status_desc`.`DESC_CODE` AS `DESC_CODE`,`mt_status_desc`.`FOR_TABLE` AS `FOR_TABLE`,`mt_status_desc`.`Remarks` AS `Remarks` from `mt_status_desc` where `mt_status_desc`.`FOR_TABLE` = 'Pstatus'
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`Desc_ID` AS `Desc_ID`",
      "alias": "Desc_ID",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`DESC_NAME` AS `DESC_NAME`",
      "alias": "DESC_NAME",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`DESC_CODE` AS `DESC_CODE`",
      "alias": "DESC_CODE",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`FOR_TABLE` AS `FOR_TABLE`",
      "alias": "FOR_TABLE",
      "groupBy": false
    },
    {
      "table": "mt_status_desc",
      "field": "`mt_status_desc`.`Remarks` AS `Remarks`",
      "alias": "Remarks",
      "groupBy": false
    }
  ],
  "tables": [
    "mt_status_desc"
  ],
  "joins": [],
  "whereConditions": [
    "`mt_status_desc`.`FOR_TABLE` = 'Pstatus'"
  ],
  "parser": "sqlsplit"
}
```

---

---


### Test Case 7: mv_ordervalue

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `mv_ordervalue` AS select `mt_item`.`Details_OrderID` AS `Details_OrderID`,sum(`mt_item`.`iQty`) AS `OrderQty`,sum(`mt_item`.`iPrice`) AS `TotalPrice` from `mt_item` where `mt_item`.`iDeleted` < 1 group by `mt_item`.`Details_OrderID`
```

#### Extracted SELECT SQL:
```sql
select `mt_item`.`Details_OrderID` AS `Details_OrderID`,sum(`mt_item`.`iQty`) AS `OrderQty`,sum(`mt_item`.`iPrice`) AS `TotalPrice` from `mt_item` where `mt_item`.`iDeleted` < 1 group by `mt_item`.`Details_OrderID`
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "mt_item",
      "field": "`mt_item`.`Details_OrderID` AS `Details_OrderID`",
      "alias": "Details_OrderID",
      "groupBy": true
    },
    {
      "table": "mt_item",
      "field": "SUM(`mt_item`.`iQty`) AS `OrderQty`",
      "alias": "OrderQty",
      "groupBy": false
    },
    {
      "table": "mt_item",
      "field": "SUM(`mt_item`.`iPrice`) AS `TotalPrice`",
      "alias": "TotalPrice",
      "groupBy": false
    }
  ],
  "tables": [
    "mt_item"
  ],
  "joins": [],
  "whereConditions": [
    "`mt_item`.`iDeleted` < 1"
  ],
  "parser": "sqlsplit"
}
```

---

---


### Test Case 8: mv_schedule

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `mv_schedule` AS select `a`.`s_id` AS `s_id`,`a`.`s_text` AS `s_text`,`a`.`sdeleted` AS `sdeleted`,`a`.`screatedate` AS `screatedate`,`a`.`supdate` AS `supdate`,`b`.`wd_id` AS `wd_id`,`b`.`wd_sid` AS `wd_sid`,`b`.`wd_weekday` AS `wd_weekday` from (`mt_schedule` `a` join `mt_weekdays` `b` on(`a`.`s_id` = `b`.`wd_sid`))
```

#### Extracted SELECT SQL:
```sql
select `a`.`s_id` AS `s_id`,`a`.`s_text` AS `s_text`,`a`.`sdeleted` AS `sdeleted`,`a`.`screatedate` AS `screatedate`,`a`.`supdate` AS `supdate`,`b`.`wd_id` AS `wd_id`,`b`.`wd_sid` AS `wd_sid`,`b`.`wd_weekday` AS `wd_weekday` from (`mt_schedule` `a` join `mt_weekdays` `b` on(`a`.`s_id` = `b`.`wd_sid`))
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "mt_schedule",
      "field": "`a`.`s_id` AS `s_id`",
      "alias": "s_id",
      "groupBy": false
    },
    {
      "table": "mt_schedule",
      "field": "`a`.`s_text` AS `s_text`",
      "alias": "s_text",
      "groupBy": false
    },
    {
      "table": "mt_schedule",
      "field": "`a`.`sdeleted` AS `sdeleted`",
      "alias": "sdeleted",
      "groupBy": false
    },
    {
      "table": "mt_schedule",
      "field": "`a`.`screatedate` AS `screatedate`",
      "alias": "screatedate",
      "groupBy": false
    },
    {
      "table": "mt_schedule",
      "field": "`a`.`supdate` AS `supdate`",
      "alias": "supdate",
      "groupBy": false
    },
    {
      "table": "mt_weekdays",
      "field": "`b`.`wd_id` AS `wd_id`",
      "alias": "wd_id",
      "groupBy": false
    },
    {
      "table": "mt_weekdays",
      "field": "`b`.`wd_sid` AS `wd_sid`",
      "alias": "wd_sid",
      "groupBy": false
    },
    {
      "table": "mt_weekdays",
      "field": "`b`.`wd_weekday` AS `wd_weekday`",
      "alias": "wd_weekday",
      "groupBy": false
    }
  ],
  "tables": [
    "mt_schedule",
    "mt_weekdays"
  ],
  "joins": [
    {
      "type": "INNER",
      "leftTable": "mt_schedule",
      "leftField": "s_id",
      "rightTable": "mt_weekdays",
      "rightField": "wd_sid",
      "condition": "(`a`.`s_id` = `b`.`wd_sid`)"
    }
  ],
  "whereConditions": [],
  "parser": "sqlsplit"
}
```

---

---


### Test Case 9: mv_tracking

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `mv_tracking` AS select `mt_tracking`.`trackID` AS `trackID`,`mt_tracking`.`tDesc` AS `tDesc`,`mt_tracking`.`tStatus` AS `tStatus`,`mt_tracking`.`tiType` AS `tiType`,`mt_tracking`.`tCreateDate` AS `tCreateDate`,`mt_tracking`.`trackingNo` AS `trackingNo`,`mt_tracking`.`trackingCost` AS `trackingCost`,`mt_tracking`.`tEditBy` AS `tEditBy`,`mt_tracking`.`tRemarks` AS `tRemarks`,`mt_tracking`.`tDelete` AS `tDelete`,`mt_tracking`.`uid` AS `uid`,`mt_tracking`.`tLastupdate` AS `tLastupdate`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from ((`mt_tracking` left join `mv_item_status_desc` on(`mt_tracking`.`tiType` = `mv_item_status_desc`.`Item_Type` and `mt_tracking`.`tStatus` = `mv_item_status_desc`.`DESC_CODE`)) left join `mv_item_type_desc` on(`mt_tracking`.`tiType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_tracking`.`tDelete` = 0
```

#### Extracted SELECT SQL:
```sql
select `mt_tracking`.`trackID` AS `trackID`,`mt_tracking`.`tDesc` AS `tDesc`,`mt_tracking`.`tStatus` AS `tStatus`,`mt_tracking`.`tiType` AS `tiType`,`mt_tracking`.`tCreateDate` AS `tCreateDate`,`mt_tracking`.`trackingNo` AS `trackingNo`,`mt_tracking`.`trackingCost` AS `trackingCost`,`mt_tracking`.`tEditBy` AS `tEditBy`,`mt_tracking`.`tRemarks` AS `tRemarks`,`mt_tracking`.`tDelete` AS `tDelete`,`mt_tracking`.`uid` AS `uid`,`mt_tracking`.`tLastupdate` AS `tLastupdate`,`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`,`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`,if(`mv_item_status_desc`.`Remarks` = 'finish',1,0) AS `finish` from ((`mt_tracking` left join `mv_item_status_desc` on(`mt_tracking`.`tiType` = `mv_item_status_desc`.`Item_Type` and `mt_tracking`.`tStatus` = `mv_item_status_desc`.`DESC_CODE`)) left join `mv_item_type_desc` on(`mt_tracking`.`tiType` = `mv_item_type_desc`.`DESC_CODE`)) where `mt_tracking`.`tDelete` = 0
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`trackID` AS `trackID`",
      "alias": "trackID",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`tDesc` AS `tDesc`",
      "alias": "tDesc",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`tStatus` AS `tStatus`",
      "alias": "tStatus",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`tiType` AS `tiType`",
      "alias": "tiType",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`tCreateDate` AS `tCreateDate`",
      "alias": "tCreateDate",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`trackingNo` AS `trackingNo`",
      "alias": "trackingNo",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`trackingCost` AS `trackingCost`",
      "alias": "trackingCost",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`tEditBy` AS `tEditBy`",
      "alias": "tEditBy",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`tRemarks` AS `tRemarks`",
      "alias": "tRemarks",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`tDelete` AS `tDelete`",
      "alias": "tDelete",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`uid` AS `uid`",
      "alias": "uid",
      "groupBy": false
    },
    {
      "table": "mt_tracking",
      "field": "`mt_tracking`.`tLastupdate` AS `tLastupdate`",
      "alias": "tLastupdate",
      "groupBy": false
    },
    {
      "table": "mv_item_type_desc",
      "field": "`mv_item_type_desc`.`DESC_NAME` AS `Type_Name`",
      "alias": "Type_Name",
      "groupBy": false
    },
    {
      "table": "mv_item_status_desc",
      "field": "`mv_item_status_desc`.`DESC_NAME` AS `Status_NAME`",
      "alias": "Status_NAME",
      "groupBy": false
    },
    {
      "table": "mv_item_status_desc",
      "field": "IF(`mv_item_status_desc`.`Remarks` = 'finish', 1, 0) AS `finish`",
      "alias": "finish",
      "groupBy": false
    }
  ],
  "tables": [
    "mt_tracking",
    "mv_item_type_desc",
    "mv_item_status_desc"
  ],
  "joins": [
    {
      "type": "LEFT",
      "leftTable": "mt_tracking",
      "leftField": "tiType",
      "rightTable": "mv_item_status_desc",
      "rightField": "Item_Type",
      "condition": "(`mt_tracking`.`tiType` = `mv_item_status_desc`.`Item_Type` AND `mt_tracking`.`tStatus` = `mv_item_status_desc`.`DESC_CODE`)"
    },
    {
      "type": "LEFT",
      "leftTable": "mt_tracking",
      "leftField": "tiType",
      "rightTable": "mv_item_type_desc",
      "rightField": "DESC_CODE",
      "condition": "(`mt_tracking`.`tiType` = `mv_item_type_desc`.`DESC_CODE`)"
    }
  ],
  "whereConditions": [
    "`mt_tracking`.`tDelete` = 0"
  ],
  "parser": "sqlsplit"
}
```

---

---


### Test Case 10: v_cost

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `v_cost` AS select date_format(`t_cost`.`c_time`,'%Y-%m') AS `c_month`,date_format(`t_cost`.`c_time`,'%Y-%m-%d %a') AS `c_date`,`t_cost`.`ID` AS `ID`,`t_cost`.`category` AS `category`,`mt_cost_category`.`cat_desc` AS `cat_desc`,`t_cost`.`c_desc` AS `c_desc`,`t_cost`.`c_price` AS `c_price`,`t_cost`.`c_time` AS `c_time`,`t_cost`.`edit_time` AS `edit_time` from (`t_cost` left join `mt_cost_category` on(`t_cost`.`category` = `mt_cost_category`.`cat_id`))
```

#### Extracted SELECT SQL:
```sql
select date_format(`t_cost`.`c_time`,'%Y-%m') AS `c_month`,date_format(`t_cost`.`c_time`,'%Y-%m-%d %a') AS `c_date`,`t_cost`.`ID` AS `ID`,`t_cost`.`category` AS `category`,`mt_cost_category`.`cat_desc` AS `cat_desc`,`t_cost`.`c_desc` AS `c_desc`,`t_cost`.`c_price` AS `c_price`,`t_cost`.`c_time` AS `c_time`,`t_cost`.`edit_time` AS `edit_time` from (`t_cost` left join `mt_cost_category` on(`t_cost`.`category` = `mt_cost_category`.`cat_id`))
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "t_cost",
      "field": "date_format(`t_cost`.`c_time`, '%Y-%m') AS `c_month`",
      "alias": "c_month",
      "groupBy": false
    },
    {
      "table": "t_cost",
      "field": "date_format(`t_cost`.`c_time`, '%Y-%m-%d %a') AS `c_date`",
      "alias": "c_date",
      "groupBy": false
    },
    {
      "table": "t_cost",
      "field": "`t_cost`.`ID` AS `ID`",
      "alias": "ID",
      "groupBy": false
    },
    {
      "table": "t_cost",
      "field": "`t_cost`.`category` AS `category`",
      "alias": "category",
      "groupBy": false
    },
    {
      "table": "mt_cost_category",
      "field": "`mt_cost_category`.`cat_desc` AS `cat_desc`",
      "alias": "cat_desc",
      "groupBy": false
    },
    {
      "table": "t_cost",
      "field": "`t_cost`.`c_desc` AS `c_desc`",
      "alias": "c_desc",
      "groupBy": false
    },
    {
      "table": "t_cost",
      "field": "`t_cost`.`c_price` AS `c_price`",
      "alias": "c_price",
      "groupBy": false
    },
    {
      "table": "t_cost",
      "field": "`t_cost`.`c_time` AS `c_time`",
      "alias": "c_time",
      "groupBy": false
    },
    {
      "table": "t_cost",
      "field": "`t_cost`.`edit_time` AS `edit_time`",
      "alias": "edit_time",
      "groupBy": false
    }
  ],
  "tables": [
    "t_cost",
    "mt_cost_category"
  ],
  "joins": [
    {
      "type": "LEFT",
      "leftTable": "t_cost",
      "leftField": "category",
      "rightTable": "mt_cost_category",
      "rightField": "cat_id",
      "condition": "(`t_cost`.`category` = `mt_cost_category`.`cat_id`)"
    }
  ],
  "whereConditions": [],
  "parser": "sqlsplit"
}
```

---

---


### Test Case 11: v_game

#### Original CREATE VIEW SQL:
```sql
CREATE ALGORITHM=UNDEFINED DEFINER=`alexk`@`%` SQL SECURITY DEFINER VIEW `v_game` AS select `mt_game_header`.`id_game` AS `id_game`,`mt_game_header`.`Create_datetime` AS `Create_datetime`,`mt_game_header`.`Created_by` AS `Created_by`,`mt_game_header`.`title` AS `title`,`mt_game_header`.`option_i` AS `option_i`,`mt_game_header`.`option_vs` AS `option_vs`,`mt_game_details`.`id_gameDetails` AS `id_gameDetails`,`mt_game_details`.`d_Create_datetime` AS `d_Create_datetime`,`mt_game_details`.`d_Created_by` AS `d_Created_by`,`mt_game_details`.`selected` AS `selected`,`mt_game_link`.`id_link` AS `id_link` from ((`mt_game_header` join `mt_game_link` on(`mt_game_header`.`id_game` = `mt_game_link`.`id_game`)) join `mt_game_details` on(`mt_game_link`.`id_gameDetails` = `mt_game_details`.`id_gameDetails`))
```

#### Extracted SELECT SQL:
```sql
select `mt_game_header`.`id_game` AS `id_game`,`mt_game_header`.`Create_datetime` AS `Create_datetime`,`mt_game_header`.`Created_by` AS `Created_by`,`mt_game_header`.`title` AS `title`,`mt_game_header`.`option_i` AS `option_i`,`mt_game_header`.`option_vs` AS `option_vs`,`mt_game_details`.`id_gameDetails` AS `id_gameDetails`,`mt_game_details`.`d_Create_datetime` AS `d_Create_datetime`,`mt_game_details`.`d_Created_by` AS `d_Created_by`,`mt_game_details`.`selected` AS `selected`,`mt_game_link`.`id_link` AS `id_link` from ((`mt_game_header` join `mt_game_link` on(`mt_game_header`.`id_game` = `mt_game_link`.`id_game`)) join `mt_game_details` on(`mt_game_link`.`id_gameDetails` = `mt_game_details`.`id_gameDetails`))
```

#### Expected Backend Output:
```json
{
  "success": true,
  "fields": [
    {
      "table": "mt_game_header",
      "field": "`mt_game_header`.`id_game` AS `id_game`",
      "alias": "id_game",
      "groupBy": false
    },
    {
      "table": "mt_game_header",
      "field": "`mt_game_header`.`Create_datetime` AS `Create_datetime`",
      "alias": "Create_datetime",
      "groupBy": false
    },
    {
      "table": "mt_game_header",
      "field": "`mt_game_header`.`Created_by` AS `Created_by`",
      "alias": "Created_by",
      "groupBy": false
    },
    {
      "table": "mt_game_header",
      "field": "`mt_game_header`.`title` AS `title`",
      "alias": "title",
      "groupBy": false
    },
    {
      "table": "mt_game_header",
      "field": "`mt_game_header`.`option_i` AS `option_i`",
      "alias": "option_i",
      "groupBy": false
    },
    {
      "table": "mt_game_header",
      "field": "`mt_game_header`.`option_vs` AS `option_vs`",
      "alias": "option_vs",
      "groupBy": false
    },
    {
      "table": "mt_game_details",
      "field": "`mt_game_details`.`id_gameDetails` AS `id_gameDetails`",
      "alias": "id_gameDetails",
      "groupBy": false
    },
    {
      "table": "mt_game_details",
      "field": "`mt_game_details`.`d_Create_datetime` AS `d_Create_datetime`",
      "alias": "d_Create_datetime",
      "groupBy": false
    },
    {
      "table": "mt_game_details",
      "field": "`mt_game_details`.`d_Created_by` AS `d_Created_by`",
      "alias": "d_Created_by",
      "groupBy": false
    },
    {
      "table": "mt_game_details",
      "field": "`mt_game_details`.`selected` AS `selected`",
      "alias": "selected",
      "groupBy": false
    },
    {
      "table": "mt_game_link",
      "field": "`mt_game_link`.`id_link` AS `id_link`",
      "alias": "id_link",
      "groupBy": false
    }
  ],
  "tables": [
    "mt_game_header",
    "mt_game_link",
    "mt_game_details"
  ],
  "joins": [
    {
      "type": "INNER",
      "leftTable": "mt_game_header",
      "leftField": "id_game",
      "rightTable": "mt_game_link",
      "rightField": "id_game",
      "condition": "(`mt_game_header`.`id_game` = `mt_game_link`.`id_game`)"
    },
    {
      "type": "INNER",
      "leftTable": "mt_game_link",
      "leftField": "id_gameDetails",
      "rightTable": "mt_game_details",
      "rightField": "id_gameDetails",
      "condition": "(`mt_game_link`.`id_gameDetails` = `mt_game_details`.`id_gameDetails`)"
    }
  ],
  "whereConditions": [],
  "parser": "sqlsplit"
}
```

---

---


## Validation Checklist

請確認以下各項目都能正確解析：

- [ ] **基本 SELECT:** 簡單的欄位選擇與別名
- [ ] **JOIN 語法:** INNER JOIN, LEFT JOIN 等複雜連接
- [ ] **WHERE 條件:** 複雜邏輯條件與運算符
- [ ] **GROUP BY:** 分組語法與聚合函數
- [ ] **ORDER BY:** 排序語法
- [ ] **MySQL 函數:** IF, date_format, CONCAT 等
- [ ] **子查詢:** 巢狀 SELECT（如有）
- [ ] **別名處理:** 表格與欄位別名正確識別
- [ ] **中文處理:** UTF-8 字元支援
- [ ] **錯誤處理:** 無效 SQL 的錯誤回傳
- [ ] **引號格式:** MySQL 反引號 (`) 正確處理
- [ ] **複雜表達式:** 函數調用與運算式解析

## Notes

- 此測試資料基於實際生產環境的 view 定義
- 所有預期輸出都經過現有 parser 驗證
- 新模組需完全相容現有輸出格式
- 測試通過率應達到 95% 以上
- 共包含 11 個真實 view 的測試案例