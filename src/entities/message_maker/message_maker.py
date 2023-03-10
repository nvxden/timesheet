import datetime as dt

from src.domain.locator import LocatorStorage, Locator
from src.entities.event.event import Event
from src.entities.message_maker.emoji import Emoji
from src.entities.message_maker.help import *
from src.entities.message_maker.piece import *
from src.utils.utils import reduce_list, insert_between


class MessageMaker(LocatorStorage):
  def __init__(self, locator: Locator):
    super().__init__(locator)

  @staticmethod
  def help() -> [Piece]:
    pieces = []
    pieces.extend(help_head)
    pieces.append(Piece('\n\n'))
    pieces.extend(
      reduce_list(lambda a, b: a + b,
                  insert_between(
                    [[Piece(f'{Emoji.COMMAND} ' + com.preview + '\n'), Piece(com.long)]
                     for com in commands],
                    [Piece('\n\n')],
                  ),
                  []),
    )
    pieces.append(Piece('\n\n'))
    pieces.extend(help_tail)
    return pieces

  @staticmethod
  def timesheetPost(
    events: [Event],
    head: [Piece] = None,
    tail: [Piece] = None
  ) -> [Piece]:
    assert(len(events) != 0)
    events = sorted(events, key=lambda e: e.start)
    paragraphs = []
    if head is not None:
      paragraphs.append(head)
    paragraph = []
    new_day = True
    for i in range(len(events)):
      event = events[i]
      if new_day:
        paragraph = [Piece(get_day(event.start))]
        new_day = False
      if len(paragraph) > 0:
        paragraph.append(Piece('\n'))
      paragraph.extend(get_event_line(event, url=event.url))
      if i+1 == len(events) or is_other_day(events[i].start, events[i+1].start):
        paragraphs.append(paragraph)
        new_day = True
    if tail is not None:
      paragraphs.append(tail)
    result = [*paragraphs[0]]
    for p in paragraphs[1:]:
      result.extend([Piece('\n\n'), *p])
    return result
  
  @staticmethod
  def eventPreview(event: Event) -> str:
    line = ''.join([piece.text for piece in get_event_line(event)])
    if event.url is not None:
      line += f', {event.url}'
    return f'{line[0]} #{event.id} {get_day(event.start, weekday=False)} {line[2:]}'


def get_event_line(event: Event, url: str = None) -> [Piece]:
  return [Piece(f'???? {event.place.name} ' +
                get_start_finish_time(event.start, event.finish) + ' '),
          Piece(event.desc, url=url)]


def is_other_day(lhs: dt.datetime, rhs: dt.datetime):
  return (dt.datetime(year=lhs.year, month=lhs.month, day=lhs.day) !=
          dt.datetime(year=rhs.year, month=rhs.month, day=rhs.day))
  
  
def get_day(date: dt.datetime, weekday: bool = True) -> str:
  return (str(int(date.strftime('%d'))) + ' '+
          date.strftime('%B') + (', ' + date.strftime('%A')
                                 if weekday else
                                 ''))


def get_start_finish_time(start: dt.datetime, _: dt.datetime) -> str:
  return f'{start.strftime("%H:%M")}'
