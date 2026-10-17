
import json
from pathlib import Path

from parser.python_parser import parse_python_file


def analyze_repository(repo_path: Path) -> dict:
    ignored_dirs = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "dist",
        "build",
    }

    python_files = []

    for file_path in repo_path.rglob("*.py"):
        relative_path = file_path.relative_to(repo_path)

        if any(part in ignored_dirs for part in relative_path.parts):
            continue

        python_files.append(file_path)

    python_files.sort()

    results = []
    failed_files = []

    for file_path in python_files:
        try:
            result = parse_python_file(file_path)
            result["file"] = file_path.relative_to(repo_path).as_posix()
            results.append(result)

            if result["error"]:
                failed_files.append(result["file"])

        except (OSError, UnicodeError) as error:
            failed_files.append(str(file_path))
            print(f"Could not read {file_path}: {error}")

    total_functions = sum(
        len(result["functions"]) for result in results
    )

    total_classes = sum(
        len(result["classes"]) for result in results
    )

    report = {
        "repository": repo_path.name,
        "total_python_files": len(python_files),
        "successfully_parsed_files": len(results) - sum(
            1 for result in results if result["error"]
        ),
        "failed_files": failed_files,
        "total_functions": total_functions,
        "total_classes": total_classes,
        "files": results,
    }

    output_path = repo_path / "neurocode_analysis.json"
    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print("\n========== Repository Analysis ==========")
    print(f"Repository: {report['repository']}")
    print(f"Python files discovered: {report['total_python_files']}")
    print(f"Successfully parsed: {report['successfully_parsed_files']}")
    print(f"Files with errors: {len(failed_files)}")
    print(f"Functions discovered: {total_functions}")
    print(f"Classes discovered: {total_classes}")
    print(f"Report saved to: {output_path}")

    return report
