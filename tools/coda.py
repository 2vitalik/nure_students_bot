from shared_utils.api.coda.v2.doc import CodaDoc

import conf


coda_doc = CodaDoc(conf.coda_doc_id, coda_token=conf.coda_token,
                   conf_path=conf.coda_conf_path)

coda_tables = {
    'teachers': coda_doc.Teachers,
    'students': coda_doc.Students,
    'streams': coda_doc.StudentStreams,
    'groups': coda_doc.StudentGroups,
    'tg_users': coda_doc.TelegramUsers,
    'tg_chats': coda_doc.TelegramChats,
    'chats_stream': coda_doc.TelegramStreamChats,
    'chats_group': coda_doc.TelegramGroupChats,
    'chats_other': coda_doc.TelegramOtherChats,
}
