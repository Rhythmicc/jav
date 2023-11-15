const completionSpec: Fig.Spec = {
    "name": "jav",
    "description": "jav",
    "subcommands": [
        {
            "name": "complete",
            "description": "获取补全列表",
            "args": [],
            "options": [
                {
                    "name": "--team",
                    "description": "团队名",
                    "isOptional": true,
                    "args": {
                        "name": "team",
                        "description": "团队名"
                    }
                },
                {
                    "name": "--token",
                    "description": "团队token",
                    "isOptional": true,
                    "args": {
                        "name": "token",
                        "description": "团队token"
                    }
                },
                {
                    "name": "--is-script",
                    "description": "是否为脚本"
                }
            ]
        },
        {
            "name": "cover",
            "description": "下载所有的封面",
            "args": [],
            "options": []
        },
        {
            "name": "info",
            "description": "查询番号信息和链接",
            "args": [
                {
                    "name": "designation",
                    "description": "番号"
                }
            ],
            "options": []
        },
        {
            "name": "web",
            "description": "通过浏览器获取番号信息",
            "args": [
                {
                    "name": "designation",
                    "description": "番号"
                }
            ],
            "options": []
        },
        {
            "name": "rank",
            "description": "查看近期榜单",
            "args": [],
            "options": [
                {
                    "name": "--enable-translate",
                    "description": "是否翻译"
                }
            ]
        },
        {
            "name": "wish",
            "description": "心愿单",
            "args": [],
            "options": []
        },
        {
            "name": "top15",
            "description": "查看近期榜单",
            "args": [],
            "options": []
        },
        {
            "name": "update",
            "description": "更新jav工具",
            "args": [],
            "options": []
        }
    ]
};
export default completionSpec;
