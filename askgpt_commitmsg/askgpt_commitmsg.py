import git


def summarize_diffs(path: str, suffix: str) -> str:
    repo = git.Repo(path)
    index = repo.index
    result = ""
    # Get the staged changes as a text diff
    staged_diff = index.diff(
        "HEAD",
        create_patch=True,
        R=True,
        ignore_blank_lines=True,
        ignore_space_at_eol=True,
    )
    change_types = {
        "A": "Added",
        "M": "Modified",
        "D": "Deleted",
        "R": "Removed",
        "T": "Transferred",
    }
    for change_type in change_types.keys():
        diffs = list(staged_diff.iter_change_type(change_type))
        if len(diffs) > 0:
            result += f"{change_types[change_type]} files:\n"
            for diff in diffs:
                filetype = get_filetype_from_path(diff.b_path)
                if filetype == suffix:
                    if change_type == "M":
                        result += f"{diff.b_path}:\n {diff.diff.decode('utf-8')}\n"
                    else:
                        result += f"{diff.b_path}\n"
    result += "\n"
    return result


def get_filetype_from_path(path: str) -> str:
    return path.split(".")[-1]


def prompt(diff_summary: str) -> str:
    return f"Write the commit message title (fewer than 50 characters) for the git diff: \n\n{diff_summary}; list major changes by the commit, with each line less than 72 characters."
