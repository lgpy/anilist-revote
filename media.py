import requests as request
import json
from termcolor import colored

import login

def getInfo(id,type):
    print(colored('[Info]', 'blue'), 'Getting Manga Info')
    token = login.AccessToken()
    headers = {'Authorization': 'Bearer ' + token}
    query = '''
    query ($id: Int,$type: MediaType) { # Define which variables will be used in the query (id)
      Media (id: $id, type: $type) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
        id
        title {
          romaji
          english
          native
        }
        coverImage {
          extraLarge
          large
        }
        mediaListEntry {
          id
          mediaId
          status
          score
        }
      }
    }
    '''
    variables = {
        'id': id,
        'type': type
    }
    response = request.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}, headers=headers)
    return onResponse(response)
    #return json.loads(response.text)

def onResponse(response):
    if (response.status_code == 200):
        return json.loads(response.text)
    elif (response.status_code == 400):
        print(colored('[Error]', 'red'), 'Invalid Token')
        login.getAuth()
    else:
        return response.text

def getlist(type,format):
    query= '''
    query ($userId: Int, $userName: String, $type: MediaType) {
      MediaListCollection(userId: $userId, userName: $userName, type: $type) {
        lists {
          name
          isCustomList
          isCompletedList: isSplitCompletedList
          entries {
            ...mediaListEntry
          }
        }
      }
    }
    
    fragment mediaListEntry on MediaList {
      score
      media {
        id
        title {
          romaji
          english
        }
        coverImage {
          extraLarge
          large
        }
        averageScore
      }
    }
    '''
    token = login.AccessToken()
    headers = {'Authorization': 'Bearer ' + token}
    variables = {
        'userId': getID(),
        'type': type
    }
    response = request.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}, headers=headers)
    response = json.loads(response.text)
    list = []
    if type=='ANIME':
        if (format==None):
            for response_list in response['data']['MediaListCollection']['lists']:
                if (response_list['isCompletedList']):
                    for response_entries in response_list['entries']:
                        list.append(response_entries)
        else:
            for response_list in response['data']['MediaListCollection']['lists']:
                if (response_list['isCompletedList'] and (format.lower() in response_list['name'].lower())):
                    for response_entries in response_list['entries']:
                        list.append(response_entries)
    elif type=='MANGA':
        for response_list in response['data']['MediaListCollection']['lists']:
            if (response_list['name'].lower()=='completed'):
                for response_entries in response_list['entries']:
                    list.append(response_entries)
    else:
        return None
    return list

def getID():
    query='''{
      Viewer {
        id
      }
    }'''
    token = login.AccessToken()
    headers = {'Authorization': 'Bearer ' + token}
    response = request.post('https://graphql.anilist.co', json={'query': query, 'variables': {}}, headers=headers)
    return json.loads(response.text)['data']['Viewer']['id']

def changeScore(score,id):
    query = '''
    mutation ($id: Int, $mediaId: Int, $status: MediaListStatus, $score: Float, $progress: Int, $progressVolumes: Int, $repeat: Int, $private: Boolean, $notes: String, $customLists: [String], $hiddenFromStatusLists: Boolean, $advancedScores: [Float], $startedAt: FuzzyDateInput, $completedAt: FuzzyDateInput) {
      SaveMediaListEntry(id: $id, mediaId: $mediaId, status: $status, score: $score, progress: $progress, progressVolumes: $progressVolumes, repeat: $repeat, private: $private, notes: $notes, customLists: $customLists, hiddenFromStatusLists: $hiddenFromStatusLists, advancedScores: $advancedScores, startedAt: $startedAt, completedAt: $completedAt) {
        id
        mediaId
        status
        score
        advancedScores
        progress
        progressVolumes
        repeat
        priority
        private
        hiddenFromStatusLists
        customLists
        notes
        updatedAt
        startedAt {
          year
          month
          day
        }
        completedAt {
          year
          month
          day
        }
        user {
          id
          name
        }
        media {
          id
          title {
            userPreferred
          }
          coverImage {
            large
          }
          type
          format
          status
          episodes
          volumes
          chapters
          averageScore
          popularity
          isAdult
          startDate {
            year
          }
        }
      }
    }
    '''
    token = login.AccessToken()
    headers = {'Authorization': 'Bearer ' + token}
    variables = {
        'score': score,
        'mediaId': id
    }
    request.post('https://graphql.anilist.co', json={'query': query, 'variables': variables},headers=headers)