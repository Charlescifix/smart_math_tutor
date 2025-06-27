def update_points_and_streak(session, was_correct: bool):
    """Update score, streak, max streak, and level for a session."""
    if was_correct:
        session.score += 10
        session.streak += 1
        session.max_streak = max(session.max_streak, session.streak)
    else:
        session.score += 2
        session.streak = 0  # reset streak on wrong answer

    # Basic level logic
    session.level = int(session.score // 30) + 1

    return session


def assign_badge(streak: int, level: int) -> str:
    """
    Returns a badge name based on current streak and level.
    """
    if streak >= 10:
        return "🔥 Math Master"
    elif streak >= 5:
        return "💡 Brain Streak"
    elif level >= 5:
        return "🎓 Rising Genius"
    elif level >= 3:
        return "🚀 Level Up"
    elif streak >= 3:
        return "🔄 On Fire"
    else:
        return "✅ Keep Going"
