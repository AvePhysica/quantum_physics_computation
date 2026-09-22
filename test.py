"""检查 Python 脚本能否运行，以及常用第三方库是否已安装。"""

import importlib.util
import sys


LIBRARIES = (
    ("numpy", "NumPy"),
    ("scipy", "SciPy"),
    ("pandas", "Pandas"),
    ("matplotlib", "Matplotlib"),
    ("sympy", "SymPy"),
    ("requests", "Requests"),
    ("qiskit", "Qiskit"),
    ("qutip", "QuTiP"),
)


def main() -> None:
    print("Python 脚本运行成功！")
    print(f"Python 版本：{sys.version.split()[0]}")
    print(f"解释器路径：{sys.executable}")
    print("\n常用库安装情况：")

    for module_name, display_name in LIBRARIES:
        installed = importlib.util.find_spec(module_name) is not None
        status = "已安装" if installed else "未安装"
        print(f"- {display_name} ({module_name})：{status}")


if __name__ == "__main__":
    main()
