# JavaCodeGenerator
create service of java code with python

# 配置模板

> 使用时在templates文件夹中添加 `param_input.txt` 文件, 将以下内容填入其中 

```
{
    "class": "Test",
    "package": "com.abc.user",
    "daoPackage":"com.abc.user.dao.mysql",
    "entityPackage":"com.abc.user.model.entity",
    "entityDtoPackage":"com.abc.user.model.dto",

    "author":"author",
    "function":"test",

    "column": {
        "updageUserName": "String",
        "activeName": "String",
        "updageUserName": "String",
        "activeName": "String"
    }
}
```