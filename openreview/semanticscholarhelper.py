from semanticscholar import SemanticScholar

# get the Semantic Scholar ID and format it properly
def get_semanticscholar_id(profile):
  try:
    ssid = profile.content['semanticScholar']
    ssid = re.sub('[^/]*/', '', ssid)
    return ssid
  except:
    print('no Semantic Scholar ID for profile ' + profile.id)
    return -1
  
# add this person's Semantic Scholar Papers to their profile
def extend_profile(profile):
  sch = SemanticScholar(timeout=100)
  
  try:
    ssid = get_semanticscholar_id(profile)
  
    # get the Semantic Scholar profile
    ssprofile = sch.author(ssid)

    for paper in ssprofile['papers']:
      papers[paper['paperId']] = {'paperId': paper['paperId'], 'year': paper['year'], 'title': paper['title'], 'venue': paper['venue'], 'authors': [x['authorId'] for x in paper['authors']], 'doi': paper['doi'], 'url': paper['url']}

    profile.content['SemanticScholarPapers'] = papers
  except:
    print('something went wrong! ' + profile.id)
