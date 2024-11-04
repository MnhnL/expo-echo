import json
import datetime
import pprint

from graphqlclient import GraphQLClient

from config import API_URL, API_TOKEN

def query(q, q_args, params):
    q_args_int = q_args.format(**params)
    q_int = q % q_args_int

    result_str = client.execute(q_int)
    result = json.loads(result_str)
    return result

class Event:
    def __init__(self, expo_dict):
        self.id = expo_dict['id']
        self.visible = expo_dict['visible']
        self.start_at = datetime.datetime.fromisoformat(expo_dict['startAt'])
        self.end_at = datetime.datetime.fromisoformat(expo_dict['endAt'])
        offer = expo_dict['offer']
        self.offer_id = offer['id']
        self.offer_name = offer['name']
        self.attendee_limit = expo_dict['attendeeLimit']
        self.reserved_spots = expo_dict['reservedSpots']
        self.unlimited = expo_dict['unlimited']

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self))

client = GraphQLClient(API_URL)

client.inject_token(f'Bearer {API_TOKEN}')

today = datetime.date.today()
today_iso = today.isoformat()

horizon = today + datetime.timedelta(days=31)
horizon_iso = horizon.isoformat()

query_str = '''
{
  events(%s) {
    totalNodeCount
    totalPageCount
    pageInfo {
      startCursor
      endCursor
    }
    nodes {
      id
      visible
      startAt
      endAt
      offer {
        id
        name
        article {id, active, name, number, priceCents, priceCurrency}
      }
      attendeeLimit
      reservedSpots
      unlimited
    }
  }
}
'''

query_args_str = 'search: {{startAtGteq: "{start_at_gteq}", endAtLteq: "{end_at_lteq}"}}, sortings: {{startAt: asc}}'
query_args_after_str = 'search: {{startAtGteq: "{start_at_gteq}", endAtLteq: "{end_at_lteq}"}}, sortings: {{startAt: asc}}, after: "{after}"'

end_cursor = True

result = query(query_str, query_args_str, {
    'start_at_gteq': today_iso,
    'end_at_lteq': horizon_iso,
})
ev = result['data']['events']

events = []

while end_cursor:
    for n in ev['nodes']:
        events.append(n)
        
    page_info = ev['pageInfo']
    start_cursor = page_info['startCursor']
    end_cursor = page_info['endCursor']

    result = query(query_str, query_args_after_str, {
        'start_at_gteq': today_iso,
        'end_at_lteq': horizon_iso,
        'after': end_cursor,
    })
    ev = result['data']['events']
    
for i, ev_dict in enumerate(filter(lambda ev: ev['visible'], events)):
    e = Event(ev_dict)
    if e.visible:
        print(i)
        print(e)
