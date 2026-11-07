import os

def test_project_structure_exists():
    required_dirs = [
        "data/raw", "data/processed", "data/ground_truth",
        "crawler/spiders", "backend/app/engine", "frontend/src",
        "evaluation_results/charts", "docs/report", "docs/screenshots"
    ]
    for d in required_dirs:
        assert os.path.exists(d), f"Directory {d} missing"

    required_files = [
        "docker-compose.yml", "Makefile", ".gitignore",
        "backend/requirements.txt", "backend/Dockerfile",
        "frontend/package.json", "frontend/Dockerfile"
    ]
    for f in required_files:
        assert os.path.isfile(f), f"File {f} missing"
