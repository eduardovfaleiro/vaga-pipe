from services.matcher import _score_job


def test_score_high_match():
    score = _score_job(
        ["python", "fastapi"],
        "Python Developer with FastAPI",
        "Build REST APIs using Python and FastAPI framework",
    )
    assert score >= 70


def test_score_zero_match():
    score = _score_job(
        ["cobol"],
        "React Frontend Engineer",
        "Build modern UIs with React and TypeScript",
    )
    assert score == 0.0


def test_score_empty_skills():
    score = _score_job([], "Python Developer", "Python and Django backend")
    assert score == 0.0


def test_score_partial_match():
    # "python" dá match, "java" não dá match contra título/descrição com só Python
    score = _score_job(
        ["python", "java"],
        "Python Developer",
        "Python backend developer position",
    )
    # 1 de 2 skills com match = 50%
    assert score == 50.0
