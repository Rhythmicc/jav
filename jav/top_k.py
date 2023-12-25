from . import *
from . import _ask


def top_k():
    return requirePackage(
        ".top.{}".format(
            _ask(
                {
                    "type": "list",
                    "message": "请选择站点",
                    "choices": ["javtxt", "jable", "javdb"],
                    "default": "javdb",
                }
            )
        ),
        "get_top",
    )()
