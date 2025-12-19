import json
import os
from pprint import pprint

from tqdm import tqdm

from pta_class import pta


def compiler_to_codetype(compiler: str) -> str:
    compiler = compiler.lower()
    if compiler in {"gcc", "clang"}:
        return "c"
    if compiler in {"g++", "clang++"}:
        return "cpp"
    if compiler in {"java", "javac"}:
        return "java"
    if compiler == "python3":
        return "python3"
    return compiler


def sanitize_folder_name(folder_name: str) -> str:
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


def create_folder(base: str, folder_name: str) -> str:
    sanitized_name = sanitize_folder_name(folder_name)
    path = os.path.join(base, sanitized_name)
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"文件夹 '{sanitized_name}' 创建成功！")
    return path


def prompt_credentials():
    try:
        from password import email, password  # type: ignore
    except ImportError:
        email = ""
        password = ""
    if email == "":
        email = input("请输入邮箱:")
    if password == "":
        password = input("请输入密码:")
    return email, password


def select_problem_set(client: pta):
    if not client.problem_sets:
        raise RuntimeError("尚未加载题目集")
    pprint({i: client.problem_sets[i].name for i in range(len(client.problem_sets))})
    while True:
        choice = input("请输入题目集的序号: ").strip()
        if choice.isdigit() and 0 <= int(choice) < len(client.problem_sets):
            return client.problem_sets[int(choice)]
        print("输入不合法，请重新输入。")


def _extract_program_text(submission) -> str:
    if not submission.submissionDetails:
        return ""
    detail = submission.submissionDetails[0]
    if detail.codeCompletionSubmissionDetail.program:
        return detail.codeCompletionSubmissionDetail.program
    return detail.programmingSubmissionDetail.program


def gather_problem_data(client: pta, problem) -> None:
    client.get_exam(problem)
    client.get_problem_list(problem)

    label_ids = list(client.problems_list[problem.id].examLabelByProblemSetProblemId)
    for label_id in tqdm(label_ids, desc="获取提交列表"):
        client.get_submission_list(problem, client.exam_info[problem.id], label_id)

    submissions = [
        s for all_subs in client.submission_list.values() for s in all_subs.values()
    ]
    for submission in tqdm(submissions, desc="获取提交详情"):
        client.get_submission_info(submission)

    labels = client.problems_list[problem.id].labels
    for label in tqdm(labels, desc="获取题目描述"):
        client.get_problem_description(problem.id, label)


def export_problem(client: pta, problem) -> None:
    base_path = create_folder("output", problem.name)
    json_dir = create_folder(base_path, "json")
    code_dir = create_folder(base_path, "code")

    problem_types = client.problems_list[problem.id]
    label_by_id = {label.id: label for label in problem_types.labels}
    data = {"title": problem.name, "id": problem.id, "content": []}

    for problem_id, submissions in client.submission_list.items():
        label = label_by_id.get(problem_id)
        if not label:
            continue

        accepted = next(
            (s for s in submissions.values() if s.status == "ACCEPTED"), None
        )
        if not accepted:
            continue

        program_text = _extract_program_text(accepted)
        if not program_text:
            continue

        datatmp = {
            "title": label.title,
            "id": label.id,
            "proid": problem_types.examLabelByProblemSetProblemId.get(label.id, ""),
        }

        with open(
            os.path.join(json_dir, f"{label.id}.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(accepted.to_dict(), f, ensure_ascii=False, indent=4)

        with open(
            os.path.join(code_dir, f"{label.id}.code.md"), "w", encoding="utf-8"
        ) as f:
            f.write(f"```{compiler_to_codetype(accepted.compiler)}\n")
            f.write(program_text)
            f.write("\n```\n")

        with open(
            os.path.join(code_dir, f"{label.id}.cont.md"), "w", encoding="utf-8"
        ) as f:
            f.write(f"# {datatmp['title']}\n")
            f.write(f"{label.content}\n")

        data["content"].append(datatmp)

    with open(os.path.join(base_path, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(email: str = "", password: str = ""):
    client = pta(email, password)
    try:
        if not client.login():
            print("登录失败")
            return False
        print("登录成功")

        client.get_problems()
        problem = select_problem_set(client)
        gather_problem_data(client, problem)
        export_problem(client, problem)
        client.save_cookies()
        return True
    finally:
        client.close()


if __name__ == "__main__":
    email, password = prompt_credentials()
    main(email, password)
