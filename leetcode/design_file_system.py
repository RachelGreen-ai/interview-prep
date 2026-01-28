# LeetCode 1166: Design File System
#%%
"""
Problem Statement:
Implement a FileSystem class:

- createPath(path: str, value: int) -> bool
  Create a new path and associate it with value.
  Return False if:
    - the path already exists, OR
    - the parent path does not exist.
  Otherwise return True.

- get(path: str) -> int
  Return the value associated with path, or -1 if the path does not exist.

Notes:
- Paths look like "/a", "/leet/code" (components separated by '/')
- "/" by itself is not a valid path to create or get (per LC prompt)

INTERVIEW EXPLANATION (brief):

- **Hash map is enough**: We only need exact path existence + parent existence checks.
  No need for prefix queries, listing directories, etc.
- **Key trick**: For createPath("/a/b", v), parent is "/a".
  - If parent doesn't exist → fail
  - If "/a/b" already exists → fail
  - Else insert into map

Complexity:
- Time: O(L) per operation where L = length of path (due to slicing)
- Space: O(N) for stored paths
"""

from __future__ import annotations


class FileSystem:
    def __init__(self):
        # Store created paths. Root is treated as existing to allow creating "/a".
        self._paths: dict[str, int] = {"/": -1}

    def createPath(self, path: str, value: int) -> bool:
        if not path or path == "/" or path in self._paths:
            return False

        # Parent is everything before the last "/" (except root).
        parent = path.rsplit("/", 1)[0]
        if parent == "":
            parent = "/"

        if parent not in self._paths:
            return False

        self._paths[path] = value
        return True

    def get(self, path: str) -> int:
        if not path or path == "/":
            return -1
        return self._paths.get(path, -1)


def test_design_file_system():
    # Example 1
    fs = FileSystem()
    assert fs.createPath("/a", 1) is True
    assert fs.get("/a") == 1

    # Example 2
    fs = FileSystem()
    assert fs.createPath("/leet", 1) is True
    assert fs.createPath("/leet/code", 2) is True
    assert fs.get("/leet/code") == 2
    assert fs.createPath("/c/d", 1) is False
    assert fs.get("/c") == -1

    # Edge cases
    fs = FileSystem()
    assert fs.get("/nope") == -1
    assert fs.createPath("/", 123) is False
    assert fs.get("/") == -1
    assert fs.createPath("/a", 1) is True
    assert fs.createPath("/a", 2) is False  # already exists
    assert fs.createPath("/a/b", 3) is True
    assert fs.get("/a/b") == 3

    print("All tests passed!")


if __name__ == "__main__":
    test_design_file_system()
# %%

