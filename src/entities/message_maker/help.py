from src.entities.message_maker.piece import Piece


class CommandDescription:
  def __init__(self, name: str, preview: str, short: str, long: str):
    self.name = name
    self.preview = preview
    self.short = short
    self.long = long


help_head = [
  Piece('Этот бот предназначен для составления расписания '
        'событий и автоматического редактирования постов в канале '
        'таким образом, чтобы они отображали актуальное состояние '
        'расписания. Пользуйтесь :)')
]

help_tail = [
  Piece('Создан by @lega4e, исходный код '),
  Piece('здесь', url='https://github.com/nvxden/timesheet')
]

commands = [
  CommandDescription(name, preview, short, long)
  for name, preview, short, long in [
    (
      'help',
      '/help',
      'Показать помощь',
      'Показывает страницу с подробным объяснением команд (эту)',
    ),
    (
      'make_event',
      '/make_event',
      'Добавить новое событие в расписание',
      'Добавляет новое событие в подключённое расписание',
    ),
    (
      'show_events',
      '/show_events',
      'Посмотреть имеющиеся события в расписании',
      'Показывает в кратком виде все события, принадлежащие подключённому расписанию; здесь можно узнать id события (предваряется решёткой "#") для команд /edit_event и /remove_event',
    ),
    (
      'edit_event',
      '/edit_event ID',
      'Редактировать событие',
      'Открывает диалог для редактирования выбранного события, принадлежащее подключённому расписанию. Событие выбирается с помощью идентификатора; чтобы узнать идентификатор события, используйте команду /show_events',
    ),
    (
      'remove_event',
      '/remove_event ID',
      'Удалить событие',
      'Удаляет из подключённого расписание событие с указаным идентификатором. Идентификатор события можно узнать с помощью команды /show_events',
    ),
    (
      'make_timesheet',
      '/make_timesheet NAME PASSWORD',
      'Создать новое расписание',
      'Создаёт новое расписание с указаным именем и паролем. Имя и пароль должны состоять только из латинских букв, цифр и символов нижнего подчёркивания. Имя и пароль будут использоваться для подключения к расписанию с помощью команды /set_timesheet. Подключиться к расписанию может любой пользователь',
    ),
    (
      'set_timesheet',
      '/set_timesheet NAME PASSWORD',
      'Подключиться к расписанию',
      'Подключает к расписанию с указаным именем. Для защиты используется пароль: спросите его у создателя расписания',
    ),
    (
      'set_channel',
      '/set_channel CHANNEL',
      'Установить канал',
      'Устанавливает канал, в который бот будет постить расписание и держать его актуальным. CHANNEL — это либо логин канала (вида @xxx) либо ссылка на канал (вида https://t.me/channel_login)',
    ),
    (
      'post',
      '/post',
      'Запостить расписание в канал',
      'Запостить подключённое расписание в установленный канал',
    ),
    (
      'post_preview',
      '/post_preview',
      'Показать расписание в чате',
      'Отправить пост расписания не в канал, а в чат с вами',
    ),
    (
      'translate',
      '/translate [message_id]',
      'Транслировать расписание в канал',
      'Постит расписание в канал и держит текст актуальным (реагирует на любые операции изменяющие расписания). Может быть вызван без аргументов — тогда создаётся новый пост. Может добавляться аргумент message_id, который представляет из себя номер сообщения в установленном канале либо ссылку на сообщение: бот отредактирует это сообщение, чтобы оно соответствовало расписанию и будет держать в актуальном состоянии',
    ),
    (
      'clear_translations',
      '/clear_translations',
      'Очистить все трансляции в канал',
      'Отключает поддержание постов в канале в актуальном состоянии',
    ),
  ]
]