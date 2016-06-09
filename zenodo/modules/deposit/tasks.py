# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Celery tasks for Zenodo Deposit."""

from __future__ import absolute_import

from celery import shared_task

from invenio_pidstore.providers.datacite import DataCiteProvider
from zenodo.modules.records.serializers import datacite_v31
from invenio_records_files.api import Record
from flask import current_app


@shared_task
def mint_doi(pid_value, record_uuid):
    """Mint the DOI with DataCite.

    :param pid_value: Value of record PID, with pid_type='recid'.
    :type pid_value: str
    """
    record = Record.get_record(record_uuid)
    dcp = DataCiteProvider.get(record['doi'])
    url = current_app.config['ZENODO_RECORDS_UI_LINKS_FORMAT'].format(
        recid=pid_value)
    doc = datacite_v31.dump(dict(metadata=record.dumps()))
    dcp.register(url, doc)
