import os
import subprocess
import sys


def pytest_sessionstart(session):
    print('Building C extension before testing...')

    project_root = os.path.abspath(os.path.join(__file__, "..", ".."))

    # Run: python -m build --wheel --no-isolation
    subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--no-isolation"],
        cwd=project_root,
        check=True
    )

    # Install the wheel into the current environment
    dist_dir = os.path.join(project_root, "dist")
    wheels = [f for f in os.listdir(dist_dir) if f.endswith(".whl")]
    if wheels:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--force-reinstall", os.path.join(dist_dir, wheels[-1])],
            check=True
        )
