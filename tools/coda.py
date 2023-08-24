from shared_utils.api.coda.v2.doc import CodaDoc

import conf


coda_doc = CodaDoc(conf.coda_doc_id, coda_token=conf.coda_token,
                   conf_path=conf.coda_conf_path)
