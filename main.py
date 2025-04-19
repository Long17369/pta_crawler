from pta_class import pta
from pprint import pprint
from tqdm import tqdm

import json
import os


def compiler_to_codetype(compiler):
    compiler = compiler.lower()
    if compiler == "gcc" or compiler == "clang":
        return "c"
    elif compiler == "g++" or compiler == "clang++":
        return "cpp"
    elif compiler == "java":
        return "java"
    elif compiler == "python3":
        return "python3"


def sanitize_folder_name(folder_name):
    illegal_chars = {
        "\\": "、",
        "/": "、",
        ":": "：",
        "*": "·",
        "?": "？",
        '"': "“",
        "<": "《",
        ">": "》",
        "|": "丨",
    }
    for char, replacement in illegal_chars.items():
        folder_name = folder_name.replace(char, replacement)
    return folder_name


def create_folder(path, folder_name):
    sanitized_name = sanitize_folder_name(folder_name)
    if not os.path.exists(path + sanitized_name):
        os.makedirs(path + sanitized_name)
        print(f"文件夹 '{sanitized_name}' 创建成功！")


def main(email: str = "", password: str = ""):
    p = pta(email, password)
    if not p.login():
        print("登录失败")
        return False
    print("登录成功")
    p.get_problems()
    pprint({i: p.problem_sets[i].name for i in range(len(p.problem_sets))})
    print("请输入题目集的序号")
    index = int(input())
    problem = p.problem_sets[index]
    p.get_exam(problem)
    p.get_problem_list(problem)
    for i in tqdm(p.problems_list[problem.id].examLabelByProblemSetProblemId):
        p.get_submission_list(problem, p.exam_info[problem.id], i)
    for i in tqdm([j for i in p.submission_list.values() for j in i.values()]):
        p.get_submission_info(i)
    with open("data2.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                k: {k2: v2.to_dict() for k2, v2 in v.items()}
                for k, v in p.submission_list.items()
            },
            f,
            ensure_ascii=False,
            indent=4,
        )
    create_folder("output/", problem.name)
    create_folder("output/" + problem.name + "/", "json")
    create_folder("output/" + problem.name + "/", "code")
    p.save_cookies()
    data = {"title": problem.name, "id": problem.id, "content": []}
    for idx, i in zip(range(len(p.submission_list)), p.submission_list.values()):
        for v in i.values():
            if v.status == "ACCEPTED":
                pid = p.problems_list[problem.id].labels[idx].id
                datatmp = {
                    "title": p.problems_list[problem.id].labels[idx].title,
                    "id": pid,
                    "proid": p.problems_list[problem.id].examLabelByProblemSetProblemId[
                        pid
                    ],
                }
                # 写入提交元数据
                with open(
                    f"output/{problem.name}/json/{pid}.json",
                    "w",
                    encoding="utf-8",
                ) as f:
                    json.dump(v.to_dict(), f, ensure_ascii=False, indent=4)
                # 写入源代码
                with open(
                    f"output/{problem.name}/code/{pid}.code.md",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(f"```{compiler_to_codetype(v.compiler)}\n")
                    if (
                        v.submissionDetails[0].codeCompletionSubmissionDetail.program
                        == ""
                    ):
                        f.write(
                            v.submissionDetails[0].programmingSubmissionDetail.program
                        )
                    else:
                        f.write(
                            v.submissionDetails[
                                0
                            ].codeCompletionSubmissionDetail.program
                        )
                    f.write("\n```\n")
                # 写入题目
                with open(
                    f"output/{problem.name}/code/{pid}.cont.md", "w", encoding="utf-8"
                ) as f:
                    f.write(f"# {datatmp['title']}\n")
                    # todo: 写入具体问题
                data["content"].append(datatmp)
                break
    with open(f"output/{problem.name}/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    email = input("请输入邮箱:")
    password = input("请输入密码:")
    a = main(email, password)
    pprint(eval(str(a)))
