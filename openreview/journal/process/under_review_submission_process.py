def process(client, edit, invitation):

    note = client.get_note(edit.note.id)

    journal = openreview.journal.Journal()

    journal.setup_under_review_submission(note)

    duedate = datetime.datetime.utcnow() + datetime.timedelta(weeks = 1)

    journal.invitation_builder.set_reviewer_assignment_invitation(journal, note, duedate)

    client.post_message(
        recipients=[journal.get_action_editors_id(number=note.number)],
        subject=f'''[{journal.short_name}] Perform reviewer assignments for {journal.short_name} submission {note.content['title']['value']}''',
        message=f'''Hi {{{{fullname}}}},

With this email, we request that you assign 3 reviewers to your assigned {journal.short_name} submission "{note.content['title']['value']}". The assignments must be completed **within 1 week** ({duedate.strftime("%b %d")}). To do so, please follow this link: https://openreview.net/group?id={journal.get_action_editors_id()}

As a reminder, up to their annual quota of six reviews per year, reviewers are expected to review all assigned submissions that fall within their expertise. Acceptable exceptions are 1) if they have an unsubmitted review for another {journal.short_name} submission or 2) situations where exceptional personal circumstances (e.g. vacation, health problems) render them incapable of fully performing their reviewing duties.

We thank you for your essential contribution to {journal.short_name}!

The {journal.short_name} Editors-in-Chief
''',
        replyTo=journal.contact_info
    )