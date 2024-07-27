# encoding:utf-8

import asyncio
from bot.bot import Bot
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from config import conf
from DouBaoChat.bot import ChatBot as DouBaoChatBot


# 豆包对话模型API
class DouBaoBot(Bot):
    def __init__(self):
        super().__init__()
        self._bot = DouBaoChatBot(
            api_key=conf().get("doubao_api_key"),
            endpoint=conf().get("model") or "doubao_pro_32k",
            bot_id=conf().get("doubao_bot_id"),
            timeout=conf().get("request_timeout"),
            temperature=conf().get("temperature", 0.9),
            top_p=conf().get("top_p", 1),
            frequency_penalty=conf().get("frequency_penalty", 0.1),
            system_prompt=conf().get("character_desc"),
        )

    def reply(self, query, context=None) -> Reply:
        if context.type == ContextType.TEXT:
            session_id = context["session_id"]
            if query in ["重置", "reset"]:
                self._bot.reset(session_id)
                return Reply(content="您的对话已重置", type=ReplyType.TEXT)
            logger.info("[DOUBAO] query={}".format(query))
            reply = asyncio.run(self._bot.ask(query, session_id))
            logger.debug(
                "[DOUBAO] session_id={}, reply_cont={}".format(
                    session_id,
                    reply
                )
            )
            reply = Reply(content=reply, type=ReplyType.TEXT)
            return reply
        else:
            logger.error("[DouBao] context type not supported")
            return Reply(content="不支持的消息类型", type=ReplyType.TEXT)