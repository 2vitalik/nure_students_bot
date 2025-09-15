from shared_utils.api.coda.v2.doc import CodaDoc

import conf


doc = CodaDoc(conf.coda_docs['python-24'], coda_token=conf.coda_token,
              conf_path=f'{conf.data_path}/coda_conf')
# doc.update_structure()  # todo: feature to backup previous version...
# doc.conf.update_original()
# doc.conf.create_overriden()
