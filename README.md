# 接口文档生成工具

### Author: 卢毅飞、张猛、陈韵博

将接口的Request和Response文件转化CityDNA内部文档格式

## 使用说明

<img src="./Instruction Pic.png"/>

请尽量按照如下格式输入

Sample API Blueprint Format:
```http
# POST /pinstreet/promote/egg_edu/api/v1/exchange

+ Request (application/json; charset=utf-8)

    + Headers

            uid: super_YH

    + Body

            {
                "ea_id": "64",
                "exchange_info": "9"
            }

+ Response 400 (application/json)

        {"error_code": 1000,
        "msg": {"exchange_info": ["This field is required."]},
        "request": "POST /pinstreet/promote/egg_edu/api/v1/exchange"}
```

Sample Request/Response Format:
```json
{
    "proposal_list" :[{"id":"146","approve":"1"}]
}
{
    "error_code": 0,
    "msg": "success",
    "request": "POST /pinstreet/bms/api/update_proposal_approve"
}
```

---
#### 7.24 更新
* 添加了原先一个JSON生成Markdown表格的功能
* 左面第二行的两个Textfield都是原先这个功能的两个额外参数域，用逗号分隔
* 只在输入单独1个JSON object的时候有效。输入API Blueprint或者两个(Request/reponse)JSON的时候无效