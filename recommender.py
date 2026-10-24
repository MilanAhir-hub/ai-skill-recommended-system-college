"""
recommender.py
--------------
Rule-based recommendation engine for career matching, skill gap analysis and
career path generation. No machine-learning model, no training data and no
external API is used anywhere: every number below is produced by explainable
arithmetic over the static knowledge base in career_data.py.

Algorithm 1 - Weighted Multi-Criteria Scoring (career fit)
----------------------------------------------------------
Total Score (0 - 100) = (
    (Weighted Skill Match Ratio * 0.50) +
    (Interest Match Ratio      * 0.30) +
    (Education Match Ratio     * 0.20)
) * 100  + goal bonus (if the student's stated goal matches this career)

Where:
- Weighted Skill Match Ratio = sum(weights of matched required skills)
                               / sum(weights of all required skills)
  Core skills count CORE_SKILL_WEIGHT (2.0), supporting skills count 1.0, so
  missing a must-have hurts more than missing a nice-to-have.
- Interest Match Ratio  = matched career interests / total career interests
- Education Match Ratio = keyword heuristic over the student's degree (0 - 1)

Algorithm 2 - Prerequisite Graph Traversal (career path)
--------------------------------------------------------
1. Skill gap          : required skills the student does not have yet.
2. Prerequisite close : recursively pull in any missing prerequisite of a gap
                        skill, so the plan never asks the student to learn
                        React before JavaScript.
3. Topological sort   : order skills so dependencies always come first,
                        tie-broken by (difficulty, learning hours, name).
4. Phase assignment   : Beginner -> Phase 1, Intermediate -> Phase 2,
                        Advanced -> Phase 3, pushed later if a prerequisite
                        landed in a later phase. Phase 4 is job readiness.
5. Duration estimate  : learning hours / study hours per week -> weeks/months.
6. Role progression   : the career's 5-stage ladder is attached with the
                        student's current readiness mapped onto it.
"""

import math
import re

from career_data import (
    CAREER_DATABASE,
    MATCH_WEIGHTS,
    SKILL_ROADMAPS,
    SKILL_LIBRARY,
    GOAL_BONUS_POINTS,
    CORE_SKILL_WEIGHT,
    SUPPORTING_SKILL_WEIGHT,
    DEFAULT_HOURS_PER_WEEK,
    MIN_HOURS_PER_WEEK,
    MAX_HOURS_PER_WEEK,
    DIFFICULTY_ORDER,
    PHASE_BLUEPRINT,
    JOB_READINESS_STEPS,
    ALGORITHM_CATALOG,
    ALGORITHM_COMBOS,
    canonical_skill,
    get_skill_meta,
    get_career_by_id,
    resolve_goal_to_career_id,
)

# The optional, selectable algorithms live beside this engine. Importing the
# module does not change any default: mcda + topological stay in charge unless
# the caller asks for something else.
import algorithms

# Readiness bands mapped from weighted skill coverage (0 - 100).
READINESS_BANDS = [
    (80, "Job Ready", "You already cover most of this role's benchmark skills - focus on proof of work and interviews."),
    (60, "Interview Ready", "You have the core of this role. Close the last gaps and start applying in parallel."),
    (40, "Developing", "A solid base is in place. Phase 2 of the plan is where this role becomes realistic."),
    (20, "Foundation Builder", "You have made a start. Work through the foundations before applying for this role."),
    (0, "Explorer", "This is a fresh start for you. The plan below begins from the basics.")
]


# ==========================================
# 1. Normalisation helpers
# ==========================================
def normalize_string_list(items):
    """
    Cleans and normalizes a list of strings:
    - Trims whitespace
    - Converts to lowercase for case-insensitive matching
    - Filters out empty or non-string items
    """
    if not items or not isinstance(items, list):
        return []

    normalized = []
    for item in items:
        if isinstance(item, str) and item.strip():
            normalized.append(item.strip().lower())
    return normalized


def canonicalize_user_skills(user_skills):
    """
    Maps every skill the student entered onto its canonical knowledge-base name
    using career_data.canonical_skill (handles case, spacing and aliases such
    as "js" -> "JavaScript" or "ml" -> "Machine Learning").

    Returns (canonical_set, resolution_log) where resolution_log records the
    aliases that were translated, so the explanation shown to the student can
    stay honest about what the engine did with their input.
    """
    if not user_skills or not isinstance(user_skills, list):
        return set(), []

    canonical = set()
    resolution_log = []

    for raw in user_skills:
        resolved = canonical_skill(raw)
        if not resolved:
            continue
        canonical.add(resolved)
        if isinstance(raw, str) and raw.strip() != resolved:
            resolution_log.append({"entered": raw.strip(), "matched_as": resolved})

    return canonical, resolution_log


def infer_implied_skills(known_skills):
    """
    Walks the prerequisite graph upward from the skills the student claims.

    If someone lists React they necessarily know JavaScript, and someone who
    lists Network Security has already covered Computer Networking. Without
    this step the engine would report those prerequisites as gaps and put them
    in the learning plan, which reads as nonsense to the student.

    Returns the set of implied prerequisite skills they did not list.
    """
    known = set(known_skills or [])
    implied = set()
    queue = list(known)

    while queue:
        skill = queue.pop()
        for prereq in get_skill_meta(skill)["prerequisites"]:
            if prereq not in known and prereq not in implied:
                implied.add(prereq)
                queue.append(prereq)

    return implied


def clamp_hours_per_week(hours_per_week):
    """Keeps the study pace inside a sane range before any duration maths."""
    try:
        hours = int(hours_per_week)
    except (TypeError, ValueError):
        return DEFAULT_HOURS_PER_WEEK

    if hours < MIN_HOURS_PER_WEEK:
        return MIN_HOURS_PER_WEEK
    if hours > MAX_HOURS_PER_WEEK:
        return MAX_HOURS_PER_WEEK
    return hours


# ==========================================
# 2. Matching criteria
# ==========================================
def calculate_skill_match(user_skills, required_skills, core_skills=None):
    """
    Compares user skills against career required skills using weighted scoring:
    core skills count CORE_SKILL_WEIGHT, supporting skills count 1.0.

    Skills implied by the prerequisite graph count as matched too (listing
    React implies JavaScript), and those are reported separately so the
    explanation stays honest about what the student actually typed.

    Returns:
    - match_ratio (float between 0.0 and 1.0, weighted)
    - matched_skills (list of required skill names the student already has)
    - missing_skills (list of required skill names still to learn)
    - missing_core_skills (the must-have subset of missing_skills)
    - implied_matches (matched skills credited through a prerequisite)
    """
    if not required_skills:
        return 0.0, [], [], [], []

    core_set = set(core_skills or [])
    user_canonical, _ = canonicalize_user_skills(user_skills)
    implied_skills = infer_implied_skills(user_canonical)

    # Keep a lowercase copy so a student-typed skill outside the library still
    # matches a required skill by plain text.
    user_lower = {skill.lower() for skill in user_canonical}

    matched_skills = []
    missing_skills = []
    missing_core_skills = []
    implied_matches = []

    matched_weight = 0.0
    total_weight = 0.0

    for req_skill in required_skills:
        weight = CORE_SKILL_WEIGHT if req_skill in core_set else SUPPORTING_SKILL_WEIGHT
        total_weight += weight

        if req_skill in user_canonical or req_skill.lower() in user_lower:
            matched_skills.append(req_skill)
            matched_weight += weight
        elif req_skill in implied_skills:
            matched_skills.append(req_skill)
            implied_matches.append(req_skill)
            matched_weight += weight
        else:
            missing_skills.append(req_skill)
            if req_skill in core_set:
                missing_core_skills.append(req_skill)

    match_ratio = (matched_weight / total_weight) if total_weight else 0.0
    return match_ratio, matched_skills, missing_skills, missing_core_skills, implied_matches


def calculate_interest_match(user_interests, relevant_interests):
    """
    Compares user interests with career relevant interests.
    Exact matches always count; substring matches only count for inputs of at
    least 4 characters, which stops noise like "ai" matching "Retail".

    Returns:
    - match_ratio (float between 0.0 and 1.0)
    - matched_interests (list of career interests matched)
    """
    if not relevant_interests or not user_interests:
        return 0.0, []

    user_interests_clean = normalize_string_list(user_interests)
    matched_interests = []

    for career_interest in relevant_interests:
        ci_lower = career_interest.lower()
        is_matched = False

        for ui in user_interests_clean:
            if ci_lower == ui:
                is_matched = True
                break
            if len(ui) >= 4 and (ci_lower in ui or ui in ci_lower):
                is_matched = True
                break

        if is_matched:
            matched_interests.append(career_interest)

    match_ratio = min(1.0, len(matched_interests) / len(relevant_interests))
    return match_ratio, matched_interests


def calculate_education_match(user_education, career):
    """
    Evaluates education compatibility heuristically.
    Checks if user education contains relevant degrees or field keywords.
    Returns a ratio between 0.0 and 1.0.
    """
    if not user_education or not isinstance(user_education, str):
        return 0.0

    edu_lower = user_education.strip().lower()
    if not edu_lower:
        return 0.0

    keywords = career.get("education_keywords", [])

    # Direct keyword match for the career's domain (e.g., Computer Science, Statistics, Design)
    for kw in keywords:
        if kw in edu_lower:
            return 1.0

    # General technical / engineering degree mentions
    general_tech_terms = [
        "engineering", "tech", "technology", "stem", "bachelor",
        "master", "b.tech", "b.e", "b.sc", "bca", "mca", "diploma"
    ]
    if any(term in edu_lower for term in general_tech_terms):
        return 0.75

    # Any other education mentioned
    return 0.40


def _tokenize(text):
    """Splits text into lowercase word tokens, dropping punctuation."""
    return {token for token in re.split(r"[^a-z0-9]+", text.lower()) if token}


def check_goal_match(user_goal, career):
    """
    True when the student's stated target career clearly refers to this career.
    Three explainable rules, in order:
    1. Job-title synonym lookup ("ML Engineer" -> ai_ml_engineer).
    2. Plain substring match either way ("Data Analyst" vs "Data Analyst").
    3. Token subset for multi-word goals ("AI Engineer" -> "AI/ML Engineer").
    """
    if not user_goal or not isinstance(user_goal, str):
        return False

    goal = user_goal.strip().lower()
    if not goal:
        return False

    # 1. Known job-title synonym
    resolved_id = resolve_goal_to_career_id(goal)
    if resolved_id:
        return resolved_id == career["id"]

    # 2. Direct substring match
    title = career["title"].lower()
    if goal in title or title in goal:
        return True

    # 3. Every word of a multi-word goal appears in the career title or id
    goal_tokens = _tokenize(goal)
    if len(goal_tokens) >= 2:
        career_tokens = _tokenize(career["title"]) | _tokenize(career["id"].replace("_", " "))
        if goal_tokens.issubset(career_tokens):
            return True

    return False


# ==========================================
# 3. Career path generation (prerequisite graph)
# ==========================================
def expand_missing_with_prerequisites(missing_skills, known_skills):
    """
    Closes the skill gap over the prerequisite graph: for every missing skill,
    pulls in any prerequisite the student does not already have.

    Example: a career requires Deep Learning. The student knows Python but not
    Machine Learning, so the plan silently adds Machine Learning as a bridge
    skill instead of asking them to start with Deep Learning.

    Returns (all_needed_skills, bridge_skills).
    """
    known = set(known_skills or [])
    needed = []
    seen = set()
    bridge_skills = []

    queue = list(missing_skills or [])
    direct = set(missing_skills or [])

    while queue:
        skill = queue.pop(0)
        if not skill or skill in seen or skill in known:
            continue

        seen.add(skill)
        needed.append(skill)
        if skill not in direct:
            bridge_skills.append(skill)

        for prereq in get_skill_meta(skill)["prerequisites"]:
            if prereq not in known and prereq not in seen:
                queue.append(prereq)

    return needed, bridge_skills


def _skill_sort_key(skill):
    """Sorts easier, shorter skills first so early wins come quickly."""
    meta = get_skill_meta(skill)
    return (
        DIFFICULTY_ORDER.get(meta["difficulty"], 2),
        meta["learning_hours"],
        skill.lower()
    )


def order_skills_by_prerequisites(skills, known_skills):
    """
    Topological sort (Kahn's algorithm) over the needed skills so that a skill
    never appears before its prerequisites. Ties are broken by difficulty, then
    learning hours, then name, which keeps the ordering deterministic.
    """
    needed = set(skills or [])
    known = set(known_skills or [])

    pending = {}
    for skill in needed:
        prereqs = [
            p for p in get_skill_meta(skill)["prerequisites"]
            if p in needed and p not in known
        ]
        pending[skill] = prereqs

    ordered = []
    resolved = set()

    while pending:
        ready = [s for s, prereqs in pending.items() if all(p in resolved for p in prereqs)]

        # Cycle guard: the data is validated, but never loop forever.
        if not ready:
            ready = [sorted(pending.keys(), key=_skill_sort_key)[0]]

        ready.sort(key=_skill_sort_key)
        for skill in ready:
            ordered.append(skill)
            resolved.add(skill)
            pending.pop(skill, None)

    return ordered


def assign_skills_to_phases(ordered_skills):
    """
    Maps each skill onto a learning phase: Beginner -> 1, Intermediate -> 2,
    Advanced -> 3, then pushes a skill later if one of its prerequisites ended
    up in a later phase. Returns {skill: phase_number}.
    """
    phase_of = {}

    for skill in ordered_skills:
        meta = get_skill_meta(skill)
        base_phase = DIFFICULTY_ORDER.get(meta["difficulty"], 2)

        prereq_phases = [
            phase_of[p] for p in meta["prerequisites"] if p in phase_of
        ]
        phase_of[skill] = max([base_phase] + prereq_phases)

    return phase_of


def describe_duration(total_hours, hours_per_week):
    """Converts study hours into a readable weeks/months estimate."""
    if total_hours <= 0:
        return {"total_hours": 0, "hours_per_week": hours_per_week,
                "estimated_weeks": 0, "estimated_months": 0.0,
                "estimated_duration": "No new learning required"}

    weeks = int(math.ceil(total_hours / float(hours_per_week)))
    months = round(weeks / 4.345, 1)

    if weeks <= 4:
        label = "About {0} week(s)".format(weeks)
    elif months < 1.5:
        label = "About 1 month"
    else:
        label = "About {0} months".format(months)

    return {
        "total_hours": total_hours,
        "hours_per_week": hours_per_week,
        "estimated_weeks": weeks,
        "estimated_months": months,
        "estimated_duration": label
    }


def build_learning_plan(missing_skills, known_skills, career, hours_per_week=DEFAULT_HOURS_PER_WEEK,
                        path_algorithm=algorithms.DEFAULT_PATH_ALGORITHM):
    """
    Builds the phased learning plan: the core of the generated career path.
    Every phase lists its skills with difficulty, hours, prerequisites,
    resources and roadmap steps, plus its own duration estimate.

    path_algorithm selects how the needed skills are grouped:
    - "topological" (default, unchanged): Kahn's sort into difficulty phases.
    - "bfs": breadth-first dependency levels, where everything in a level can
      be studied in parallel. Both produce the same output shape.
    """
    hours_per_week = clamp_hours_per_week(hours_per_week)
    path_algorithm = algorithms.resolve_path_algorithm(path_algorithm)

    needed, bridge_skills = expand_missing_with_prerequisites(missing_skills, known_skills)

    # --- Alternative path algorithm: breadth-first dependency levels ---
    if path_algorithm == "bfs":
        return algorithms.build_bfs_learning_plan(
            needed, bridge_skills, known_skills, career,
            hours_per_week, missing_skills
        )

    # --- Original path algorithm: topological sort into difficulty phases ---
    ordered = order_skills_by_prerequisites(needed, known_skills)
    phase_of = assign_skills_to_phases(ordered)

    direct_gap = set(missing_skills or [])
    core_set = set(career.get("core_skills", []))

    # Group the skills into their phase buckets, preserving topological order.
    grouped = {1: [], 2: [], 3: []}
    for skill in ordered:
        meta = get_skill_meta(skill)
        grouped.setdefault(phase_of[skill], []).append({
            "skill": skill,
            "category": meta["category"],
            "difficulty": meta["difficulty"],
            "learning_hours": meta["learning_hours"],
            "prerequisites": meta["prerequisites"],
            "resources": meta["resources"],
            "steps": meta["roadmap"],
            "is_core_skill": skill in core_set,
            "is_bridge_skill": skill not in direct_gap,
            "in_knowledge_base": meta["in_knowledge_base"]
        })

    phases = []
    total_hours = 0
    week_cursor = 0

    for blueprint in PHASE_BLUEPRINT:
        number = blueprint["phase"]

        # Phase 4 is always the applied / job-readiness phase.
        if number == 4:
            phases.append({
                "phase": number,
                "name": blueprint["name"],
                "goal": blueprint["goal"],
                "focus_difficulty": "Applied",
                "skills": [],
                "action_steps": list(JOB_READINESS_STEPS),
                "portfolio_projects": list(career.get("portfolio_projects", [])),
                "certifications": list(career.get("certifications", [])),
                "estimated_hours": 0,
                "estimated_weeks": 4,
                "starts_week": week_cursor + 1,
                "ends_week": week_cursor + 4
            })
            week_cursor += 4
            continue

        phase_skills = grouped.get(number, [])
        if not phase_skills:
            continue

        phase_hours = sum(item["learning_hours"] for item in phase_skills)
        phase_weeks = int(math.ceil(phase_hours / float(hours_per_week)))
        total_hours += phase_hours

        phases.append({
            "phase": number,
            "name": blueprint["name"],
            "goal": blueprint["goal"],
            "focus_difficulty": blueprint["difficulty"],
            "skills": phase_skills,
            "action_steps": [],
            "portfolio_projects": [],
            "certifications": [],
            "estimated_hours": phase_hours,
            "estimated_weeks": phase_weeks,
            "starts_week": week_cursor + 1,
            "ends_week": week_cursor + phase_weeks
        })
        week_cursor += phase_weeks

    # Renumber phases so the student never sees "Phase 1, Phase 3" when a
    # difficulty bucket was empty (e.g. no beginner gaps left to close).
    for display_number, phase in enumerate(phases, start=1):
        phase["display_phase"] = display_number
        _, _, label = phase["name"].partition(" - ")
        phase["name"] = "Phase {0} - {1}".format(display_number, label or phase["name"])

    duration = describe_duration(total_hours, hours_per_week)

    # The three skills worth starting this week: earliest phase first (so every
    # prerequisite is already satisfied), core skills prioritised within a
    # phase so effort lands where the fit score moves most.
    priority = sorted(
        range(len(ordered)),
        key=lambda i: (phase_of[ordered[i]], 0 if ordered[i] in core_set else 1, i)
    )[:3]
    priority = [ordered[i] for i in priority]

    return {
        "algorithm": "topological",
        "hours_per_week": hours_per_week,
        "total_skills_to_learn": len(ordered),
        "skill_sequence": ordered,
        "bridge_skills": bridge_skills,
        "start_with": priority,
        "phases": phases,
        "total_learning_hours": total_hours,
        "estimated_weeks": duration["estimated_weeks"],
        "estimated_months": duration["estimated_months"],
        "estimated_duration": duration["estimated_duration"]
    }


def determine_readiness(skill_ratio, missing_core_skills):
    """
    Maps weighted skill coverage onto a readiness band, which tells the student
    where they stand against the entry bar for this career right now.
    """
    coverage = round(skill_ratio * 100, 2)

    level, message = READINESS_BANDS[-1][1], READINESS_BANDS[-1][2]
    for threshold, band_level, band_message in READINESS_BANDS:
        if coverage >= threshold:
            level, message = band_level, band_message
            break

    return {
        "level": level,
        "skill_coverage_percentage": coverage,
        "message": message,
        "blocking_core_skills": list(missing_core_skills),
        "entry_ready": coverage >= 60 and not missing_core_skills
    }


def build_progression_ladder(career, known_skills, readiness):
    """
    Attaches the career's role progression ladder and marks where the student
    is on it. Stage 1 is the target to enter; later stages are mapped out with
    the skills each one expects, including the ones already acquired.
    """
    known = set(known_skills or [])
    ladder = []

    for stage in career.get("career_path", []):
        stage_skills = stage.get("skills_to_add", [])
        already_have = [s for s in stage_skills if s in known]
        still_needed = [s for s in stage_skills if s not in known]

        if stage["stage"] == 1:
            status = "entered" if readiness["entry_ready"] else "target"
        elif stage["stage"] == 2:
            status = "next"
        else:
            status = "future"

        ladder.append({
            "stage": stage["stage"],
            "level": stage["level"],
            "role": stage["role"],
            "experience": stage["experience"],
            "salary_inr": stage["salary_inr"],
            "focus": stage["focus"],
            "milestone": stage["milestone"],
            "skills_to_add": stage_skills,
            "skills_already_acquired": already_have,
            "skills_still_needed": still_needed,
            "status": status
        })

    return ladder


def generate_career_path(career, user, matched_skills, missing_skills,
                         missing_core_skills, skill_ratio,
                         hours_per_week=DEFAULT_HOURS_PER_WEEK,
                         path_algorithm=algorithms.DEFAULT_PATH_ALGORITHM):
    """
    Full career path for one career: readiness, phased learning plan, role
    progression ladder, market context and the immediate next actions.
    """
    known_skills, _ = canonicalize_user_skills(user.get("skills", []))
    known_skills |= infer_implied_skills(known_skills)
    known_skills |= set(matched_skills)

    readiness = determine_readiness(skill_ratio, missing_core_skills)
    learning_plan = build_learning_plan(
        missing_skills, known_skills, career, hours_per_week, path_algorithm
    )
    ladder = build_progression_ladder(career, known_skills, readiness)

    # Immediate, concrete next actions derived from the plan.
    next_actions = []
    for skill in learning_plan["start_with"]:
        meta = get_skill_meta(skill)
        next_actions.append(
            "Start {0} ({1}, ~{2} hrs): {3}".format(
                skill, meta["difficulty"], meta["learning_hours"], meta["roadmap"][0]
            )
        )

    if career.get("portfolio_projects"):
        next_actions.append(
            "Plan your first portfolio project: {0}".format(career["portfolio_projects"][0])
        )
    if career.get("certifications"):
        next_actions.append(
            "Target one credential this year: {0}".format(career["certifications"][0])
        )

    return {
        "career_id": career["id"],
        "career_title": career["title"],
        "readiness": readiness,
        "learning_plan": learning_plan,
        "progression_ladder": ladder,
        "entry_stage": ladder[0] if ladder else None,
        "long_term_role": ladder[-1]["role"] if ladder else "",
        "next_actions": next_actions,
        "market_insights": {
            "demand": career.get("demand", "Moderate"),
            "entry_salary_inr": career.get("entry_salary_inr", ""),
            "growth_outlook": career.get("growth_outlook", ""),
            "remote_friendly": career.get("remote_friendly", False),
            "industries": career.get("industries", []),
            "tools": career.get("tools", []),
            "soft_skills": career.get("soft_skills", [])
        },
        "certifications": career.get("certifications", []),
        "portfolio_projects": career.get("portfolio_projects", []),
        "related_careers": [
            {"id": rid, "title": get_career_by_id(rid)["title"]}
            for rid in career.get("related_careers", [])
            if get_career_by_id(rid)
        ]
    }


# ==========================================
# 4. Roadmap (kept for backwards compatibility)
# ==========================================
def generate_roadmap(missing_skills):
    """
    Generates a flat {skill: [steps]} roadmap for the missing skills.
    Predefined steps come from SKILL_ROADMAPS; unknown skills fall back to
    generic beginner steps via get_skill_meta.
    """
    roadmap = {}

    for skill in missing_skills or []:
        if skill in SKILL_ROADMAPS:
            roadmap[skill] = list(SKILL_ROADMAPS[skill])
        else:
            roadmap[skill] = list(get_skill_meta(skill)["roadmap"])

    return roadmap


# ==========================================
# 4b. Shared evidence collection (used by every scoring algorithm)
# ==========================================
def collect_evidence(user, career):
    """
    Measures one career against the normalised profile. Every scoring
    algorithm consumes the same evidence, so a difference in their output is a
    difference in reasoning, never a difference in the input they saw.
    """
    (skill_ratio, matched_skills, missing_skills,
     missing_core_skills, implied_matches) = calculate_skill_match(
        user.get("skills", []), career["required_skills"], career.get("core_skills")
    )
    interest_ratio, matched_interests = calculate_interest_match(
        user.get("interests", []), career["relevant_interests"]
    )
    education_ratio = calculate_education_match(user.get("education", ""), career)
    goal_match = check_goal_match(user.get("career_goal", ""), career)

    effective_skills, _ = canonicalize_user_skills(user.get("skills", []))
    effective_skills |= infer_implied_skills(effective_skills)

    return {
        "career_id": career["id"],
        "skill_ratio": skill_ratio,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "missing_core_skills": missing_core_skills,
        "implied_matches": implied_matches,
        "interest_ratio": interest_ratio,
        "matched_interests": matched_interests,
        "education_ratio": education_ratio,
        "goal_match": goal_match,
        "goal_bonus": GOAL_BONUS_POINTS if goal_match else 0.0,
        "effective_skills": effective_skills
    }


def build_request_context(user, scoring_algorithm, careers=None):
    """
    Precomputes everything a scoring algorithm needs across the whole career
    set, once per request:
    - the decision tree is walked once, not once per career
    - Bayes posteriors must be normalised over all careers, so every career's
      evidence is gathered before any score is produced
    """
    if careers is None:
        careers = CAREER_DATABASE

    scoring_algorithm = algorithms.resolve_scoring_algorithm(scoring_algorithm)
    context = {"scoring_algorithm": scoring_algorithm, "evidence": {}}

    if scoring_algorithm == "mcda":
        return context

    for career in careers:
        context["evidence"][career["id"]] = collect_evidence(user, career)

    if scoring_algorithm == "decision_tree":
        known_skills, _ = canonicalize_user_skills(user.get("skills", []))
        known_skills |= infer_implied_skills(known_skills)
        context["traversal"] = algorithms.traverse_decision_tree(
            user.get("interests", []), known_skills
        )

    if scoring_algorithm == "bayes":
        context["posteriors"] = algorithms.bayes_posteriors(context["evidence"], careers)

    return context


# ==========================================
# 5. Scoring one career
# ==========================================
def evaluate_career_for_user(user, career, weights=None, hours_per_week=DEFAULT_HOURS_PER_WEEK,
                             scoring_algorithm=algorithms.DEFAULT_SCORING_ALGORITHM,
                             path_algorithm=algorithms.DEFAULT_PATH_ALGORITHM,
                             context=None):
    """
    Calculates the matching score, skill gap analysis and generated career path
    for one career.

    Parameters:
    - user: dict with keys 'skills', 'interests', 'education', 'career_goal'
    - career: dict from CAREER_DATABASE
    - weights: dict of weights, defaults to MATCH_WEIGHTS
    - hours_per_week: study pace used for the career path duration estimates
    - scoring_algorithm: "mcda" (default), "decision_tree" or "bayes"
    - path_algorithm: "topological" (default) or "bfs"
    - context: precomputed request context from build_request_context

    The original MCDA score is always computed and reported, whichever
    algorithm is selected, so the alternatives can be compared against the
    baseline without a second request.
    """
    if weights is None:
        weights = MATCH_WEIGHTS

    scoring_algorithm = algorithms.resolve_scoring_algorithm(scoring_algorithm)
    path_algorithm = algorithms.resolve_path_algorithm(path_algorithm)
    if context is None or context.get("scoring_algorithm") != scoring_algorithm:
        context = build_request_context(user, scoring_algorithm)

    user_skills = user.get("skills", [])
    user_interests = user.get("interests", [])
    user_education = user.get("education", "")
    user_goal = user.get("career_goal", "")

    # 1. Weighted skill match (50% default)
    (skill_ratio, matched_skills, missing_skills,
     missing_core_skills, implied_matches) = calculate_skill_match(
        user_skills, career["required_skills"], career.get("core_skills")
    )

    # 2. Interest match (30% default)
    interest_ratio, matched_interests = calculate_interest_match(
        user_interests, career["relevant_interests"]
    )

    # 3. Education match (20% default)
    education_ratio = calculate_education_match(user_education, career)

    # 4. Weighted heuristic scoring formula
    skill_weight = weights.get("skill", 0.50)
    interest_weight = weights.get("interest", 0.30)
    education_weight = weights.get("education", 0.20)

    raw_score = (
        (skill_ratio * skill_weight) +
        (interest_ratio * interest_weight) +
        (education_ratio * education_weight)
    )
    base_score = raw_score * 100

    # 5. Small bonus when this career is the student's stated goal
    is_goal_match = check_goal_match(user_goal, career)
    goal_bonus = GOAL_BONUS_POINTS if is_goal_match else 0.0

    mcda_score = round(max(0.0, min(100.0, base_score + goal_bonus)), 2)
    normalized_score = mcda_score

    # 6. Selected scoring algorithm. MCDA above is always computed; when another
    #    algorithm is chosen it produces the headline score instead, and the
    #    MCDA figure stays available as the reference baseline.
    scoring_info = algorithms.algorithm_info(scoring_algorithm, "scoring")
    algorithm_detail = {
        "explanation": [
            "Weighted criteria: {0}% skills + {1}% interests + {2}% education.".format(
                int(skill_weight * 100), int(interest_weight * 100), int(education_weight * 100)
            ),
            "Core skills counted at {0}x against supporting skills.".format(int(CORE_SKILL_WEIGHT)),
            "Base {0}%{1} gives the final fit score.".format(
                round(base_score, 2),
                " plus a {0}-point goal bonus".format(int(goal_bonus)) if goal_bonus else ""
            )
        ]
    }

    if scoring_algorithm == "decision_tree":
        evidence = context["evidence"].get(career["id"]) or collect_evidence(user, career)
        tree_result = algorithms.score_decision_tree(career, evidence, context["traversal"])
        normalized_score = tree_result["score"]
        algorithm_detail = tree_result

    elif scoring_algorithm == "bayes":
        posterior = context.get("posteriors", {}).get(career["id"])
        if posterior is None:
            evidence = context["evidence"].get(career["id"]) or collect_evidence(user, career)
            posterior = algorithms.bayes_posteriors({career["id"]: evidence}, [career])[career["id"]]
        normalized_score = posterior["score"]
        algorithm_detail = posterior

    # 7. Roadmap + full generated career path
    roadmap = generate_roadmap(missing_skills)
    career_path = generate_career_path(
        career, user, matched_skills, missing_skills,
        missing_core_skills, skill_ratio, hours_per_week, path_algorithm
    )

    learning_plan = career_path["learning_plan"]
    total_required = len(career["required_skills"])

    return {
        "career_id": career["id"],
        "career_title": career["title"],
        "career_category": career.get("category", "General"),
        "description": career["description"],
        "recommended_education": career["recommended_education"],
        "matching_score": normalized_score,
        "algorithm": {
            "scoring": {
                "id": scoring_algorithm,
                "name": scoring_info["name"] if scoring_info else scoring_algorithm,
                "family": scoring_info["family"] if scoring_info else "",
                "score_label": scoring_info["score_label"] if scoring_info else "Score",
                "score_scale": scoring_info["score_scale"] if scoring_info else "",
                "detail": algorithm_detail
            },
            "path": {
                "id": path_algorithm,
                "name": (algorithms.algorithm_info(path_algorithm, "path") or {}).get("name", path_algorithm),
                "phase_label": (algorithms.algorithm_info(path_algorithm, "path") or {}).get("phase_label", "Phase")
            },
            "mcda_reference_score": mcda_score,
            "is_default_algorithm": (
                scoring_algorithm == algorithms.DEFAULT_SCORING_ALGORITHM
                and path_algorithm == algorithms.DEFAULT_PATH_ALGORITHM
            )
        },
        "score_breakdown": {
            "skill_match_percentage": round(skill_ratio * 100, 2),
            "interest_match_percentage": round(interest_ratio * 100, 2),
            "education_match_percentage": round(education_ratio * 100, 2),
            "base_score": round(base_score, 2),
            "goal_bonus_points": goal_bonus,
            "weights_used": {
                "skill": "{0}%".format(int(skill_weight * 100)),
                "interest": "{0}%".format(int(interest_weight * 100)),
                "education": "{0}%".format(int(education_weight * 100))
            },
            "note": "Core skills are weighted {0}x against supporting skills in the skill match.".format(
                int(CORE_SKILL_WEIGHT)
            )
        },
        "ai_algo_breakdown": {
            "algorithm": "Rule-Based Skill Gap Analysis, Weighted MCDA & Prerequisite Graph Traversal",
            "bullets": [
                "Skill Analysis: Matched {0} of {1} benchmark skill(s) ({2}% weighted coverage) and detected {3} gap skill(s) for {4}.{5}".format(
                    len(matched_skills), total_required, round(skill_ratio * 100, 1),
                    len(missing_skills), career["title"],
                    " Credited {0} skill(s) implied by your existing ones ({1}).".format(
                        len(implied_matches), ", ".join(implied_matches)
                    ) if implied_matches else ""
                ),
                "Interest Alignment: Evaluated {0} matching domain interest(s) ({1}% alignment).".format(
                    len(matched_interests), round(interest_ratio * 100, 1)
                ),
                "Academic Relevance: Evaluated education background against domain requirements ({0}% match).".format(
                    round(education_ratio * 100, 1)
                ),
                "Weighted Score Prediction: Aggregated 50% skills + 30% interests + 20% education{0} into a final {1}% match score.".format(
                    " + {0} pt goal bonus".format(int(goal_bonus)) if goal_bonus else "",
                    normalized_score
                ),
                "Career Path Generation: Sequenced {0} skill(s) across {1} phase(s) using the prerequisite graph, estimated at {2} study hours ({3}).".format(
                    learning_plan["total_skills_to_learn"], len(learning_plan["phases"]),
                    learning_plan["total_learning_hours"], learning_plan["estimated_duration"]
                )
            ]
        },
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "missing_core_skills": missing_core_skills,
        "implied_skills": implied_matches,
        "matched_interests": matched_interests,
        "skill_gap_summary": {
            "total_required_skills": total_required,
            "matched_count": len(matched_skills),
            "missing_count": len(missing_skills),
            "missing_core_count": len(missing_core_skills),
            "implied_count": len(implied_matches),
            "bridge_skill_count": len(learning_plan["bridge_skills"]),
            "weighted_coverage_percentage": round(skill_ratio * 100, 2)
        },
        "matches_career_goal": is_goal_match,
        "learning_roadmap": roadmap,
        "career_path": career_path
    }


# ==========================================
# 6. Ranking all careers
# ==========================================
def get_top_career_recommendations(user, careers=None, top_n=3, weights=None,
                                   hours_per_week=DEFAULT_HOURS_PER_WEEK,
                                   scoring_algorithm=algorithms.DEFAULT_SCORING_ALGORITHM,
                                   path_algorithm=algorithms.DEFAULT_PATH_ALGORITHM):
    """
    Evaluates all careers in the knowledge base for a given user profile.
    Returns the top 'top_n' careers sorted by matching_score (descending).
    Ties are broken by weighted skill coverage, then by career title, so the
    ranking is stable and reproducible for the same input.
    """
    if careers is None:
        careers = CAREER_DATABASE

    scoring_algorithm = algorithms.resolve_scoring_algorithm(scoring_algorithm)
    path_algorithm = algorithms.resolve_path_algorithm(path_algorithm)

    # Built once: the decision tree is walked a single time, and Bayes needs
    # every career's evidence before any posterior can be normalised.
    context = build_request_context(user, scoring_algorithm, careers)

    results = []
    for career in careers:
        results.append(evaluate_career_for_user(
            user, career, weights, hours_per_week,
            scoring_algorithm, path_algorithm, context
        ))

    results.sort(
        key=lambda item: (
            -item["matching_score"],
            -item["skill_gap_summary"]["weighted_coverage_percentage"],
            item["career_title"]
        )
    )

    try:
        limit = int(top_n)
    except (TypeError, ValueError):
        limit = 3
    limit = max(1, min(limit, len(results)))

    return results[:limit]


def recommend_single_career(user, career_id, hours_per_week=DEFAULT_HOURS_PER_WEEK,
                            scoring_algorithm=algorithms.DEFAULT_SCORING_ALGORITHM,
                            path_algorithm=algorithms.DEFAULT_PATH_ALGORITHM):
    """
    Full evaluation for one specific career chosen by the student, even when it
    is not in their top matches. Powers the "explore any career path" endpoint.
    Returns None when the career id is unknown.
    """
    career = get_career_by_id(career_id)
    if not career:
        return None

    # Bayes posteriors are shares of 100% across every career, so the context
    # must still be built over the whole catalog even for a single lookup.
    context = build_request_context(user, scoring_algorithm)
    return evaluate_career_for_user(
        user, career, hours_per_week=hours_per_week,
        scoring_algorithm=scoring_algorithm, path_algorithm=path_algorithm,
        context=context
    )


def compare_careers(user, career_ids, hours_per_week=DEFAULT_HOURS_PER_WEEK,
                    scoring_algorithm=algorithms.DEFAULT_SCORING_ALGORITHM,
                    path_algorithm=algorithms.DEFAULT_PATH_ALGORITHM):
    """
    Side-by-side comparison of several careers for the same student profile,
    sorted best fit first. Unknown ids are ignored.
    """
    context = build_request_context(user, scoring_algorithm)

    evaluations = []
    for career_id in career_ids or []:
        career = get_career_by_id(career_id)
        if not career:
            continue
        evaluations.append(evaluate_career_for_user(
            user, career, hours_per_week=hours_per_week,
            scoring_algorithm=scoring_algorithm, path_algorithm=path_algorithm,
            context=context
        ))

    evaluations.sort(key=lambda item: -item["matching_score"])
    return evaluations


# ==========================================
# 7. "What if I choose a different algorithm?"
# ==========================================
def compare_algorithms(user, hours_per_week=DEFAULT_HOURS_PER_WEEK, top_n=3, careers=None):
    """
    Runs every scoring algorithm and every path algorithm over the same
    profile and reports what changes. This is the answer to "if we choose this
    one, then what?": the same student, the same knowledge base, three ways of
    ranking careers and two ways of ordering the learning.

    Returns the per-algorithm rankings, where they agree, and the trade-off
    each choice implies.
    """
    if careers is None:
        careers = CAREER_DATABASE

    hours_per_week = clamp_hours_per_week(hours_per_week)
    top_n = max(1, min(int(top_n or 3), len(careers)))

    # --- Scoring algorithms: same evidence, three different rankings ---
    scoring_results = []
    rankings = {}

    for entry in ALGORITHM_CATALOG["scoring"]:
        algorithm_id = entry["id"]
        ranked = get_top_career_recommendations(
            user, careers=careers, top_n=top_n, hours_per_week=hours_per_week,
            scoring_algorithm=algorithm_id,
            path_algorithm=algorithms.DEFAULT_PATH_ALGORITHM
        )
        rankings[algorithm_id] = [item["career_id"] for item in ranked]

        scoring_results.append({
            "id": algorithm_id,
            "name": entry["name"],
            "family": entry["family"],
            "one_line": entry["one_line"],
            "score_label": entry["score_label"],
            "score_scale": entry["score_scale"],
            "is_default": entry.get("default", False),
            "strengths": entry["strengths"],
            "limits": entry["limits"],
            "top_career": ranked[0]["career_title"] if ranked else "",
            "top_career_id": ranked[0]["career_id"] if ranked else "",
            "top_score": ranked[0]["matching_score"] if ranked else 0.0,
            "ranking": [
                {
                    "rank": index + 1,
                    "career_id": item["career_id"],
                    "career_title": item["career_title"],
                    "score": item["matching_score"],
                    "why": (item["algorithm"]["scoring"]["detail"].get("explanation") or [""])[0]
                }
                for index, item in enumerate(ranked)
            ]
        })

    # --- Where the three algorithms agree ---
    top_choices = [result["top_career_id"] for result in scoring_results if result["top_career_id"]]
    unanimous = len(set(top_choices)) == 1 and len(top_choices) == len(scoring_results)

    all_top_sets = [set(ids) for ids in rankings.values() if ids]
    shared = set.intersection(*all_top_sets) if all_top_sets else set()
    shared_titles = [
        get_career_by_id(career_id)["title"]
        for career_id in sorted(shared) if get_career_by_id(career_id)
    ]

    if unanimous:
        agreement_verdict = (
            "All three scoring algorithms pick {0} first, so the recommendation is robust: "
            "it does not depend on which method you trust.".format(scoring_results[0]["top_career"])
        )
    else:
        agreement_verdict = (
            "The algorithms disagree on first place ({0}). That usually means the profile sits "
            "between two tracks: MCDA rewards overall coverage, the decision tree follows your "
            "strongest interest, and Bayes rewards skills that are distinctive to one career.".format(
                ", ".join(
                    "{0}: {1}".format(r["name"], r["top_career"]) for r in scoring_results
                )
            )
        )

    # --- Path algorithms, compared on the agreed (or MCDA) top career ---
    focus_id = scoring_results[0]["top_career_id"] if scoring_results else None
    focus_career = get_career_by_id(focus_id) if focus_id else None

    path_results = []
    if focus_career:
        for entry in ALGORITHM_CATALOG["path"]:
            evaluation = evaluate_career_for_user(
                user, focus_career, hours_per_week=hours_per_week,
                scoring_algorithm=algorithms.DEFAULT_SCORING_ALGORITHM,
                path_algorithm=entry["id"]
            )
            plan = evaluation["career_path"]["learning_plan"]
            first_phase = plan["phases"][0] if plan["phases"] else {}

            path_results.append({
                "id": entry["id"],
                "name": entry["name"],
                "family": entry["family"],
                "one_line": entry["one_line"],
                "phase_label": entry["phase_label"],
                "is_default": entry.get("default", False),
                "strengths": entry["strengths"],
                "limits": entry["limits"],
                "career_title": focus_career["title"],
                "total_skills": plan["total_skills_to_learn"],
                "total_hours": plan["total_learning_hours"],
                "estimated_weeks": plan["estimated_weeks"],
                "estimated_duration": plan["estimated_duration"],
                "phase_count": len(plan["phases"]),
                "first_group": [item["skill"] for item in first_phase.get("skills", [])],
                "start_with": plan["start_with"],
                "skill_sequence": plan["skill_sequence"],
                "extra": plan.get("bfs", {})
            })

    path_verdict = ""
    if len(path_results) == 2:
        topo, bfs = path_results[0], path_results[1]
        topo_groups = max(0, topo["phase_count"] - 1)
        bfs_groups = max(0, bfs["phase_count"] - 1)
        path_verdict = (
            "Both plans contain the same {0} skill(s) and the same {1} study hours, so neither is "
            "faster. They differ in shape: {2} gives {3} difficulty phase{4} in one fixed order, "
            "while {5} gives {6} dependency level{7} and shows that {8} skill(s) can be started "
            "today, in parallel.".format(
                topo["total_skills"], topo["total_hours"],
                topo["name"], topo_groups, "" if topo_groups == 1 else "s",
                bfs["name"], bfs_groups, "" if bfs_groups == 1 else "s",
                len(bfs["first_group"])
            )
        )

    # --- The two offered combos, each evaluated as a whole ---
    # A combo is scored by its own algorithm and its path is built for its own
    # top career, so this is the honest answer to "if I pick this pair, what
    # do I actually get?"
    combo_results = []
    for combo in ALGORITHM_COMBOS:
        ranked = get_top_career_recommendations(
            user, careers=careers, top_n=top_n, hours_per_week=hours_per_week,
            scoring_algorithm=combo["scoring"], path_algorithm=combo["path"]
        )
        if not ranked:
            continue

        winner = ranked[0]
        plan = winner["career_path"]["learning_plan"]
        first_phase = plan["phases"][0] if plan["phases"] else {}
        scoring_entry = algorithms.algorithm_info(combo["scoring"], "scoring") or {}
        path_entry = algorithms.algorithm_info(combo["path"], "path") or {}

        combo_results.append({
            "id": combo["id"],
            "label": combo["label"],
            "tagline": combo["tagline"],
            "best_for": combo["best_for"],
            "is_default": combo.get("default", False),
            "scoring": {
                "id": combo["scoring"],
                "name": scoring_entry.get("name", combo["scoring"]),
                "score_label": scoring_entry.get("score_label", "Score"),
                "score_scale": scoring_entry.get("score_scale", ""),
                "strengths": scoring_entry.get("strengths", []),
                "limits": scoring_entry.get("limits", [])
            },
            "path": {
                "id": combo["path"],
                "name": path_entry.get("name", combo["path"]),
                "phase_label": path_entry.get("phase_label", "Phase"),
                "strengths": path_entry.get("strengths", []),
                "limits": path_entry.get("limits", [])
            },
            "top_career": winner["career_title"],
            "top_career_id": winner["career_id"],
            "top_score": winner["matching_score"],
            "mcda_reference_score": winner["algorithm"]["mcda_reference_score"],
            "ranking": [
                {
                    "rank": index + 1,
                    "career_id": item["career_id"],
                    "career_title": item["career_title"],
                    "score": item["matching_score"]
                }
                for index, item in enumerate(ranked)
            ],
            "plan": {
                "total_skills": plan["total_skills_to_learn"],
                "total_hours": plan["total_learning_hours"],
                "estimated_weeks": plan["estimated_weeks"],
                "estimated_duration": plan["estimated_duration"],
                "group_count": max(0, len(plan["phases"]) - 1),
                "first_group_name": first_phase.get("name", ""),
                "first_group": [item["skill"] for item in first_phase.get("skills", [])],
                "start_with": plan["start_with"],
                "extra": plan.get("bfs", {})
            }
        })

    # Do the two combos land on the same career, and do they cost the same?
    combo_verdict = ""
    if len(combo_results) == 2:
        first, second = combo_results
        same_career = first["top_career_id"] == second["top_career_id"]
        same_cost = first["plan"]["total_hours"] == second["plan"]["total_hours"]

        if same_career:
            combo_verdict = (
                "Both combos pick {0} first, so the recommendation does not depend on which "
                "pair you trust. ".format(first["top_career"])
            )
        else:
            combo_verdict = (
                "The combos disagree on first place: {0} picks {1}, {2} picks {3}. That means the "
                "profile sits between two tracks - {0} rewards overall coverage across all three "
                "criteria, while {2} follows your single strongest interest down one branch. ".format(
                    first["label"], first["top_career"], second["label"], second["top_career"]
                )
            )

        if same_career and same_cost:
            combo_verdict += (
                "The learning content is identical too ({0} skills, {1} hours); only the grouping "
                "changes: {2} gives {3} difficulty phase{7} in one fixed order, while {4} gives {5} "
                "dependency level{8} and shows {6} skill(s) you could start today in parallel.".format(
                    first["plan"]["total_skills"], first["plan"]["total_hours"],
                    first["path"]["name"], first["plan"]["group_count"],
                    second["path"]["name"], second["plan"]["group_count"],
                    len(second["plan"]["first_group"]),
                    "" if first["plan"]["group_count"] == 1 else "s",
                    "" if second["plan"]["group_count"] == 1 else "s"
                )
            )
        else:
            combo_verdict += (
                "Because they target different careers, the plans differ too: {0} hours for {1} "
                "against {2} hours for {3}.".format(
                    first["plan"]["total_hours"], first["top_career"],
                    second["plan"]["total_hours"], second["top_career"]
                )
            )

    return {
        "profile_summary": {
            "skills": len(user.get("skills", []) or []),
            "interests": len(user.get("interests", []) or []),
            "education": user.get("education", ""),
            "goal": user.get("career_goal", ""),
            "hours_per_week": hours_per_week
        },
        "combos": combo_results,
        "combo_verdict": combo_verdict,
        "scoring_algorithms": scoring_results,
        "path_algorithms": path_results,
        "agreement": {
            "unanimous_top_career": unanimous,
            "top_choices": [
                {"algorithm": r["name"], "career": r["top_career"], "score": r["top_score"]}
                for r in scoring_results
            ],
            "shared_in_all_top_lists": shared_titles,
            "verdict": agreement_verdict
        },
        "path_comparison_verdict": path_verdict,
        "how_to_choose": [
            "Pick Combo 1 (Weighted MCDA + Topological Sort) for a balanced, explainable fit score and a syllabus-style order. It is the default and the easiest to defend line by line.",
            "Pick Combo 2 (Decision Tree + Breadth-First Search) when the reasoning matters as much as the number, and when you want to see what can be started today in parallel.",
            "Pick Weighted MCDA for a balanced, explainable fit score: it is the default and the easiest to defend line by line.",
            "Pick the Decision Tree when you want to see the reasoning as a path of questions, or when one interest clearly dominates.",
            "Pick Naive Bayes when you want a probability rather than a score, and want absent skills to count as evidence against a career. Note that it answers 'which career do you resemble today', so an ambitious goal you have barely started will rank lower here than under MCDA.",
            "Pick Topological Sort for a syllabus-style order, easiest topics first.",
            "Pick Breadth-First Search when you want to know what can be started today and what each level unlocks."
        ]
    }


def summarize_skill_demand(careers=None):
    """
    Counts how many careers require each skill, which answers "what should I
    learn if I am still undecided?" using nothing but the knowledge base.
    Returns a list of {skill, required_by, careers, difficulty, learning_hours}
    sorted by how many careers need it.
    """
    if careers is None:
        careers = CAREER_DATABASE

    demand = {}
    for career in careers:
        for skill in career["required_skills"]:
            entry = demand.setdefault(skill, {"skill": skill, "required_by": 0, "careers": []})
            entry["required_by"] += 1
            entry["careers"].append(career["title"])

    for skill, entry in demand.items():
        meta = SKILL_LIBRARY.get(skill, {})
        entry["difficulty"] = meta.get("difficulty", "Intermediate")
        entry["learning_hours"] = meta.get("learning_hours", 40)
        entry["category"] = meta.get("category", "Other")

    return sorted(
        demand.values(),
        key=lambda item: (-item["required_by"], item["skill"])
    )
