const completionSpec: Fig.Spec = {
    "name": "jav",
    "description": "jav",
    "subcommands": [
        {
            "name": "--help",
            "description": "获取帮助"
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
            "args": [
                {
                    "name": "--enable_translate",
                    "description": "是否翻译",
                    "isOptional": true,
                    "args": {
                        "name": "enable_translate",
                        "description": "是否翻译"
                    }
                }
            ],
            "options": []
        }
    ]
};
export default completionSpec;
