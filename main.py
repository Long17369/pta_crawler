import json
import os
import hashlib
from typing import Optional, Tuple

from loguru import logger
from tqdm import tqdm

from pta_class.logger import setup_logging
from pta_class import Problems, Submission, pta


def compiler_to_codetype(compiler: str) -> Optional[str]:
    compiler = (compiler or "").lower()
    if compiler in {"gcc", "clang"}:
        return "c"
    if compiler in {"g++", "clang++"}:
        return "cpp"
    if compiler in {"java", "javac"}:
        return "java"
    if compiler in {"python3", "python", "pypy3"}:
        return "python"
    return None


def to_stable_numeric_id(raw_value: str, namespace: str = "") -> str:
    raw = str(raw_value)
    if raw.isdigit():
        return raw
    text = f"{namespace}:{raw}"
    num = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % (10**16)
    return str(num).zfill(16)


def load_problem_set_data(path: str) -> dict:
    if not os.path.exists(path):
        return {"type": "problemSet", "title": "", "content": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if (
            isinstance(data, dict)
            and data.get("type") == "problemSet"
            and isinstance(data.get("content"), list)
        ):
            valid_content = []
            for item in data["content"]:
                if (
                    isinstance(item, dict)
                    and isinstance(item.get("id"), str)
                    and item["id"].isdigit()
                    and isinstance(item.get("title"), str)
                ):
                    valid_content.append({"id": item["id"], "title": item["title"]})
            return {
                "type": "problemSet",
                "title": str(data.get("title", "")),
                "content": valid_content,
            }
    except Exception as e:
        logger.warning(f"读取已有题集索引失败，将重建: {path}, err={e}")
    return {"type": "problemSet", "title": "", "content": []}


def upsert_problem_set_entry(
    index_path: str,
    index_title: str,
    child_id: str,
    child_title: str,
) -> None:
    data = load_problem_set_data(index_path)
    data["type"] = "problemSet"
    data["title"] = index_title

    content_by_id = {
        item["id"]: {"id": item["id"], "title": item["title"]}
        for item in data.get("content", [])
        if isinstance(item, dict)
        and isinstance(item.get("id"), str)
        and item["id"].isdigit()
        and isinstance(item.get("title"), str)
    }
    content_by_id[child_id] = {"id": child_id, "title": child_title}
    data["content"] = sorted(content_by_id.values(), key=lambda item: item["id"])

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


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
        logger.info(f"文件夹 '{sanitized_name}' 创建成功！")
    return path


def prompt_credentials() -> Tuple[str, str]:
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


def select_problem_set(client: pta) -> Optional[Problems]:
    if not client.problem_sets:
        raise RuntimeError("尚未加载题目集")
    # 倒序展示，最近的题目集在前；提供退出选项
    indices = list(range(len(client.problem_sets) - 1, -1, -1))
    listing = "\n".join(f"{idx}: {client.problem_sets[idx].name}" for idx in indices)
    logger.info("可选题目集(输入数字选择，q 退出):\n" + listing)
    while True:
        choice = input("请输入题目集的序号: ").strip()
        if choice.lower() in {"q", "quit", "exit"}:
            logger.info("用户选择退出")
            return None
        if choice.isdigit() and 0 <= int(choice) < len(client.problem_sets):
            sel = client.problem_sets[int(choice)]
            logger.info(f"选择题目集: index={choice}, id={sel.id}, name={sel.name}")
            return sel
        print("输入不合法，请重新输入。")


def _extract_program_text(submission: Submission) -> str:
    if not submission.submissionDetails:
        return ""
    detail = submission.submissionDetails[0]
    if detail.codeCompletionSubmissionDetail.program:
        return detail.codeCompletionSubmissionDetail.program
    return detail.programmingSubmissionDetail.program


def gather_problem_data(client: pta, problem: Problems) -> None:
    client.get_exam(problem)
    client.get_problem_list(problem)

    label_ids = list(client.problems_list[problem.id].examLabelByProblemSetProblemId)
    logger.info(f"待抓取题目数量: {len(label_ids)}")
    for label_id in tqdm(label_ids, desc="获取提交列表"):
        client.get_submission_list(problem, client.exam_info[problem.id], label_id)

    submissions = [
        s for all_subs in client.submission_list.values() for s in all_subs.values()
    ]
    logger.info(f"待抓取提交详情数量: {len(submissions)}")
    for submission in tqdm(submissions, desc="获取提交详情"):
        client.get_submission_info(submission)

    labels = client.problems_list[problem.id].labels
    logger.info(f"待抓取题目描述数量: {len(labels)}")
    for label in tqdm(labels, desc="获取题目描述"):
        client.get_problem_description(problem.id, label)


def export_problem(client: pta, problem: Problems) -> None:
    problem_set_id = to_stable_numeric_id(problem.id, "problemSet")
    base_path = create_folder("output", problem_set_id)
    problem_set_data_path = os.path.join(base_path, "data.json")
    root_data_path = os.path.join("output", "data.json")

    upsert_problem_set_entry(
        root_data_path,
        "output",
        problem_set_id,
        problem.name,
    )

    problem_types = client.problems_list[problem.id]
    label_by_id = {label.id: label for label in problem_types.labels}
    data = load_problem_set_data(problem_set_data_path)
    data["type"] = "problemSet"
    data["title"] = problem.name

    content_by_id = {
        item["id"]: {"id": item["id"], "title": item["title"]}
        for item in data.get("content", [])
        if isinstance(item, dict)
        and isinstance(item.get("id"), str)
        and item["id"].isdigit()
        and isinstance(item.get("title"), str)
    }

    for problem_id in sorted(client.submission_list.keys(), key=str):
        submissions = client.submission_list[problem_id]
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

        target_problem_id = to_stable_numeric_id(label.id, problem_set_id)
        problem_dir = create_folder(base_path, target_problem_id)

        source_file = {"code": program_text}
        language = compiler_to_codetype(accepted.compiler)
        if language:
            source_file["language"] = language

        code_data = {
            "type": "problem",
            "title": label.title,
            "content": [source_file],
        }
        if label.description:
            code_data["description"] = label.description
        elif label.content:
            code_data["description"] = label.content

        with open(os.path.join(problem_dir, "data.json"), "w", encoding="utf-8") as f:
            json.dump(code_data, f, ensure_ascii=False, indent=4)

        content_by_id[target_problem_id] = {
            "id": target_problem_id,
            "title": label.title,
        }
        logger.debug(
            f"导出完成: id={target_problem_id}, title={label.title}, compiler={accepted.compiler}"
        )

    data["content"] = sorted(content_by_id.values(), key=lambda item: item["id"])
    with open(problem_set_data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"导出索引文件完成: {problem_set_data_path}")


def main(email: str = "", password: str = "") -> bool:
    with pta(email, password) as client:
        if not client.login():
            logger.error("登录失败")
            return False
        logger.info("登录成功")
        client.save_cookies()

        if not client.get_problems():
            logger.error("获取题库失败，程序结束")
            return False

        problem = select_problem_set(client)
        if problem is None:
            return False
        gather_problem_data(client, problem)
        export_problem(client, problem)
        return True


if __name__ == "__main__":
    setup_logging()
    email, password = prompt_credentials()
    main(email, password)
