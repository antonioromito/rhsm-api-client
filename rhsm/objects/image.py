# Copyright (C) 2019 Antonio Romito (aromito@redhat.com)
#
# This file is part of the sos project: https://github.com/antonioromito/rhsm-api-client
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

import logging
import sys
import re

logging.getLogger(__name__)


class Image:
    def __init__(self, expiration, href):
        self.expiration = expiration
        self.href = href

    def get_filename(self, checksum):
        pattern = re.compile(checksum + '\\/(.*)\\?user\\=')
        filename = pattern.search(self.href).group(1)
        return filename

    @staticmethod
    def write_to_file(data, filename):
        file_name = filename

        with open(file_name, "wb") as f:
            print("Downloading %s" % file_name)
            response = data
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()

    @staticmethod
    def deserialize(data):

        image = Image(expiration=data['expiration'], href=data['href'])
        return image

