def process(client, edit, invitation):

    journal = openreview.journal.Journal()

    ## Notify readers
    journal.notify_readers(edit)

    note = client.get_note(edit.note.id)

    ## On update or delete return
    if note.tcdate != note.tmdate:
        return

    recommendations = client.get_notes(forum=note.forum, invitation=edit.invitation)
    if len(recommendations) == 3:

        submission = client.get_note(note.forum)
        duedate = datetime.datetime.utcnow() + datetime.timedelta(weeks = 1)

        journal.invitation_builder.set_review_rating_invitation(journal, submission, openreview.tools.datetime_millis(duedate))

        ## send email to action editors
        client.post_message(
            recipients=[journal.get_action_editors_id(number=submission.number)],
            subject=f'''[{journal.short_name}] Evaluate reviewers and submit decision for {journal.short_name} submission {submission.content['title']['value']}''',
            message=f'''Hi {{{{fullname}}}},

Thank you for overseeing the review process for {journal.short_name} submission "{submission.content['title']['value']}".

All reviewers have submitted their official recommendation of a decision for the submission. Therefore it is now time for you to determine a decision for the submission. Before doing so:

- Make sure you have sufficiently discussed with the authors (and possibly the reviewers) any concern you may have about the submission.
- Rate the quality of the reviews submitted by the reviewers. **You will not be able to submit your decision until these ratings have been submitted**. To rate a review, go on the submission’s page and click on button “Rating” for each of the reviews.

We ask that you submit your decision **within 1 week** ({duedate.strftime("%b %d")}). To do so, please follow this link: https://openreview.net/forum?id={submission.id}

The possible decisions are:
- **Accept as is**: once its camera ready version is submitted, the manuscript will be marked as accepted.
- **Accept with minor revision**: to use if you wish to request some specific revisions to the manuscript, to be specified explicitly in your decision comments. These revisions will be expected from the authors when they submit their camera ready version.
- **Reject**: the paper is rejected, but you may indicate whether you would be willing to consider a significantly revised version of the manuscript. Such a revised submission will need to be entered as a new submission, that will also provide a link to this rejected submission as well as a description of the changes made since.

Your decision may also include certification(s) recommendations for the submission (in case of an acceptance).

For more details and guidelines on performing your review, visit {journal.website}.

We thank you for your essential contribution to {journal.short_name}!

The {journal.short_name} Editors-in-Chief
''',
            replyTo=journal.contact_info
        )