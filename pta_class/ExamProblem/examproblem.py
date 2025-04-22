




a = {
    "problemSetProblem": {
        "id": "1912711373419077632",
        "label": "6-1",
        "score": 10,
        "problemConfig": {
            "codeCompletionProblemConfig": {
                "timeLimit": 400,
                "memoryLimit": 65536,
                "codeSizeLimit": 16,
                "cases": {
                    "0": {
                        "hint": "",
                        "showHint": False,
                        "score": 7,
                        "isPublic": False
                    },
                    "1": {
                        "hint": "",
                        "showHint": False,
                        "score": 1,
                        "isPublic": False
                    },
                    "2": {
                        "hint": "",
                        "showHint": False,
                        "score": 1,
                        "isPublic": False
                    },
                    "3": {
                        "hint": "",
                        "showHint": False,
                        "score": 1,
                        "isPublic": False
                    }
                },
                "exampleTestDatas": [
                    {
                        "name": "",
                        "input": "abcdef\n",
                        "output": "defabc"
                    },
                    {
                        "name": "",
                        "input": "abcdef\n",
                        "output": "defabc"
                    }
                ],
                "testdataDescriptionCode": "",
                "tools": [],
                "ignorePresentationError": False,
                "pathAsStdin": "",
                "pathAsStdout": ""
            },
            "solutionVisible": False,
            "answerVisible": False
        },
        "deadline": "1970-01-01T00:00:00Z",
        "title": "移动字母",
        "content": "本题要求编写函数，将输入字符串的前3个字符移到最后。\n\n### 函数接口定义：\n```c++\nvoid Shift( char s[] );\n```\n其中`char s[]`是用户传入的字符串，题目保证其长度不小于3；函数`Shift`须将按照要求变换后的字符串仍然存在`s[]`里。\n\n### 裁判测试程序样例：\n```c++\n#include <stdio.h>\n#include <string.h>\n\n#define MAXS 10\n\nvoid Shift( char s[] );\n\nvoid GetString( char s[] ); /* 实现细节在此不表 */\n\nint main()\n{\n    char s[MAXS];\n\n    GetString(s);\n    Shift(s);\n    printf(\"%s\\n\", s);\n\t\n    return 0; \n}\n\n/* 你的代码将被嵌在这里 */\n```\n\n### 输入样例：\n```in\nabcdef\n\n```\n\n### 输出样例：\n```out\ndefabc\n```",
        "type": "CODE_COMPLETION",
        "author": "张泳",
        "difficulty": 0,
        "compiler": "GCC",
        "problemStatus": "REVIEWED",
        "lastSubmissionId": "0",
        "solution": "",
        "problemSetId": "1912711373087727616",
        "problemId": "430",
        "description": "本题要求编写函数，将输入字符串的前3个字符移到最后。\n\n### 函数接口定义：\n```c++\nvoid Shift( char s[] );\n```\n其中`char s[]`是用户传入的字符串，题目保证其长度不小于3；函数`Shift`须将按照要求变换后的字符串仍然存在`s[]`里。\n\n### 裁判测试程序样例：\n```c++\n#include <stdio.h>\n#include <string.h>\n\n#define MAXS 10\n\nvoid Shift( char s[] );\n\nvoid GetString( char s[] ); /* 实现细节在此不表 */\n\nint main()\n{\n    char s[MAXS];\n\n    GetString(s);\n    Shift(s);\n    printf(\"%s\\n\", s);\n\t\n    return 0; \n}\n\n/* 你的代码将被嵌在这里 */\n```\n\n### 输入样例：\n```in\nabcdef\n\n```\n\n### 输出样例：\n```out\ndefabc\n```",
        "problemPoolIndex": 1,
        "indexInProblemPool": 1,
        "authorOrganizationId": "2"
    },
    "organization": {
        "id": "2",
        "name": "浙大城市学院",
        "code": "zucc",
        "type": "SCHOOL",
        "logo": "a7a4740b-4fb1-4f54-b79c-6080378d7579.png"
    },
    "examLabel": "6-1"
}