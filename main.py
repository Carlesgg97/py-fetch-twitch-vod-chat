import requests
import json
import sys
import argparse


ACCEPT_HEADER = "application/vnd.twitchtv.v5+json"
BASE_URL_TEMPLATE = "https://api.twitch.tv/v5/videos/%s/comments"

def parse_args():
  parser = argparse.ArgumentParser(description='Download a twitch vod\'s chat messages')
  parser.add_argument('vod_id', type=int, help='Vod id, obtained from the last digits of the vod url')
  parser.add_argument('client_id', type=str, help='Client id, visit https://dev.twitch.tv/docs/api to find out more')
  return parser.parse_args()

def fetch_vod_comments(vod_id, client_id):
  url = BASE_URL_TEMPLATE % vod_id
  qstring = "?content_offset_seconds=0"

  comments_list = []
  next_cursor = None

  while True:
    response = requests.get(url + qstring, headers={'Accept': ACCEPT_HEADER, 'Client-ID': client_id})
    print('Obtained response code %s for cursor %s' % (response.status_code, next_cursor), file=sys.stderr)
    json_data = response.json()
    comments_list = comments_list + json_data['comments']
    next_cursor = json_data.get('_next')
    if not next_cursor:
      break
    qstring = "?cursor=%s" % next_cursor
  return comments_list

if __name__ == '__main__':
  args = parse_args()
  comments_list = fetch_vod_comments(args.vod_id, args.client_id)
  print(json.dumps(comments_list, indent=2))
