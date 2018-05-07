#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2018
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
from collections import OrderedDict
from queue import Queue

import pytest

from telegram import Bot
from telegram.ext import TypeHandler, HandlerContext, JobQueue
from telegram.utils.deprecate import TelegramDeprecationWarning


class TestTypeHandler(object):
    test_flag = False

    @pytest.fixture(autouse=True)
    def reset(self):
        self.test_flag = False

    def callback_basic(self, bot, update):
        test_bot = isinstance(bot, Bot)
        test_update = isinstance(update, dict)
        self.test_flag = test_bot and test_update

    def callback_queue_1(self, bot, update, job_queue=None, update_queue=None):
        self.test_flag = (job_queue is not None) or (update_queue is not None)

    def callback_queue_2(self, bot, update, job_queue=None, update_queue=None):
        self.test_flag = (job_queue is not None) and (update_queue is not None)

    def callback_context(self, update, context):
        self.test_flag = (isinstance(context, HandlerContext) and
                          isinstance(context.bot, Bot) and
                          isinstance(update, dict) and
                          isinstance(context.update_queue, Queue) and
                          isinstance(context.job_queue, JobQueue) and
                          context.user_data is None and
                          context.chat_data is None)

    def test_basic(self, dp):
        handler = TypeHandler(dict, self.callback_basic, use_context=False)
        dp.add_handler(handler)

        assert handler.check_update({'a': 1, 'b': 2})
        assert not handler.check_update('not a dict')
        dp.process_update({'a': 1, 'b': 2})
        assert self.test_flag

    def test_strict(self):
        handler = TypeHandler(dict, self.callback_basic, use_context=False, strict=True)
        o = OrderedDict({'a': 1, 'b': 2})
        assert handler.check_update({'a': 1, 'b': 2})
        assert not handler.check_update(o)

    def test_pass_job_or_update_queue(self, dp):
        handler = TypeHandler(dict, self.callback_queue_1, use_context=False, pass_job_queue=True)
        dp.add_handler(handler)

        dp.process_update({'a': 1, 'b': 2})
        assert self.test_flag

        dp.remove_handler(handler)
        handler = TypeHandler(dict, self.callback_queue_1, use_context=False,
                              pass_update_queue=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update({'a': 1, 'b': 2})
        assert self.test_flag

        dp.remove_handler(handler)
        handler = TypeHandler(dict, self.callback_queue_2, use_context=False, pass_job_queue=True,
                              pass_update_queue=True)
        dp.add_handler(handler)

        self.test_flag = False
        dp.process_update({'a': 1, 'b': 2})
        assert self.test_flag

    def test_context(self, dp):
        handler = TypeHandler(dict, self.callback_context, use_context=True)
        dp.add_handler(handler)

        dp.process_update({'a': 1, 'b': 2})
        assert self.test_flag

    def test_non_context_deprecation(self):
        with pytest.warns(TelegramDeprecationWarning):
            TypeHandler(dict, self.callback_context)
