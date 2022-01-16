from semanticscholar import SemanticScholar

# get the Semantic Scholar ID and format it properly
get_semanticscholar_id(profile):
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
    
def build_id_mapping(profiles):
  idhash = {}
  for profile in profiles:
    idhash[get_semanticscholar_id(profile)] = profile.id
  return idhash

# in all the profiles, substitute OpenReview IDs for Semantic Scholar IDs in the SemanticScholarPapers attribute
def substitute_ids(profiles):
  idhash = build_id_mapping(profiles)
  
  for profile in profiles:
    for paper in profile.content['SemanticScholarPapers']:
      # there will be some authors who don't have OpenReview ids; we can't do anything with this info so we ignore it for now
      paper['authors'] = [idhash[x] for x in paper['authors'] if x in idhash]
