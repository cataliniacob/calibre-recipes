#!/usr/bin/env python

from __future__ import print_function

import io
import os
import subprocess
import sys
import tempfile

if __name__ == '__main__':
    suffix = '_cropped.pdf'

    for file_name in os.listdir(sys.argv[1]):
        if file_name.endswith(suffix):
            print('converting {}'.format(file_name))

            _, report_path = tempfile.mkstemp(file_name)
            _, edited_report_path = tempfile.mkstemp(file_name)

            subprocess.call(['pdftk', file_name, 'dump_data', 'output', report_path])
            title = file_name[:-len(suffix)]

            with io.open(report_path, 'r', encoding='ascii') as report, io.open(edited_report_path, 'w', encoding='ascii') as edited_report:
                right_after_title = False
                for line in report:
                    line = line.rstrip(u'\n')
                    if u'InfoKey: Title' in line:
                        right_after_title = True
                    if right_after_title and u'InfoValue:' in line:
                        right_after_title = False
                        line = u'InfoValue: {}'.format(title)
                    print(line, file=edited_report)
                        
                print(u'InfoBegin', file=edited_report)
                print(u'InfoKey: Author', file=edited_report)
                print(u'InfoValue: Ross Anderson', file=edited_report)

            subprocess.call(['pdftk', file_name, 'update_info', edited_report_path, 'output', 'final/{}.pdf'.format(title)])
        
