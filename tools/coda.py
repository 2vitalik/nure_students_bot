from shared_utils.api.coda.v2.doc import CodaDoc

import conf


coda_doc = CodaDoc('dOgO644f8xs', coda_token=conf.coda_token,
                   conf_path=conf.coda_conf_path)
# coda_doc.update_structure()
