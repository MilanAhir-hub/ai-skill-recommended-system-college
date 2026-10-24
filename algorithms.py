"""
algorithms.py
-------------
The optional, selectable algorithms that sit beside the original engine.

The system now offers a choice at two independent points:

    SCORING  (which career fits?)        PATH  (how do I get there?)
    ------------------------------       ---------------------------
    mcda           Weighted MCDA         topological   Kahn's sort  (original)
    decision_tree  Decision Tree  (new)  bfs           Breadth-First Search (new)
    bayes          Naive Bayes    (new)

Nothing here replaces the original algorithm: `mcda` and `topological` remain
the defaults and their code still lives in recommender.py. This module only
adds the alternatives, plus the machinery to compare them.

Every algorithm below is deterministic and rule-based. The decision tree is
declared as data in career_data.DECISION_TREE, and the Bayes probabilities are
expert-declared constants in career_data.BAYES_PARAMS: nothing is trained,
nothing is sampled, and no external service is called.
"""

import math

from career_data import (
    CAREER_DATABASE,
    INTEREST_LIBRARY,
    SKILL_CATEGORIES,
    DECISION_TREE,
    DECISION_TREE_SCORES,
    BAYES_PARAMS,
    ALGORITHM_CATALOG,
    DIFFICULTY_ORDER,
    JOB_READINESS_STEPS,
    get_skill_meta,
    get_career_by_id,
)

DEFAULT_SCORING_ALGORITHM = "mcda"
DEFAULT_PATH_ALGORITHM = "topological"

SCORING_ALGORITHM_IDS = [entry["id"] for entry in ALGORITHM_CATALOG["scoring"]]
PATH_ALGORITHM_IDS = [entry["id"] for entry in ALGORITHM_CATALOG["path"]]


def resolve_scoring_algorithm(name):
    """Returns a valid scoring algorithm id, falling back to the default."""
    if isinstance(name, str) and name.strip().lower() in SCORING_ALGORITHM_IDS:
        return name.strip().lower()
    return DEFAULT_SCORING_ALGORITHM


def resolve_path_algorithm(name):
    """Returns a valid path algorithm id, falling back to the default."""
    if isinstance(name, str) and name.strip().lower() in PATH_ALGORITHM_IDS:
        return name.strip().lower()
    return DEFAULT_PATH_ALGORITHM


def algorithm_info(algorithm_id, family="scoring"):
    """Catalog entry for one algorithm, used by the UI and the explanations."""
    for entry in ALGORITHM_CATALOG.get(family, []):
        if entry["id"] == algorithm_id:
            return entry
    return None


# ==========================================
# 1. Profile features shared by the new algorithms
# ==========================================
def dominant_interest_group(user_interests):
    """
    Counts how many of the student's interests fall into each declared interest
    group and returns the strongest one, with the full tally for the
    explanation. Ties break on the declared order of INTEREST_LIBRARY, so the
    answer is reproducible.
    """
    chosen = {i.strip().lower() for i in (user_interests or []) if isinstance(i, str) and i.strip()}

    tally = []
    for group, interests in INTEREST_LIBRARY.items():
        hits = [i for i in interests if i.lower() in chosen]
        tally.append({"group": group, "matches": len(hits), "interests": hits})

    best = max(tally, key=lambda item: item["matches"]) if tally else None
    if not best or best["matches"] == 0:
        return None, tally
    return best["group"], tally


def dominant_skill_category(known_skills):
    """
    Counts the student's skills per knowledge-base category and returns the
    strongest category. Ties break on category name for reproducibility.
    """
    known = set(known_skills or [])

    tally = []
    for category, skills in SKILL_CATEGORIES.items():
        hits = sorted(s for s in skills if s in known)
        tally.append({"category": category, "matches": len(hits), "skills": hits})

    tally.sort(key=lambda item: (-item["matches"], item["category"]))
    best = tally[0] if tally else None
    if not best or best["matches"] == 0:
        return None, tally
    return best["category"], tally


# ==========================================
# 2. Decision Tree (rule-based classification)
# ==========================================
def traverse_decision_tree(user_interests, known_skills):
    """
    Walks the declared decision tree once per request and records the decision
    path. Returns the leaf careers, the careers reachable elsewhere under the
    same branch, and a human-readable trace of each question and answer.
    """
    interest_group, interest_tally = dominant_interest_group(user_interests)
    skill_category, skill_tally = dominant_skill_category(known_skills)

    decisions = []

    # --- Question 1: interest group ---
    branches = DECISION_TREE["branches"]
    if interest_group and interest_group in branches:
        branch_key = interest_group
        answer = interest_group
        matched = True
    else:
        branch_key = "_default"
        answer = "No clear interest signal, using the skills-only branch"
        matched = False

    decisions.append({
        "step": 1,
        "question": DECISION_TREE["question"],
        "attribute": DECISION_TREE["attribute"],
        "answer": answer,
        "matched": matched,
        "evidence": [
            "{0}: {1} interest(s)".format(item["group"], item["matches"])
            for item in sorted(interest_tally, key=lambda i: -i["matches"])[:3]
            if item["matches"] > 0
        ]
    })

    node = branches[branch_key]

    # --- Question 2: strongest skill family ---
    child_branches = node.get("branches", {})
    if skill_category and skill_category in child_branches:
        child_key = skill_category
        answer = skill_category
        matched = True
    else:
        child_key = "_default"
        answer = (
            "{0} (no branch of its own, using the default leaf)".format(skill_category)
            if skill_category else "No skills entered, using the default leaf"
        )
        matched = False

    decisions.append({
        "step": 2,
        "question": node.get("question", "Which skill family is strongest?"),
        "attribute": node.get("attribute", "skill_category"),
        "answer": answer,
        "matched": matched,
        "evidence": [
            "{0}: {1} skill(s)".format(item["category"], item["matches"])
            for item in skill_tally[:3] if item["matches"] > 0
        ]
    })

    leaf_careers = list(child_branches[child_key].get("leaf", []))

    # Everything reachable elsewhere under the same interest branch counts as a
    # near miss: related, but not where the tree actually landed.
    branch_careers = []
    for child in child_branches.values():
        for career_id in child.get("leaf", []):
            if career_id not in leaf_careers and career_id not in branch_careers:
                branch_careers.append(career_id)

    decisions.append({
        "step": 3,
        "question": "Which careers sit at this leaf?",
        "attribute": "leaf",
        "answer": ", ".join(get_career_by_id(c)["title"] for c in leaf_careers if get_career_by_id(c)),
        "matched": True,
        "evidence": []
    })

    return {
        "branch": branch_key,
        "skill_branch": child_key,
        "leaf_careers": leaf_careers,
        "branch_careers": branch_careers,
        "decisions": decisions,
        "interest_tally": [i for i in interest_tally if i["matches"] > 0],
        "skill_tally": [s for s in skill_tally[:5] if s["matches"] > 0]
    }


def score_decision_tree(career, evidence, traversal):
    """
    Scores one career from the decision tree traversal.

    A career at the matched leaf starts high, a career elsewhere under the same
    branch starts in the middle, and anything the tree did not reach starts low.
    Each band is then widened by the student's actual skill coverage, and the
    degree adds or removes a small, declared amount.
    """
    cfg = DECISION_TREE_SCORES
    coverage = evidence["skill_ratio"]
    career_id = career["id"]

    if career_id in traversal["leaf_careers"]:
        placement = "leaf"
        reason = "Reached directly by the decision path"
        score = cfg["leaf_base"] + cfg["leaf_coverage"] * coverage
    elif career_id in traversal["branch_careers"]:
        placement = "branch"
        reason = "Sits under the same interest branch, but not at the matched leaf"
        score = cfg["branch_base"] + cfg["branch_coverage"] * coverage
    else:
        placement = "outside"
        reason = "Not reached by the decision path"
        score = cfg["other_base"] + cfg["other_coverage"] * coverage

    education_adjustment = 0.0
    if evidence["education_ratio"] >= 1.0:
        education_adjustment = cfg["education_bonus"]
    elif evidence["education_ratio"] <= 0.4:
        education_adjustment = cfg["education_penalty"]
    score += education_adjustment

    goal_bonus = evidence.get("goal_bonus", 0.0)
    score = max(0.0, min(100.0, score + goal_bonus))

    explanation = [
        "{0}. {1}: {2}".format(d["step"], d["question"], d["answer"])
        for d in traversal["decisions"]
    ]
    explanation.append(
        "Placement: {0} ({1}), widened by {2}% skill coverage{3}.".format(
            placement, reason, round(coverage * 100, 1),
            ", adjusted {0:+.0f} for the degree".format(education_adjustment)
            if education_adjustment else ""
        )
    )

    return {
        "score": round(score, 2),
        "placement": placement,
        "reason": reason,
        "decision_path": traversal["decisions"],
        "education_adjustment": education_adjustment,
        "goal_bonus": goal_bonus,
        "explanation": explanation
    }


# ==========================================
# 3. Naive Bayes (declared probabilities)
# ==========================================
def _log(probability):
    """Safe logarithm with Laplace smoothing, so no term can be log(0)."""
    smoothing = BAYES_PARAMS["smoothing"]
    return math.log(max(smoothing, min(1.0 - smoothing, probability)))


def _career_prior(career, total_weight):
    """P(career) from its declared market demand, normalised across careers."""
    weight = BAYES_PARAMS["demand_prior"].get(career.get("demand", "Moderate"), 1.0)
    return weight / total_weight


def bayes_log_posterior(career, evidence, total_prior_weight):
    """
    Computes the unnormalised log posterior for one career:

        log P(C | E) = log P(C) + sum over evidence of log P(e | C)

    Evidence is every skill in the career's benchmark (present or absent), the
    skills the student holds outside that benchmark, the career's interests,
    the degree, and the stated goal.
    """
    params = BAYES_PARAMS
    log_prior = math.log(_career_prior(career, total_prior_weight))
    log_likelihood = 0.0
    contributions = []

    core = set(career.get("core_skills", []))
    required = career["required_skills"]
    held = evidence["effective_skills"]

    # --- Benchmark skills: present / absent evidence ---
    for skill in required:
        p_present = params["p_core_skill_present"] if skill in core else params["p_required_skill_present"]
        if skill in held:
            term = _log(p_present)
            label = "has {0}".format(skill)
        else:
            term = _log(1.0 - p_present)
            label = "lacks {0}".format(skill)
        log_likelihood += term
        contributions.append({"evidence": label, "log_contribution": round(term, 3)})

    # --- Skills held outside this career's benchmark ---
    extra_skills = sorted(held - set(required))
    for skill in extra_skills:
        term = _log(params["p_unrelated_skill_present"])
        log_likelihood += term
        contributions.append({
            "evidence": "has {0}, outside this benchmark".format(skill),
            "log_contribution": round(term, 3)
        })

    # --- Interests ---
    matched_interests = set(evidence["matched_interests"])
    for interest in career["relevant_interests"]:
        if interest in matched_interests:
            term = _log(params["p_relevant_interest"])
            label = "interested in {0}".format(interest)
        else:
            term = _log(1.0 - params["p_relevant_interest"])
            label = "not interested in {0}".format(interest)
        log_likelihood += term
        contributions.append({"evidence": label, "log_contribution": round(term, 3)})

    # --- Education ---
    ratio = evidence["education_ratio"]
    if ratio >= 1.0:
        edu_key = "domain"
    elif ratio >= 0.75:
        edu_key = "general"
    elif ratio > 0.0:
        edu_key = "other"
    else:
        edu_key = "missing"
    term = _log(params["p_education"][edu_key])
    log_likelihood += term
    contributions.append({
        "evidence": "degree is a {0} match".format(edu_key),
        "log_contribution": round(term, 3)
    })

    # --- Stated goal ---
    if evidence.get("goal_match"):
        term = _log(params["p_goal_named"])
        label = "named this career as the goal"
    else:
        term = _log(params["p_goal_other"])
        label = "did not name this career"
    log_likelihood += term
    contributions.append({"evidence": label, "log_contribution": round(term, 3)})

    contributions.sort(key=lambda item: -item["log_contribution"])

    # Correct for the naive independence assumption before normalising: skills
    # are correlated, so the raw product over-counts the evidence.
    damping = BAYES_PARAMS.get("evidence_damping", 1.0)
    damped_likelihood = log_likelihood * damping

    return {
        "log_prior": round(log_prior, 4),
        "log_likelihood": round(log_likelihood, 4),
        "damping": damping,
        "log_posterior": log_prior + damped_likelihood,
        "prior_percentage": round(_career_prior(career, total_prior_weight) * 100, 2),
        "supporting_evidence": contributions[:4],
        "opposing_evidence": contributions[-3:][::-1]
    }


def bayes_posteriors(evidence_by_career, careers=None):
    """
    Computes normalised posteriors across every career, so the results sum to
    100%. Normalisation uses the log-sum-exp trick for numerical stability.

    evidence_by_career: {career_id: evidence dict}
    Returns {career_id: payload with posterior, percentage and explanation}
    """
    if careers is None:
        careers = CAREER_DATABASE

    total_weight = sum(
        BAYES_PARAMS["demand_prior"].get(c.get("demand", "Moderate"), 1.0) for c in careers
    )

    raw = {}
    for career in careers:
        evidence = evidence_by_career.get(career["id"])
        if evidence is None:
            continue
        raw[career["id"]] = bayes_log_posterior(career, evidence, total_weight)

    if not raw:
        return {}

    # log-sum-exp normalisation
    log_values = [item["log_posterior"] for item in raw.values()]
    peak = max(log_values)
    denominator = sum(math.exp(value - peak) for value in log_values)

    results = {}
    for career_id, item in raw.items():
        posterior = math.exp(item["log_posterior"] - peak) / denominator
        percentage = round(posterior * 100, 2)

        explanation = [
            "Prior from declared market demand: {0}%.".format(item["prior_percentage"]),
            "Log-likelihood of your evidence given this career: {0} (damped by {1} to correct for correlated skills).".format(
                item["log_likelihood"], item["damping"]
            ),
            "Strongest support: {0}.".format(
                "; ".join(e["evidence"] for e in item["supporting_evidence"][:3]) or "none"
            ),
            "Strongest evidence against: {0}.".format(
                "; ".join(e["evidence"] for e in item["opposing_evidence"][:2]) or "none"
            ),
            "Normalised posterior across all {0} careers: {1}%.".format(len(raw), percentage)
        ]

        results[career_id] = {
            "score": percentage,
            "posterior": posterior,
            "posterior_percentage": percentage,
            "prior_percentage": item["prior_percentage"],
            "log_prior": item["log_prior"],
            "log_likelihood": item["log_likelihood"],
            "supporting_evidence": item["supporting_evidence"],
            "opposing_evidence": item["opposing_evidence"],
            "explanation": explanation
        }

    return results


# ==========================================
# 4. Breadth-First Search learning path
# ==========================================
def _skill_sort_key(skill):
    """Same deterministic ordering used by the original engine."""
    meta = get_skill_meta(skill)
    return (DIFFICULTY_ORDER.get(meta["difficulty"], 2), meta["learning_hours"], skill.lower())


def bfs_levels(needed_skills, known_skills):
    """
    Level-order (breadth-first) traversal of the prerequisite graph.

    Level 1 holds every needed skill whose prerequisites are already satisfied,
    so they can all be started today and learned in parallel. Removing a level
    exposes the next frontier. A skill's level is therefore the length of its
    longest prerequisite chain inside the plan, which is exactly its BFS depth
    from the set of skills the student can start with.
    """
    needed = set(needed_skills or [])
    known = set(known_skills or [])

    remaining = set(needed)
    resolved = set()
    levels = []

    while remaining:
        frontier = []
        for skill in remaining:
            prereqs = [
                p for p in get_skill_meta(skill)["prerequisites"]
                if p in needed and p not in known
            ]
            if all(p in resolved for p in prereqs):
                frontier.append(skill)

        # Guard: a cycle would leave nothing ready. Release the lowest-key skill
        # so the traversal always terminates.
        if not frontier:
            frontier = [sorted(remaining, key=_skill_sort_key)[0]]

        frontier.sort(key=_skill_sort_key)
        levels.append(frontier)
        resolved.update(frontier)
        remaining.difference_update(frontier)

    return levels


def shortest_prerequisite_chain(skill, needed_skills, known_skills):
    """
    The shortest chain of prerequisites inside the plan that leads to `skill`,
    found by breadth-first search backwards through the graph. Used to explain
    why a deep skill cannot be started yet.
    """
    needed = set(needed_skills or [])
    known = set(known_skills or [])

    queue = [[skill]]
    seen = {skill}

    best = [skill]
    while queue:
        chain = queue.pop(0)
        head = chain[-1]
        prereqs = [
            p for p in get_skill_meta(head)["prerequisites"]
            if p in needed and p not in known
        ]
        if not prereqs:
            if len(chain) > len(best):
                best = chain
            continue
        for prereq in sorted(prereqs, key=_skill_sort_key):
            if prereq not in seen:
                seen.add(prereq)
                queue.append(chain + [prereq])

    return list(reversed(best))


def build_bfs_learning_plan(needed_skills, bridge_skills, known_skills, career,
                            hours_per_week, direct_gaps):
    """
    Builds the learning plan from BFS levels instead of difficulty phases.

    The output shape matches the original topological plan exactly, so the same
    interface renders either one; the difference is what a "phase" means. Here
    a phase is a dependency level: everything in it can be studied in parallel,
    and finishing it unlocks the next level.
    """
    known = set(known_skills or [])
    direct = set(direct_gaps or [])
    core_set = set(career.get("core_skills", []))

    levels = bfs_levels(needed_skills, known)
    sequence = [skill for level in levels for skill in level]

    depth_of = {}
    for index, level in enumerate(levels, start=1):
        for skill in level:
            depth_of[skill] = index

    phases = []
    total_hours = 0
    week_cursor = 0

    for index, level in enumerate(levels, start=1):
        items = []
        for skill in level:
            meta = get_skill_meta(skill)
            items.append({
                "skill": skill,
                "category": meta["category"],
                "difficulty": meta["difficulty"],
                "learning_hours": meta["learning_hours"],
                "prerequisites": meta["prerequisites"],
                "resources": meta["resources"],
                "steps": meta["roadmap"],
                "is_core_skill": skill in core_set,
                "is_bridge_skill": skill not in direct,
                "in_knowledge_base": meta["in_knowledge_base"],
                "bfs_level": index
            })

        level_hours = sum(item["learning_hours"] for item in items)
        level_weeks = int(math.ceil(level_hours / float(hours_per_week)))
        total_hours += level_hours

        unlocks = []
        if index < len(levels):
            unlocks = list(levels[index])

        if index == 1:
            goal = "Everything here is unblocked right now: start any of them today, in any order."
        else:
            goal = "Unlocked by finishing Level {0}. These {1} skill(s) can run in parallel.".format(
                index - 1, len(items)
            )

        phases.append({
            "phase": index,
            "display_phase": index,
            "name": "Level {0} - {1}".format(
                index, "Start now" if index == 1 else "Unlocked after Level {0}".format(index - 1)
            ),
            "goal": goal,
            "focus_difficulty": "Dependency level {0}".format(index),
            "skills": items,
            "action_steps": [],
            "portfolio_projects": [],
            "certifications": [],
            "estimated_hours": level_hours,
            "estimated_weeks": level_weeks,
            "starts_week": week_cursor + 1,
            "ends_week": week_cursor + level_weeks,
            "unlocks": unlocks,
            "parallel_count": len(items)
        })
        week_cursor += level_weeks

    # Applied phase, identical to the original plan's final phase.
    phases.append({
        "phase": len(levels) + 1,
        "display_phase": len(levels) + 1,
        "name": "Level {0} - Portfolio & Job Readiness".format(len(levels) + 1),
        "goal": "Turn the new skills into proof: projects, certificates, interviews.",
        "focus_difficulty": "Applied",
        "skills": [],
        "action_steps": list(JOB_READINESS_STEPS),
        "portfolio_projects": list(career.get("portfolio_projects", [])),
        "certifications": list(career.get("certifications", [])),
        "estimated_hours": 0,
        "estimated_weeks": 4,
        "starts_week": week_cursor + 1,
        "ends_week": week_cursor + 4,
        "unlocks": [],
        "parallel_count": 0
    })

    weeks = int(math.ceil(total_hours / float(hours_per_week))) if total_hours else 0
    months = round(weeks / 4.345, 1) if weeks else 0.0
    if weeks <= 0:
        duration = "No new learning required"
    elif weeks <= 4:
        duration = "About {0} week(s)".format(weeks)
    elif months < 1.5:
        duration = "About 1 month"
    else:
        duration = "About {0} months".format(months)

    # What to start first: the whole of level 1 is startable, core skills first.
    start_with = sorted(
        levels[0] if levels else [],
        key=lambda s: (0 if s in core_set else 1, _skill_sort_key(s))
    )[:3]

    deepest = max(depth_of.values()) if depth_of else 0
    deepest_skill = None
    if depth_of:
        deepest_skill = sorted(
            (s for s, d in depth_of.items() if d == deepest), key=_skill_sort_key
        )[0]

    return {
        "algorithm": "bfs",
        "hours_per_week": hours_per_week,
        "total_skills_to_learn": len(sequence),
        "skill_sequence": sequence,
        "bridge_skills": list(bridge_skills or []),
        "start_with": start_with,
        "phases": phases,
        "total_learning_hours": total_hours,
        "estimated_weeks": weeks,
        "estimated_months": months,
        "estimated_duration": duration,
        "bfs": {
            "levels": len(levels),
            "max_depth": deepest,
            "parallel_at_level_1": len(levels[0]) if levels else 0,
            "depth_by_skill": depth_of,
            "deepest_skill": deepest_skill,
            "longest_chain": (
                shortest_prerequisite_chain(deepest_skill, needed_skills, known)
                if deepest_skill else []
            )
        }
    }
