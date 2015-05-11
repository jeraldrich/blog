Multiprocessing SQLAlchemy Largefile Processing
=======

The first step of any analytics data pipeline is to integrate external datasources, filter, and insert into a datastore. Usually, threading is good enough to process each line and insert into the database.

However, when processing large files (1GB+), one cpu core will spike at 100% and the GIL will fight for CPU contention between parsing each line, filtering / inserting the data, and switching between threads.

In this example, I have a simple table called chat_messages which is populated by parsing a large json file of JSON strings. The main point of this is to show how easy it is to use multiprocessing.

I am using python multiprocessing to parse the large file in one process, and filter/insert the data in every other CPU avaliable. This dropped CPU usage from 100% on one core, to 10-20% per core. When insering 10+ million rows into a mysql database, total time of using twisted / threaded vs multiprocessing dropped from 10+ minutes, to 2 minutes.

I used the consumer producer pattern because then I could easily share one queue  between all of the different processes. One producer fills the queue with each parsed line from the log file, and a consumer is spawned per CPU core which consumes each line in the queue.

A mysql session pool is created and shared between every consumer process (SQLAlchemy). When there are 500+ line items in the consumer queue, mysql inserts will be automatically batched.

Here's the full source: https://github.com/jeraldrich/MSLP

Here's what the SQLAlchemy model looks like::

        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, String, TIMESTAMP


        Base = declarative_base()


        class ChatMessage(Base):
            __tablename__ = 'chat_messages'
            __table_args__ = {'mysql_engine': 'InnoDB'}

            id = Column('id', String(255), primary_key=True)
            _from = Column('from', String(255), nullable=False)
            _type = Column('type', String(50))
            site_id = Column('site_id', String(50), nullable=False, index=True)
            data = Column('data', String(255), default='')
            timestamp = Column('timestamp', TIMESTAMP, nullable=False, index=True)

            def __repr__(self):
                return "id='{id}',ts='{ts}',type='{t}',data='{data}'>".format(
                    id=self.id,
                    ts=self.timestamp,
                    t=self._type,
                    data=self.data,
                )

Here's what I use to filter each json line and create a new SQLAlchemy object::

        import json
        import logging
        from datetime import datetime

        from consumers.models import ChatMessage


        logger = logging.getLogger('chat_message_parser')

        class ChatMessageParser():

            def parse(self, data):
                """
                parse each line in the log and populate log data with matched pattern
                """
                json_message = json.loads(data)
                # logger.info('json data is {0}'.format(json_message['data']))
                chat_message = None
                if json_message['type'] == 'message':
                    chat_message = ChatMessage(
                        id=json_message['id'],
                        _from=json_message['from'],
                        _type=json_message['type'],
                        site_id=json_message['site_id'],
                        data=json_message['data']['message'],
                        timestamp=json_message['timestamp'],
                    )
                elif json_message['type'] == 'status':
                    chat_message = ChatMessage(
                        id=json_message['id'],
                        _from=json_message['from'],
                        _type=json_message['type'],
                        site_id=json_message['site_id'],
                        data=json_message['data']['status'],
                        timestamp=json_message['timestamp'],
                    )
                else:
                    logger.error('Invalid json status detected'.format(chat_message))
                    return None
                # convert timestamp str to datetime
                chat_message.timestamp = datetime.fromtimestamp(int(json_message['timestamp']))

                return chat_message


For my producer, a large file is split up into chunks, and then each chunk yields a line into the consumer queue::

        from itertools import chain, islice
        import os
        import time
        import logging

        logger = logging.getLogger('chat_message_parser')

        class LargeFileParser(object):

            def __init__(self, filename):
                self.filename = filename
                self.split_files = []
                # lines per split file
                self.split_every = 100000
                self._split_large_file()

            def __iter__(self):
                logger.info('yielding')
                while self.split_files:
                    split_file = self.split_files.pop()
                    with open(split_file, 'rU') as f:
                        lines = f.readlines()
                        for line in lines:
                            yield line
                    logger.info('removing split_file')
                    os.remove(split_file)
                lines = None
                logger.info('end')

            def _split_large_file(self):
                """
                from http://codereview.stackexchange.com/a/57400
                """
                if not os.path.isfile(self.filename):
                    raise Exception(
                        'file does not exist:{0}'.format(self.filename)
                    )
                def _chunks(chunk_iterable, n):
                   chunk_iterable = iter(chunk_iterable)
                   while True:
                       yield chain([next(chunk_iterable)], islice(chunk_iterable, n-1))
                with open(self.filename) as bigfile:
                    for i, lines in enumerate(_chunks(bigfile, self.split_every)):
                        file_split = '{}.{}'.format(self.filename, i)
                        with open(file_split, 'w') as f:
                            f.writelines(lines)
                        self.split_files.append(file_split)
                #logger.info(self.split_files)
                return True

Instead of splitting a large file, you could probably iterate over chunks and use fileseek, but splitting the file up allows me to use multiple consumers if disk IO is not a bottleneck.


My consumer / producer processes are managed by using a multiprocessing manager queue which is wrapped in a class that spawns and joins the producer / consumer processes::

        from multiprocessing import Process, cpu_count, Manager
        from os import sys
        import time
        import logging
        from Queue import Empty

        from sqlalchemy.orm import scoped_session, sessionmaker
        from sqlalchemy import asc

        from producers import LargeFileParser, ChatMessageParser
        from consumers import create_mysql_pool, batch_insert
        from consumers.models import ChatMessage
        from settings import CHAT_LOG


        logger = logging.getLogger('chat_message_parser')
        logger.setLevel(logging.DEBUG)
        logging.basicConfig()
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        logger.addHandler(stream_handler)


        def producer_queue(queue, parser):
            for data in LargeFileParser(CHAT_LOG):
                parsed_data = parser.parse(data)
                queue.put(parsed_data)
            queue.put('STOP')


        def consumer_queue(proc_id, queue):

            # shared pooled session per consumer proc
            mysql_pool = create_mysql_pool()
            session_factory = sessionmaker(mysql_pool)
            Session = scoped_session(session_factory)

            while True:
                try:
                    time.sleep(0.01)
                    consumer_data = queue.get(proc_id, 1)
                    if consumer_data == 'STOP':
                        logger.info('STOP received')
                        # put stop back in queue for other consumers
                        queue.put('STOP')
                        break
                    consumer_data_batch = []
                    consumer_data_batch.append(consumer_data)
                    if queue.qsize() > 500:
                        for i in xrange(50):
                            consumer_data = queue.get(proc_id, 1)
                            consumer_data_batch.append(consumer_data)
                    session = Session()
                    batch_insert(session, consumer_data_batch)
                    # logger.info(consumer_data)
                except Empty:
                    pass


        class ParserManager(object):

            def __init__(self):
                self.manager = Manager()
                self.queue = self.manager.Queue()
                self.NUMBER_OF_PROCESSES = cpu_count()
                self.parser = ChatMessageParser()

            def start(self):
                self.producer = Process(
                    target=producer_queue,
                    args=(self.queue, self.parser)
                )
                self.producer.start()

                self.consumers = [
                    Process(target=consumer_queue, args=(i, self.queue,))
                    for i in xrange(self.NUMBER_OF_PROCESSES)
                ]
                for consumer in self.consumers:
                    consumer.start()

            def join(self):
                self.producer.join()
                for consumer in self.consumers:
                    consumer.join()

        if __name__ == '__main__':
            try:
                manager = ParserManager()
                manager.start()
                manager.join()
            except (KeyboardInterrupt, SystemExit):
                logger.info('interrupt signal received')
                sys.exit(1)
            except Exception, e:
                raise e

When using python multiprocessing, you will want to use the multiprocessing module to create all queues and threads. Otherwise, you may get a deadlock when two seperate processes try to read from the same queue at once.

By seperating the producer and consumers, the main flow of the program becomes very simple to manage. You can immediatly tell from the code what is going on, and add other SQLAlchemy models as needed.
