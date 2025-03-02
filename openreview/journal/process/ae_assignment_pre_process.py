def process(client, edge, invitation):

    journal = openreview.journal.Journal()

    submission = client.get_note(edge.head)

    venue_id = submission.content.get('venueid', {}).get('value')
    if venue_id not in [journal.submitted_venue_id, journal.under_review_venue_id]:
        raise openreview.OpenReviewException(f'Can not edit assignments for this submission: {venue_id}')

    if edge.ddate:

        submission=client.get_note(edge.head)

        decisions=client.get_notes(invitation=journal.get_ae_decision_id(number=submission.number))

        if decisions:
            raise openreview.OpenReviewException(f'Can not remove assignment, the user {edge.tail} already posted a decision.')

    else:
        ## Check conflicts
        conflicts = journal.assignment.compute_conflicts(submission, edge.tail)
        if conflicts:
           raise openreview.OpenReviewException(f'Can not add assignment, conflict detected for {edge.tail}.')