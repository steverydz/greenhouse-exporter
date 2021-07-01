from models import Candidates


def add_new_candidates(greenhouse_cursor, canonical_session):
    greenhouse_cursor.execute(
        "SELECT id, first_name, last_name FROM candidates WHERE created_at between '2021-07-01' and '2021-07-02'"
    )

    for candidate in greenhouse_cursor.fetchall():
        c = Candidates(id=candidate[0], first_name=candidate[1], last_name=candidate[2])
        canonical_session.add(c)

    canonical_session.commit()